import pytest
from scenarios.jwt_expiry_regression import JWTAuthService, TokenValidationError
from scenarios.database_deadlock import MockConnectionPool, BillingService, ConnectionPoolExhausted
from scenarios.redis_cache_stampede import ProductCatalogCache, CacheStampedeError

def test_jwt_auth_bug_and_fix():
    svc = JWTAuthService()
    
    # Buggy token expires immediately
    buggy_token = svc.create_token("user-42", buggy=True)
    with pytest.raises(TokenValidationError, match="Token expired"):
        svc.verify_token(buggy_token)

    # Fixed token validates successfully
    clean_token = svc.create_token("user-42", buggy=False)
    assert svc.verify_token(clean_token) is True

def test_database_connection_leak_and_fix():
    pool = MockConnectionPool(max_size=3)
    billing = BillingService(pool)

    # Buggy: 3 failed requests exhaust all 3 pool connections
    for _ in range(3):
        with pytest.raises(ValueError):
            billing.process_charge(-10.0, buggy=True)
    
    assert pool.available_count == 0
    with pytest.raises(ConnectionPoolExhausted):
        billing.process_charge(100.0, buggy=True)

    # Fixed pool: guarantees release even when exception is raised
    fixed_pool = MockConnectionPool(max_size=3)
    fixed_billing = BillingService(fixed_pool)
    for _ in range(5):
        with pytest.raises(ValueError):
            fixed_billing.process_charge(-10.0, buggy=False)
    
    # All connections remain available
    assert fixed_pool.available_count == 3
    assert fixed_billing.process_charge(50.0, buggy=False) is True

def test_cache_stampede_dogpiling_and_fix():
    # Cache with limit of 3 DB queries
    cache = ProductCatalogCache(db_query_limit=3)

    # Populate cache initially
    cache.get_product("sku-99", buggy=False)

    # Manually expire entry
    cache._cache["sku-99"]["expires_at"] = 0.0

    # Fixed logic protects DB during surge: stale serve while throttling
    for _ in range(10):
        item = cache.get_product("sku-99", buggy=False)
        assert item["id"] == "sku-99"
