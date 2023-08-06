from typing import Any

from eevend_libs.client.base_client import BaseClient

service_name = "eev-auth-service"


class AuthClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(service_name)

    def email_login(self, email: str, password: str, platform: str) -> Any:
        return self.post('email_login', email=email, password=password, platform=platform)

    def user_logout(self, login_token: str) -> Any:
        return self.get('logout/%s' % login_token)

    def add_user(self,
                 auth_user_email: str,
                 auth_user_password: str,
                 auth_user_type: str,
                 auth_user_name: str) -> Any:
        return self.post('add_user',
                         auth_user_email=auth_user_email,
                         auth_user_password=auth_user_password,
                         auth_user_type=auth_user_type,
                         auth_user_name=auth_user_name)

    def check_user_email(self,
                         auth_user_email: str,
                         auth_user_type: str,
                         password_reset: bool) -> Any:
        return self.get(f'check_user_email?'
                        f'auth_user_email={auth_user_email}&'
                        f'auth_user_type={auth_user_type}&'
                        f'password_reset={password_reset}')

    def check_link_token(self, auth_user_link_token: str) -> Any:
        return self.get(f'check_link_token?auth_user_link_token={auth_user_link_token}')

    def edit_user_password(self, auth_user_email: str, auth_user_password: str) -> Any:
        return self.put('edit_user_password', auth_user_email=auth_user_email, auth_user_password=auth_user_password)

    def edit_user_details(self, auth_user_id: int,
                          auth_user_email: str,
                          auth_user_name: str) -> Any:
        return self.put('edit_user_details',
                        auth_user_id=auth_user_id,
                        auth_user_email=auth_user_email,
                        auth_user_name=auth_user_name)

    def has_permission(self, user_login_token: str, permission: str) -> Any:
        return self.get(f'/permission/has_permission?'
                        f'user_login_token={user_login_token}&'
                        f'permission={permission}')


class AccountClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(service_name)

    def add_user_account(self,
                         user_id: id,
                         user_email: str,
                         user_first_name: str,
                         user_last_name: str,
                         user_phone_number: str,
                         user_type: str,
                         user_gender: str,
                         user_date_of_birth: str,
                         user_username: str,
                         user_profile_image_file_id: str,
                         seller_status_reason: str) -> Any:
        return self.post('user',
                         user_id=user_id,
                         user_email=user_email,
                         user_first_name=user_first_name,
                         user_last_name=user_last_name,
                         user_phone_number=user_phone_number,
                         user_type=user_type,
                         user_gender=user_gender,
                         user_date_of_birth=user_date_of_birth,
                         user_username=user_username,
                         user_profile_image_file_id=user_profile_image_file_id,
                         seller_status_reason=seller_status_reason)

    def get_user(self, user_id: int) -> Any:
        return self.get('user/%s' % user_id)

    def edit_user_account(self,
                          user_id: id,
                          user_email: str,
                          user_first_name: str,
                          user_last_name: str,
                          user_phone_number: str,
                          user_gender: str,
                          user_date_of_birth: str,
                          user_username: str,
                          user_profile_image_file_id: str,
                          seller_status: str,
                          seller_status_reason: str,
                          seller_account_balance: float = None) -> Any:
        return self.put('user',
                        user_id=user_id,
                        user_email=user_email,
                        user_first_name=user_first_name,
                        user_last_name=user_last_name,
                        user_phone_number=user_phone_number,
                        user_gender=user_gender,
                        user_date_of_birth=user_date_of_birth,
                        user_username=user_username,
                        user_profile_image_file_id=user_profile_image_file_id,
                        seller_status=seller_status,
                        seller_status_reason=seller_status_reason,
                        seller_account_balance=seller_account_balance)


class FileClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(service_name)

    def get_file(self, file_id: int) -> Any:
        return self.get('file/%s' % file_id)

    def get_files(self, file_ids: [int]) -> Any:
        return self.get('files', file_ids)

    def add_file(self,
                 file_reference: str,
                 file_title: str,
                 file_description: str,
                 file_path: str,
                 file_expiry_date: str) -> Any:
        return self.post('file',
                         file_reference=file_reference,
                         file_title=file_title,
                         file_description=file_description,
                         file_path=file_path,
                         file_expiry_date=file_expiry_date)

    def edit_file(self,
                  file_id: int,
                  file_reference: str,
                  file_title: str,
                  file_description: str,
                  file_path: str,
                  file_expiry_date: str) -> Any:
        return self.put('file/%s' % file_id,
                        file_id=file_id,
                        file_reference=file_reference,
                        file_title=file_title,
                        file_description=file_description,
                        file_path=file_path,
                        file_expiry_date=file_expiry_date)

    def delete_file(self, file_id: int):
        return self.delete('file/%s' % file_id)
