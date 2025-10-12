from invoke import task

@task
def test_backend_data(c):
    """Run tests for back-end/data_accessor"""
    with c.cd('back-end/data_accessor'):
        c.run("hatch run dev:test")

@task
def test_backend_server(c):
    """Run tests for back-end/mcp_server"""
    with c.cd('back-end/mcp_server'):
        c.run("hatch run dev:test")

@task
def test_frontend_client(c):
    """Run tests for front-end/mcp_client"""
    with c.cd('front-end/mcp_client'):
        c.run("hatch run dev:test")

@task
def test_frontend_app(c):
    """Run tests for front-end/music-findr-app"""
    with c.cd('front-end/music-findr-app'):
        c.run("npm run test")

@task(pre=[
    test_backend_data,
    test_backend_server,
    test_frontend_app
])
def test(c):
    """Run all tests"""
    print("✅ All tests completed.")
