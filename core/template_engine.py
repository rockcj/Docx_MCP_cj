#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档模板引擎
提供模板的加载、渲染、验证和管理功能
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# ==================== 数据结构定义 ====================

@dataclass
class TemplateMetadata:
    """模板元数据"""
    id: str
    name: str
    category: str
    version: str
    description: str
    author: str = "system"
    created_date: str = ""
    tags: List[str] = field(default_factory=list)
    difficulty_level: str = "beginner"

@dataclass
class TemplateSection:
    """模板段落定义"""
    section_id: str
    section_type: str  # paragraph, heading, table, image
    content: Dict[str, Any]
    position: str
    required: bool = True
    editable: bool = False
    validation_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TemplateRules:
    """模板规则"""
    editable_sections: List[str] = field(default_factory=list)
    required_variables: List[str] = field(default_factory=list)
    optional_variables: List[str] = field(default_factory=list)
    validation_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AIGuidance:
    """AI指导信息"""
    suggested_prompts: List[str] = field(default_factory=list)
    content_examples: Dict[str, str] = field(default_factory=dict)
    style_guidelines: List[str] = field(default_factory=list)

@dataclass
class DocumentTemplate:
    """文档模板"""
    metadata: TemplateMetadata
    page_settings: Dict[str, Any]
    sections: List[TemplateSection]
    rules: TemplateRules
    ai_guidance: AIGuidance

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    error_messages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_variables: List[str] = field(default_factory=list)

@dataclass
class TemplateSuggestion:
    """模板建议"""
    template_id: str
    template_name: str
    match_score: float
    reason: str
    preview: str
    estimated_time: str

# ==================== 模板引擎核心类 ====================

class DocumentTemplateEngine:
    """文档模板引擎"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.template_registry: Dict[str, DocumentTemplate] = {}
        self.template_categories: Dict[str, List[str]] = {}
        
        # 确保模板目录存在
        self.templates_dir.mkdir(exist_ok=True)
        
        # 加载所有模板
        self._load_all_templates()
        
        logger.info(f"模板引擎初始化完成，加载了 {len(self.template_registry)} 个模板")
    
    def _load_all_templates(self):
        """加载所有模板文件"""
        if not self.templates_dir.exists():
            logger.warning(f"模板目录不存在: {self.templates_dir}")
            return
        
        for category_dir in self.templates_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                self.template_categories[category] = []
                
                for template_file in category_dir.glob("*.json"):
                    try:
                        template = self._load_template_from_file(template_file)
                        if template:
                            self.template_registry[template.metadata.id] = template
                            self.template_categories[category].append(template.metadata.id)
                            logger.info(f"加载模板: {template.metadata.name}")
                    except Exception as e:
                        logger.error(f"加载模板失败 {template_file}: {e}")
    
    def _load_template_from_file(self, file_path: Path) -> Optional[DocumentTemplate]:
        """从文件加载单个模板"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 解析元数据
            metadata = TemplateMetadata(**data["template_metadata"])
            
            # 解析页面设置
            page_settings = data["template_structure"]["page_settings"]
            
            # 解析段落
            sections = []
            for section_data in data["template_structure"]["sections"]:
                section = TemplateSection(**section_data)
                sections.append(section)
            
            # 解析规则
            rules = TemplateRules(**data["template_rules"])
            
            # 解析AI指导
            ai_guidance = AIGuidance(**data.get("ai_guidance", {}))
            
            return DocumentTemplate(
                metadata=metadata,
                page_settings=page_settings,
                sections=sections,
                rules=rules,
                ai_guidance=ai_guidance
            )
            
        except Exception as e:
            logger.error(f"解析模板文件失败 {file_path}: {e}")
            return None
    
    def get_template(self, template_id: str) -> Optional[DocumentTemplate]:
        """获取指定模板"""
        return self.template_registry.get(template_id)
    
    def get_available_templates(self, category: str = None) -> List[DocumentTemplate]:
        """获取可用模板列表"""
        if category:
            template_ids = self.template_categories.get(category, [])
            return [self.template_registry[tid] for tid in template_ids if tid in self.template_registry]
        else:
            return list(self.template_registry.values())
    
    def get_template_categories(self) -> List[str]:
        """获取模板分类列表"""
        return list(self.template_categories.keys())
    
    def suggest_templates_by_intent(self, user_intent: str) -> List[TemplateSuggestion]:
        """基于用户意图推荐模板"""
        suggestions = []
        
        # 关键词匹配
        intent_lower = user_intent.lower()
        
        for template in self.template_registry.values():
            score = 0.0
            reasons = []
            
            # 基于分类匹配
            if "商务" in intent_lower or "business" in intent_lower:
                if template.metadata.category == "business":
                    score += 0.8
                    reasons.append("匹配商务文档需求")
            
            if "学术" in intent_lower or "论文" in intent_lower or "academic" in intent_lower:
                if template.metadata.category == "academic":
                    score += 0.8
                    reasons.append("匹配学术文档需求")
            
            if "表格" in intent_lower or "table" in intent_lower:
                if template.metadata.category == "table":
                    score += 0.9
                    reasons.append("匹配表格需求")
            
            # 基于标签匹配
            for tag in template.metadata.tags:
                if tag.lower() in intent_lower:
                    score += 0.3
                    reasons.append(f"匹配标签: {tag}")
            
            # 基于描述匹配
            if any(keyword in template.metadata.description.lower() for keyword in intent_lower.split()):
                score += 0.2
                reasons.append("描述匹配")
            
            if score > 0:
                suggestion = TemplateSuggestion(
                    template_id=template.metadata.id,
                    template_name=template.metadata.name,
                    match_score=score,
                    reason="; ".join(reasons),
                    preview=template.metadata.description[:100] + "...",
                    estimated_time="5-10分钟"
                )
                suggestions.append(suggestion)
        
        # 按匹配分数排序
        suggestions.sort(key=lambda x: x.match_score, reverse=True)
        return suggestions[:5]  # 返回前5个建议
    
    def validate_template_data(self, template_id: str, data: Dict[str, Any]) -> ValidationResult:
        """验证模板数据"""
        template = self.get_template(template_id)
        if not template:
            return ValidationResult(
                is_valid=False,
                error_messages=[f"模板不存在: {template_id}"]
            )
        
        errors = []
        warnings = []
        missing_variables = []
        
        # 检查必填变量
        for required_var in template.rules.required_variables:
            if required_var not in data or not data[required_var]:
                missing_variables.append(required_var)
                errors.append(f"缺少必填变量: {required_var}")
        
        # 检查可选变量
        for optional_var in template.rules.optional_variables:
            if optional_var not in data:
                warnings.append(f"缺少可选变量: {optional_var}")
        
        # 检查验证规则
        for var_name, validation_rule in template.rules.validation_rules.items():
            if var_name in data:
                if not self._validate_variable_format(data[var_name], validation_rule):
                    errors.append(f"变量 {var_name} 格式不正确")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            error_messages=errors,
            warnings=warnings,
            missing_variables=missing_variables
        )
    
    def _validate_variable_format(self, value: Any, validation_rule: str) -> bool:
        """验证变量格式"""
        if validation_rule == "email_format":
            return "@" in str(value) and "." in str(value)
        elif validation_rule == "phone_format":
            return len(str(value).replace("-", "").replace(" ", "")) >= 10
        elif validation_rule == "date_format":
            try:
                datetime.strptime(str(value), "%Y-%m-%d")
                return True
            except ValueError:
                return False
        elif validation_rule.startswith("min_length_"):
            min_len = int(validation_rule.split("_")[-1])
            return len(str(value)) >= min_len
        elif validation_rule.startswith("max_length_"):
            max_len = int(validation_rule.split("_")[-1])
            return len(str(value)) <= max_len
        
        return True
    
    def render_template_preview(self, template_id: str, sample_data: Dict[str, Any] = None) -> str:
        """渲染模板预览"""
        template = self.get_template(template_id)
        if not template:
            return "模板不存在"
        
        preview_lines = []
        preview_lines.append(f"模板名称: {template.metadata.name}")
        preview_lines.append(f"分类: {template.metadata.category}")
        preview_lines.append(f"描述: {template.metadata.description}")
        preview_lines.append("")
        preview_lines.append("文档结构:")
        
        for section in template.sections:
            section_preview = f"- {section.section_id}: {section.section_type}"
            if section.required:
                section_preview += " (必填)"
            if section.editable:
                section_preview += " (可编辑)"
            preview_lines.append(section_preview)
        
        return "\n".join(preview_lines)
    
    def get_template_filling_guidance(self, template_id: str) -> Dict[str, Any]:
        """获取模板填写指导"""
        template = self.get_template(template_id)
        if not template:
            return {"error": "模板不存在"}
        
        guidance = {
            "template_name": template.metadata.name,
            "required_variables": template.rules.required_variables,
            "optional_variables": template.rules.optional_variables,
            "suggested_prompts": template.ai_guidance.suggested_prompts,
            "content_examples": template.ai_guidance.content_examples,
            "style_guidelines": template.ai_guidance.style_guidelines,
            "editable_sections": template.rules.editable_sections
        }
        
        return guidance

# ==================== 模板渲染器 ====================

class TemplateRenderer:
    """模板渲染器"""
    
    def __init__(self, template_engine: DocumentTemplateEngine):
        self.template_engine = template_engine
    
    def render_template_to_document(self, template_id: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """将模板渲染为文档结构"""
        template = self.template_engine.get_template(template_id)
        if not template:
            return {"error": "模板不存在"}
        
        # 验证数据
        validation_result = self.template_engine.validate_template_data(template_id, variables)
        if not validation_result.is_valid:
            return {"error": "数据验证失败", "details": validation_result.error_messages}
        
        # 渲染文档结构
        document_structure = {
            "page_settings": template.page_settings,
            "sections": []
        }
        
        for section in template.sections:
            rendered_section = self._render_section(section, variables)
            document_structure["sections"].append(rendered_section)
        
        return document_structure
    
    def _render_section(self, section: TemplateSection, variables: Dict[str, Any]) -> Dict[str, Any]:
        """渲染单个段落"""
        rendered_content = section.content.copy()
        
        # 替换变量
        if "text" in rendered_content:
            text = rendered_content["text"]
            for var_name, var_value in variables.items():
                placeholder = f"{{{{{var_name}}}}}"
                if placeholder in text:
                    text = text.replace(placeholder, str(var_value))
            rendered_content["text"] = text
        
        return {
            "section_id": section.section_id,
            "section_type": section.section_type,
            "content": rendered_content,
            "position": section.position,
            "required": section.required,
            "editable": section.editable
        }
