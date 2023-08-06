from v_cloud_market_cli_common.utils.server_api_wrapper import NewServerWrapper
from v_cloud_market_cli_common.config.server_config import API_VERSION
from .service_common import ServiceCommon

class UserServiceQueryParam:
    service_active = True
    service_id = ''
    service = ''
    status = []
    start_from = 0
    end_at = 0
    current = 1
    page_size = 10

    def as_dict(self) -> dict:

        return {
            'serviceActivated': selfv_cloud_market_cli_common.service_active,
            'serviceID': selfv_cloud_market_cli_common.service_id,
            'service': selfv_cloud_market_cli_common.service,
            'serviceStatuses[]': self.status,
            'userServiceStartFrom': self.start_from,
            'userServiceEndAt': self.end_at,
            'current': self.current,
            'pageSize': self.page_size
        }


class UserService:

    def __init__(self, net_type: str, password: str, nonce=0):
        self.cli, _ = NewServerWrapper(net_type, password, nonce)

    def get_user_service_page(self, current=1, page_size=10, statuses=None):
        '''
        Query user service via order info
        '''
        orderRoute = API_VERSION + '/order'

        activated = True
        if type(statuses) is not list:
            activated = statuses in ['ServicePending', 'ServiceRunning']
        opts = {
            'current': current,
            'pageSize': page_size,
            'serviceActivated': activated,
            'serviceStatuses[]': statuses if type(statuses) is list else [statuses]
        }

        opts = {k: v for k, v in opts.items() if v is not None}
        resp = self.cli.get_request(orderRoute, url_param=opts)
        ServiceCommon.validate_response(resp)
        return resp

    def get_user_service_info(self, provider_host: str, user_service_id: str):
        route = API_VERSION + '/userService/' + user_service_id
        tmp = self.cli.node_host
        self.cli.node_host = provider_host
        resp = self.cli.get_request(route, needAuth=True)
        ServiceCommon.validate_response(resp)
        self.cli.node_host = tmp
        return resp

    def access_user_api_get(self, user_service_id: str, api_type: str, api_func: str):
        route = API_VERSION + f'/service/userAPI/get/{api_type}/{api_func}/{user_service_id}'
        resp = self.cli.get_request(route, needAuth=True)
        return resp

    def access_user_api_post(self, user_service_id: str, api_type: str, api_func: str):
        pass

    def query_user_service(self, param: UserServiceQueryParam):
        route = API_VERSION + '/order'
        resp = self.cli.get_request(route, url_param=param.as_dict())
        ServiceCommon.validate_response(resp)
        return resp

    def _get_service_provider_api(self, provider_id: str):
        route = API_VERSION + '/service/provider/' + provider_id
        resp = self.cli.get_request(route)

        if isinstance(resp, dict):
            result = {
                'provider': resp.get('name', ''),
                'apiHost': resp.get('apiHost', '')
            }
        else:
            result = {
                'provider': '',
                'apiHost': ''
            }
        return result

    def _get_order_distinct_list(self, distinct_field: str, order_statuses: list):
        '''
        return: a list of distinct_field value
        '''
        route = API_VERSION + '/order/distinct'
        opts = {
            'distinctField': distinct_field,
            'statuses': order_statuses if type(order_statuses) is list else [order_statuses]
        }
        resp = self.cli.get_request(route, url_param=opts)
        ServiceCommon.validate_response(resp)
        return resp

    def check_image(self, image_info: str) -> bool:
        try:
            colon_index = image_info.rfind(":")
            image_name = image_info
            if colon_index < 0:
                return False
            image_name = image_info[:colon_index]
            tag = image_info[colon_index + 1:]
            route = f'/v1/repositories/{image_name}/tags/{tag}'
            temp = self.cli.node_host
            self.cli.node_host = "https://index.docker.io"
            resp = self.cli.get_request(route, raw_res=True)
            self.cli.node_host = temp
            return resp.status_code == 200
        except Exception as err:
            print(err)
        return False

    def check_ports(self, ports:list, region: str, provider_addr: str):
        temp = self.cli.node_host
        self.cli.node_host = provider_addr
        route = API_VERSION + '/k8s/checkports'
        data = {
            "region": region,
            "ports": ports
        }
        resp = self.cli.post_request(route, body_data=data)
        self.cli.node_host = temp
        ServiceCommon.validate_response(resp)
        return resp

    def start_usr_service(self, config:dict, route: str, secret: str) -> bool:
        temp = self.cli.node_host
        self.cli.node_host = ""
        headers = {
            "secret": secret
        }
        resp = self.cli.post_request(route, body_data=config, headers=headers, raw_res=True)
        self.cli.node_host = temp
        return resp.status_code == 200

    def service_status(self, provider_addr: str, secret: str):
        temp = self.cli.node_host
        self.cli.node_host = provider_addr
        route = API_VERSION + '/k8s/pod/status'
        headers = {
            "secret": secret
        }
        resp = self.cli.get_request(route, headers=headers)
        self.cli.node_host = temp
        ServiceCommon.validate_response(resp)
        return resp
