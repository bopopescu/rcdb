#include "catch.hpp"
#include "RCDB/SqLiteProvider.h"

using namespace rcdb;

TEST_CASE("General test of SqLite", "[sqlite]")
{
    using namespace std;

    const char* env = std::getenv("RCDB_TEST_CONNECTION");
    if(env == nullptr) {
        FAIL("Environment variable RCDB_TEST_CONNECTION is not set");
    }


    if(string(env).find("sqlite://") == string::npos) {
        INFO("Connection string is not SQLite exiting SQLite provider tests");
        CAPTURE(env)
        // The test only works with SQLite
        return;
    }

    string path(env);
    SqLiteProvider prov(path);

    auto cnd = prov.GetCondition(1, string("int_cnd"));
    REQUIRE(cnd);
    REQUIRE(cnd->ToInt() == 5);


    cnd = prov.GetCondition(99999999999, string("int_cnd"));
    REQUIRE_FALSE(cnd);
}

