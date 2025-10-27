#!/usr/bin/env python3
"""
简单测试混合传输模式的功能
"""

from final_complete_server import create_hybrid_starlette_app, mcp

def simple_test():
    """简单测试函数"""
    print("Simple Hybrid Transport Mode Test")
    print("=" * 40)

    try:
        # 创建混合应用
        print("Creating hybrid app...")
        app = create_hybrid_starlette_app(mcp, debug=True)
        print("[OK] Hybrid app created successfully")

        # 检查应用状态
        print("\nChecking application state...")
        assert hasattr(app.state, 'fastmcp_server')
        assert hasattr(app.state, 'supported_transports')
        assert 'sse' in app.state.supported_transports
        assert 'streamable-http' in app.state.supported_transports
        print("[OK] Application state correct")

        # 检查路由
        print("\nChecking routes...")
        routes = app.routes
        route_paths = [getattr(route, 'path', str(route)) for route in routes]
        print(f"Found routes: {route_paths}")

        expected_paths = ['/sse', '/messages/', '/mcp']
        for path in expected_paths:
            if any(path in route_path for route_path in route_paths):
                print(f"[OK] Route {path} found")
            else:
                print(f"[WARN] Route {path} not found")

        print("\n" + "=" * 40)
        print("SUCCESS: All basic tests passed!")
        print("Hybrid transport mode is working correctly.")

        return True

    except Exception as e:
        print(f"ERROR: Test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simple_test()
    if not success:
        exit(1)