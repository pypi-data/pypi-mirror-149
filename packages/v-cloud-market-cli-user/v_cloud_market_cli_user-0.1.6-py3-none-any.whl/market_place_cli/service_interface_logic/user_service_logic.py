import datetime
import json
import threading

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress


from market_place_cli.v_cloud_market_cli_common.service.wallet_service import WalletService, WalletCipher
from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.v_cloud_market_cli_common.service_display.user_service_display import UserServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.market_service_display import MarketServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service.user_service import UserService
from market_place_cli.v_cloud_market_cli_common.service.market_service import MarketService
from market_place_cli.service_interface_request.wallet_service_request import WalletRequest
from market_place_cli.service_interface_request.user_service_request import UserServiceRequest
from market_place_cli.service_interface_request.common_request import get_table_choice
from market_place_cli.service_interface_logic.common import get_net, wallet_has_password
from market_place_cli.v_cloud_market_cli_common.utils.message_decipher import decrypt_message
from market_place_cli.v_cloud_market_cli_common.utils.server_stream import ServerStream

from utils.string_utils import get_container_memory


class UserServiceLogic:

    def __init__(self):
        self.title = 'UserService'
        self.console = None
        self.ur = None  # User Request
        self.ud = None  # User Display
        self.net_type = 'M'
        self.main_functions = ['Show Running User Service', 'Show Usable User Service', 'Show Past User Service', 'Show Abort User Service']
        self.interface_index = 0 
        self.stream = ServerStream()
        self.password = None
        self.wr = None


    @property
    def Name(self):
        return self.title

    def StartLogic(self, console: Console, isTestnet: bool):
        self.console = console
        self.wr = WalletRequest(self.console)
        self.net_type = get_net(isTestnet)
        self.ur = UserServiceRequest(self.console)
        self.ud = UserServiceDisplay(self.console)
        console.clear()
        while True:
            choice = MainInterface.display_service_choice(console, self.title, self.main_functions, True)
            if choice == '1':
                self.interface_index = 1
                self.show_current_user_service_logic()
            elif choice == '2':
                self.interface_index = 2
                self.show_usable_user_service_logic()
            elif choice == '3':
                self.interface_index = 3
                self.show_past_user_service_logic()
            elif choice == '4':
                self.interface_index = 4
                self.show_abort_user_service_logic()
            elif choice.lower() == 'b':
                break
            self.interface_index = 0

    def show_current_user_service_logic(self):
        self.show_user_service_page("ServiceRunning")

    def show_usable_user_service_logic(self):
        self.show_user_service_page("ServiceUsable")

    def show_past_user_service_logic(self):
        self.show_user_service_page("ServiceDone")

    def show_abort_user_service_logic(self):
        self.show_user_service_page("ServiceAbort")

    def access_provider_api_logic(self, us: UserService, user_service_info: dict, index: int):
        try:
            # get decryption private key
            private_key = WalletService(None, self.net_type, self.password).fetch_wallet_info(index, "priv")

            # get provider host
            ms = MarketService(self.net_type, password, index)
            provider_host = ms.get_provider_host(user_service_info["provider"])

            info = us.get_user_service_info(provider_host, user_service_info["id"])
            magic = info["magic"]
            cipher = decrypt_message(private_key, magic)
            p = Panel.fit(cipher)
            p.title = "Service Login Information"
            p.title_align = "center"
            self.console.print(p)
            self.console.input("Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("[bright_red]Failed to get userservice info. Press ENTER to continue...")

    # To-Do: refactor function 
    def access_user_service_api_logic(self, us: UserService, user_service_info: dict, index: int):
        md = MarketServiceDisplay(self.console)
        ms = MarketService(self.net_type, password, index)
        service_info = ms.get_service_info(user_service_info['serviceID'])
        self.console.print(md.form_service_api(service_info['serviceAPI']))
        is_secret, api_func = self.ur.get_api_func(service_info['serviceAPI'])
        if is_secret:
            msg = us.access_user_api_get(user_service_id, 'secret', api_func)
        else:
            msg = us.access_user_api_get(user_service_id, 'normal', api_func)
        p = Panel.fit(msg)
        p.title = '[]User Service API Service Response'
        p.title_align = 'center'
        self.console.print(p)
        self.console.input("Press ENTER to continue...")

    def start_user_service_api_logic(self, us: UserService, order_info: dict, index: int):

        if order_info["serviceStatus"] != "ServicePending":
            self.console.print(f"Order service status is { order_info['status'] }, and cannot start service.")
            self.console.input("Press ENTER to continue...")
            return
        # get provider host
        full_user_service_info = self._get_us_info_with_secret(us, order_info, index)
        if full_user_service_info is None or "Secret" not in full_user_service_info:
            self.console.print(f"[bright_green]Order {full_user_service_info['id']} has invalid magic!")
            self.console.input("Press ENTER to continue...")
            return

        image_name = self.ur.get_image_info(us.check_image)
        # get container and host post persistStorage
        serviceOptions = full_user_service_info["serviceOptions"]
        port_configs = self.ur.get_ports(serviceOptions, full_user_service_info["provider_host"], us.check_ports)
        memory = get_container_memory(serviceOptions["resourceUnit"])
        container_config = {
            "name": "container-0",
            "imageName": image_name,
            "ports": port_configs,
            "resource": {
                "memory": memory
            }
        }
        if "persistStorage" in serviceOptions and serviceOptions["persistStorage"] == "yes":
            container_config["mountPath"] = self.ur.get_mount_path()
        cmd = self.console.input("Please input command(optional) : ")
        if len(cmd.replace(" ", "")) > 0:
            container_config["command"] = cmd
        args = self.console.input("Please input arguments to (optional) : ")
        if len(args) != 0:
            container_config["args"] = args
        service_config = {
            "name": order_info["id"],
            "containers": [container_config]
        }
        try:
            if not us.start_usr_service(service_config, full_user_service_info["Ip"], full_user_service_info["Secret"]):
                self.console.print(f"[bright_red]Failed to start service { order_info['id'] }")
            else:
                self.console.print(f"[bright_green]Order { order_info['id'] } user service has been deployed successfully!")
        except Exception as e:
            print(e)
            self.console.print(f"[bright_red]Failed to start service { order_info['id'] }")
        self.console.input("Press ENTER to continue...")

    def tail_service_log_logic(self, us: UserService, order_info: dict, index: int):
        user_service_info = self._get_us_info_with_secret(us, order_info, index)
        if user_service_info is None or "Secret" not in user_service_info:
            self.console.print(f"[bright_green]Order {order_info['id']} has invalid magic!")
            self.console.input("Press ENTER to continue...")
            return
        url = user_service_info["provider_host"] + "/api/v1/k8s/pod/logs"
        headers = {
            "Connection": "close",
            "secret": user_service_info["Secret"]
        }
        self.console.clear()
        self.console.print("[bright_green]Press ENTER to stop log...")
        log_thread = threading.Thread(target=self.stream.open, args=(url, headers, None, self.read_stream))
        log_thread.daemon = True
        log_thread.start()
        self.console.input("")
        # close stream
        self.stream.close()

    def monitor_services(self, us: UserService, orders: list, index: int):
        status_list = []
        with Progress() as progress:
            task = progress.add_task("[green]Querying data...", total=len(orders) * 2, start=False)
            progress.start_task(task)
            try:
                for order in orders:
                    if order["serviceStatus"] != "ServiceRunning":
                        continue
                    user_service = self._get_us_info_with_secret(us, order, index)
                    progress.update(task, advance=1)
                    if user_service is None:
                        continue
                    status_data = us.service_status(user_service["provider_host"], user_service["Secret"])
                    progress.update(task, advance=1)
                    if status_data is None:
                        continue
                    item = {
                        "id": order["id"],
                        "region": order["serviceOptions"]["region"]
                    }
                    if "podStatus" in status_data and "containerStatuses" in status_data["podStatus"]:
                        container_status = status_data["podStatus"]["containerStatuses"][0]
                        item["image"] = container_status["image"]
                        state = list(container_status["state"].keys())
                        item["state"] = state[0]
                        item["restartCount"] = container_status["restartCount"]
                        item["hostIP"] = status_data["podStatus"]["hostIP"]

                    if "podSpec" in status_data and "containers" in status_data["podSpec"]:
                        # only one container in each pod
                        container = status_data["podSpec"]["containers"][0]
                        if "ports" in container:
                            item["ports"] = container["ports"]
                    if "oomNotice" in status_data and "history" in status_data["oomNotice"]:
                        item['oomHistory'] = []
                        for timestamp in status_data["oomNotice"]["history"]:
                            local_time = datetime.datetime.fromtimestamp(timestamp)
                            item['oomHistory'].append(str(local_time))
                    status_list.append(item)
            except Exception as e:
                print(e)
                self.console.input("Press ENTER to continue...")
                return
        headers = [
            { "text": "Order ID", "value": "id"},
            { "text": "Region", "value": "region"},
            { "text": "Image", "value": "image"},
            { "text": "Container Status", "value": "state"},
            # { "text": "Restart Count", "value": "restartCount"},
            { "text": "Host IP", "value": "hostIP"},
            { "text": "Port Spec", "value": "ports", "justify": "left"},
            { "text": "Out of Memory History", "value": "oomHistory"},
        ]
        self.ud.display_service_status(headers, status_list)
        self.console.input("Press ENTER to continue...")

    def show_user_service_page(self, status: str):
        index = self.wr.get_payment_address()
        if wallet_has_password(self.net_type):
            self.password = self.wr.get_dec_password()

        us = UserService(self.net_type, self.password, index)
        cur = 1
        page_size = 10
        title, extra = self._construct_page_title(status)
        while True:
            try:
                display_result, has_next = self._construct_user_service_page(us, cur, status)
            except Exception as e:
                self.console.print(e)
                self.console.input("[bright_red]Failed to get userservice info. Press ENTER to continue...")
                break
            w = self.ud.show_user_service_page(title, display_result['list'])
            has_next = len(display_result['list']) >= page_size
            choice = get_table_choice(self.console, w, has_next, extra=extra)
            if choice == 'p' and cur > 1:
                cur -= 1
            elif choice == 'n' and has_next:
                cur += 1
            elif choice == 'e':
                break
            elif choice == 'd':
                user_service_id = self.ur.get_user_service_id()
                u, ok = self.validate_user_service(display_result, user_service_id)
                if ok:
                    self.ud.show_user_service_detail(u)
            elif status == 'ServiceUsable' and choice == 'u':
                user_service_id = self.ur.get_user_service_id()
                us_info, ok = self.validate_user_service(display_result, user_service_id)
                if ok:
                    self.access_provider_api_logic(us, us_info, index)
            elif status == 'ServiceUsable' and choice == 's':
                user_service_id = self.ur.get_user_service_id()
                us_info, ok = self.validate_user_service(display_result, user_service_id)
                if ok:
                    self.start_user_service_api_logic(us, us_info, index)
            elif choice == 'a':
                user_service_id = self.ur.get_user_service_id()
                us_info, ok = self.validate_user_service(display_result, user_service_id)
                if ok:
                    self.access_user_service_api_logic(us, us_info, index)
            elif self.interface_index == 1 and choice == 't':
                user_service_id = self.ur.get_user_service_id()
                us_info, ok = self.validate_user_service(display_result, user_service_id)
                if ok:
                    self.tail_service_log_logic(us, us_info, index)
            elif self.interface_index == 1 and choice == 'm':
                order_id = self.console.input('[bright_green]Please enter order id: ')
                temp_list = []
                for item in display_result["list"]:
                    if item["id"] == order_id:
                        temp_list.append(item)
                if len(temp_list) == 0:
                    temp_list = display_result["list"]
                self.monitor_services(us, temp_list, index)

    def validate_user_service(self, result: dict, user_service_id: str) -> (dict, bool):
        found = False
        for u in result['list']:
            if u['id'] == user_service_id:
                found = True
                return u, found
        if not found:
            self.console.input("[bright_red]User Service ID Not Found.[/] Press ENTER to continue...")
            return None, found

    def _construct_user_service_page(self, us: UserService, cur_page: int, status: str):
        if status == 'ServiceUsable':
            display_result = us.get_user_service_page(
                current=cur_page,
                page_size=10,
                statuses=['ServicePending', 'ServiceRunning'])
        else:
            display_result = us.get_user_service_page(
                current=cur_page,
                page_size=10,
                statuses=status)

        has_next = False if len(display_result['list']) < 10 else True
        return display_result, has_next

    def _construct_page_title(self, status: str):
        extra = {}
        title = 'User Service Information Table'
        if status == 'ServiceRunning':
            title = 'Running ' + title
            extra = {'d': '[D]User Service Detail', 'a': '[A]User Service API Access', 't': '[T]Tail Service Log', 'm': '[M]Monitor Service In Current Page'}
        elif status == 'ServiceUsable':
            title = 'Usable ' + title
            extra = {'d': '[D]User Service Detail', 'u': '[U]User Service Usage Info', 's': '[S]Start a service'}
        elif status == 'ServiceDone':
            title = 'Past ' + title
        return title, extra

    def _get_us_info_with_secret(self, us: UserService, order_info: dict, wallet_index: int) -> dict:
        # get decryption private key
        try:
            private_key = WalletService(None, self.net_type, self.password).fetch_wallet_info(wallet_index, "priv")
            ms = MarketService(self.net_type, self.password)
            provider_host = ms.get_provider_host(order_info['provider'])
            info = us.get_user_service_info(provider_host, order_info["id"])
            info["provider_host"] = provider_host
            plain_txt_magic = decrypt_message(private_key, info["magic"])
            magic_dict = json.loads(plain_txt_magic)
            return { **magic_dict, **info }
        except Exception as err:
            print(err)
            return None

    def read_stream(self, data):
        line = data.decode("utf-8")
        if line.startswith("data:"):
            line = line[5:]
        if line != "\"logger - Client disconnected.\"":
            self.console.print(line)
