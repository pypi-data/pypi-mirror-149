import json, redis, os, requests, ast
# from mobio.libs.Singleton import Singleton
from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager

# @Singleton
class DataOut:

    def send(self, body, merchant_id, data_type):
        list_app = get_list_app_merchant_register(merchant_id, data_type)
        if list_app and len(list_app) > 0:
            kafka_manager = KafkaProducerManager()
            body_mess = {
                ParamTopicSaveEvent.DATA_EVENT: body,
                ParamTopicSaveEvent.MERCHANT_ID: merchant_id,
                ParamTopicSaveEvent.DATA_TYPE: data_type,
            }
            kafka_manager.flush_message(topic="save-event-need-send", key=merchant_id, value=body_mess)
            return True
        return False

global_redis_client = None
REDIS_DB = "{}?health_check_interval=30".format(os.environ.get("REDIS_URI", "redis://:Mobio123@redis.mobio.dev:6379/0"))
class RedisClient(object):
    @staticmethod
    def get_connect():
        global global_redis_client
        if global_redis_client is None:
            global_redis_client = redis.from_url(REDIS_DB)
        return global_redis_client

    def get_value(self, key_cache):
        redis_conn = self.get_connect()
        return redis_conn.get(key_cache)

    def set_value(self, key_cache, value_cache):
        redis_conn = self.get_connect()
        redis_conn.set(key_cache, value_cache, ex=1800)

class ParamTopicSaveEvent:
    DATA_EVENT = "data_event"
    MERCHANT_ID = "merchant_id"
    DATA_TYPE = "data_type"

def get_merchant_config_host(merchant_id, key_host):
    key_cache = "data_out#" + merchant_id + "#" + key_host
    redis_value = RedisClient().get_value(key_cache=key_cache)
    if not redis_value:
        adm_url = str("{host}/adm/api/v2.1/merchants/{merchant_id}/config/detail").format(
            host=os.environ.get("ADMIN_HOST", "https://api-test1.mobio.vn/"),
            merchant_id=merchant_id,
        )
        request_header = {"X-Module-Request": "DATA_OUT", "X-Mobio-SDK": "DATA_OUT"}
        param = {"fields": ",".join(["internal_host", "module_host", "public_host", "config_host"])}
        response = requests.get(
            adm_url,
            params=param,
            headers=request_header,
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
        data = result.get("data", {}) if result and result.get("data", {}) else {}
        RedisClient().set_value(key_cache=key_cache, value_cache=data.get(key_host, ""))
        return data.get(key_host)
    else:
        return str(redis_value.decode("utf-8"))

def get_list_app_merchant_register(merchant_id, data_type):
    key_cache = "data_out#" + merchant_id + "#" + data_type
    redis_value = RedisClient().get_value(key_cache=key_cache)
    # print(redis_value)
    if not redis_value:
        # print("get_list_app_merchant_register no cache")
        host_data_out = get_merchant_config_host(merchant_id, "data-out-app-api-service-host")
        # host_data_out = "https://api-test1.mobio.vn/"
        api_url = str("{host}/datasync/api/v1.0/event-out/app/register").format(
            host=host_data_out,
        )
        request_header = {"X-Module-Request": "DATA_OUT", "X-Mobio-SDK": "DATA_OUT",
                          "Authorization": 'Basic {}'.format(os.environ.get('YEK_REWOP', "f38b67fa-22f3-4680-9d01-c36b23bd0cad")),
                          "X-Merchant-ID": merchant_id,
                          }
        param = {"data_type": data_type}
        response = requests.get(
            api_url,
            params=param,
            headers=request_header,
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
        data = result.get("data", []) if result and result.get("data", []) else []
        RedisClient().set_value(key_cache=key_cache, value_cache=json.dumps(data, ensure_ascii=False))
        return data
    else:
        # print("get_list_app_merchant_register cache exists")
        return ast.literal_eval(str(redis_value.decode("utf-8")))


if __name__ == "__main__":
    body, merchant_id, data_type = {"name": "test"}, "1b99bdcf-d582-4f49-9715-1b61dfff3924", "profile"
    result = DataOut().send(body, merchant_id, data_type)
    print(result)
