import traceback
import requests
import json
from functools import wraps
from YOMLogger import YOMLogger
from YOMErrors import ApiResponseError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls)\
                .__call__(*args, **kwargs)
        return cls._instances[cls]

def job_info(f):
    @wraps(f)
    def job_info_decorator(self, *args, **kwargs):
        if not self.job_info:
            # create job info
            self.init_job_info()

        # 1.- Define subprocess info dictionary
        data = {
            "processName": f.__name__,
            "startDate": "",
            "endDate": "",
            "status": "",
            "detailedStatus": [],
            "error": "",
            "detailedErrors": [],
        }
        data = {
            "id": self.job_info["_id"],
            "processName": f.__name__,
            "status": "",
            "detailedStatus": [],
            "error": "",
            "detailedErrors": [],
        }
        try:
            #data["startDate"] = str(datetime.now())
            (status_details, errors_details) = f(self, *args, **kwargs)
            #data["endDate"] = str(datetime.now())
            data["status"] = "completed" if len(errors_details) == 0 else "error"
            data["detailedStatus"] = [{"statusCode":key, "quantity": status_details[key]} for key in status_details.keys()]
            data["error"] = "" if len(errors_details) == 0 else "ERROR"
            data["detailedErrors"] = errors_details
        except Exception as exception:
            self.logger.exception(f'Error in {f.__name__} function job_info_decorator: {str(exception)}')
            data["status"] = "error"
            data["detailedStatus"] = []
            data["error"] = type(exception).__name__
            data["detailedErrors"] = [{
                "name": type(exception).__name__,
                "message": str(exception),
                "stack": traceback.format_exc()
            }]
        self.logger.info('OUTPUT DATA DETAILS')
        self.logger.info(data)

        self.loader.update_job_info_subprocess(data)
    return job_info_decorator

class YOMAPI(metaclass=Singleton):
    def __init__(self, APIConfig):
        self.client_id = APIConfig.api_client_id
        self.client_secret = APIConfig.api_client_secret
        self.customer_id = APIConfig.api_customer_id
        self.domain = APIConfig.api_domain
        self.url = APIConfig.api_url
        self.origin = APIConfig.api_origin
        self.logger = YOMLogger(APIConfig.api_customer_name)
        self.url_v3 = APIConfig.api_url_v3

    
    def __build_session(self, token=None):
        if not token:
            token = self.get_token()
        origin = self.origin
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Origin': origin,
            'Authorization': 'Bearer ' + str(token),
        })
        return session

    
    def get_token(self):
        """
        Request a token from YOM API to realize and authentication.
        """
        origin, url = self.origin, self.url
        path = url + '/api/v2/auth/tokens/grant'
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Origin': origin
        })
        response = None
        try:
            response = session.post(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            if 'accessToken' in response:
                return response['accessToken']
            return None
        except Exception as error:
            msg_err = f'API Response: {str(response)} \n Error:{str(error)}'
            raise ApiResponseError(path, msg_err)

    # Importer

    def bulk_importer(self, model, batch, token):
        """
        Send data to importer, data must be a dictionary.
        """
        # Upload data
        path = f'{self.url}/api/v2/import/{model}/bulk'
        try:
            session = self.__build_session(token)
            response = session.post(path, json.dumps(batch))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Commerce Endpoints
    """
    def get_commerces_mapping(self, token=None, authorized=None):
        """
        Return all commerces from API
        """
        current_page = 0
        total_pages = float('inf')
        commerces = []

        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_commerces_mapping_page(page=current_page, limit=10000, token=token, authorized=authorized)
            commerces += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending commerce mapping query for page {}/{}'.format(current_page, total_pages))
        return commerces


    def get_commerce(self, commerce_id, token=None):
        """
        Function that get the commerce for the current user
        """
        path = f'{self.url}/api/v2/commerces/{commerce_id}'
        session = self.__build_session(token)
        try:
            response = session.get(path)
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))

    def get_commerces(self, token=None, input_params=None):
        current_page = 0
        total_pages = float('inf')
        commerces = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_commerces_page(page=current_page, limit=100, token=token, input_params=input_params)
            commerces += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending commerces query for page {}/{}'.format(current_page, total_pages))
        return commerces

    def update_bulk_commerces(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/commerces/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }

            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def create_bulk_commerces(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/commerces/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
            }
            response = session.post(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def update_bulk_commerce_metrics(self, batch, token):
        path = f'{self.url}/api/v2/commerce-metrics/bulk-upsert'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'customerId': self.customer_id
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def __get_commerces_mapping_page(self, page, limit, token, authorized):
        path = self.url + '/api/v2/commerces/mapping'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit,
                'field': 'contact.externalId'
            }
            if authorized:
                params['authorized'] = True
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))

    def __get_commerces_page(self, page, limit, token, input_params=None):
        path = self.url + '/api/v2/commerces'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit
            }
            if input_params:
                if 'updated_before_than' in input_params: params['updatedBeforeThan'] = input_params['updated_before_than']
                if 'active' in input_params and input_params['active']: params['active'] = 'true'
                if 'externalId' in input_params and input_params['externalId']: params['externalId'] = 'true'
            response = session.get(path, params=params)

            if response.status_code < 200 or response.status_code >= 299:
                self.logger.info(response._content)

            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))

    """
    Product Endpoints
    """
    def get_products_mapping(self, token=None):
        current_page = 0
        total_pages = float('inf')
        products = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_products_mapping_page(page=current_page, limit=100, token=token)
            products += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending products mapping query for page {}/{}'.format(current_page, total_pages))
        return products


    def get_products(self, token, input_params=None):
        current_page = 0
        total_pages = float('inf')
        products = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_products_page(page=current_page, limit=100, token=token, input_params=input_params)
            products += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending products query for page {}/{}'.format(current_page, total_pages))
        return products


    def update_bulk_products(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/products/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def __get_products_mapping_page(self, page, limit, token):
        path = self.url + '/api/v2/products/mapping'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit,
                'field': 'sku' 
            }
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def __get_products_page(self, page, limit, token, input_params=None):
        path = self.url + '/api/v2/products'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit
            }
            if input_params:
                if 'updated_before_than' in input_params: params['updatedBeforeThan'] = input_params['updated_before_than']
                if 'enabled' in input_params and input_params['enabled']: params['enabled'] = 'true'
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Promotions Endpoints
    """
    def update_bulk_promotions(self, batch, fields_not_to_be_updated, token, sync_job_id=None, from_integration=None):
        path = self.url + '/api/v2/promotions/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            if sync_job_id:
                body['syncJobId'] = sync_job_id
            if from_integration:
                body['fromIntegration'] = from_integration
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def bulk_clean_promotions(self, job_id, token=None, segment_id=None):
        path = self.url +f'/api/v2/promotions/delete-not-by-sync-job/{job_id}'
        self.logger.info('Sending promotions delete for job id {}'.format(job_id))

        try:
            session = self.__build_session(token)
            if segment_id:
                path += f'?segmentId={segment_id}'

            response = session.delete(path)
            self.logger.info((response.status_code, response.json()))
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Overrides Endpoints
    """
    def update_bulk_overrides(self, batch, fields_not_to_be_updated, token, sync_job_id=None, from_integration=None):
        path = self.url + '/api/v2/segments/overrides/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            if sync_job_id is not None:
                body['syncJobId'] = sync_job_id
            if from_integration is not None:
                body['fromIntegration'] = from_integration

            response = session.put(path, json.dumps(body))
            print(response)
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))

    
    def update_bulk_overrides_by_segment(self, segment_id, batch, fields_not_to_be_updated, token):
        path = self.url + f'/api/v2/segments/{segment_id}/overrides/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def bulk_clean_overrides(self, job_id, token=None, segment_id=None):
        path = self.url + f'/api/v2/segments/overrides/delete-not-by-sync-job/{job_id}'
        self.logger.info('Sending overrides delete for job id {}'.format(job_id))
        try:
            session = self.__build_session(token)
            if segment_id:
                path += f'?segmentId={segment_id}'
            response = session.delete(path)
            self.logger.info((response.status_code, response.json()))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))

    
    """
    Segments Endpoints
    """
    def get_segments(self, query, token=None):
        path = self.url + '/api/v2/segments'
        session = self.__build_session(token)
        try:
            response = session.get(path, params=query)
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def get_segments_mapping(self, token=None, fields='name priority'):
        current_page = 0
        total_pages = float('inf')
        segments = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_segments_mapping_page(fields=fields, token=token, page=current_page, limit=10000)
            segments += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending segments mapping query for page {}/{}'.format(current_page, total_pages))
        return segments


    def update_bulk_segments(
        self,
        batch,
        fields_not_to_be_updated,
        token,
        sync_job_id=None,
        from_integration=None,
        filter_keys=None
    ):
        path = self.url + '/api/v2/segments/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            if sync_job_id:
                body['syncJobId'] = sync_job_id
            if from_integration:
                body['fromIntegration'] = from_integration
            if filter_keys:
                body['filterKeys'] = filter_keys

            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def get_user_segments_mapping(self, token=None, fields='segmentId commerceId'):
        current_page = 0
        total_pages = float('inf')
        segments = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_user_segments_mapping_page(
                fields=fields,
                token=token,
                page=current_page,
                limit=10000,
            )
            segments += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending user segments mapping query for page {}/{}'.format(current_page, total_pages))
        return segments


    def update_bulk_user_segments(
        self,
        batch,
        fields_not_to_be_updated,
        token,
        sync_job_id=None,
        from_integration=None,
        filter_keys=None
    ):
        path = self.url + '/api/v2/segments/user-segments/bulk'
        session = self.__build_session(token)

        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            if sync_job_id:
                body['syncJobId'] = sync_job_id
            if from_integration:
                body['fromIntegration'] = from_integration
            if filter_keys:
                body['filterKeys'] = filter_keys
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def create_segment(self, external_id, priority, token, from_integration):
        path = self.url + '/api/v2/segments'
        session = self.__build_session(token)

        try:
            body = {
                'name': external_id,
                'externalId': external_id,
                'priority': priority,
            }
            if from_integration:
                body['fromIntegration'] = from_integration
            response = session.post(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def bulk_clean_segments(self, job_id, token=None):
        path = self.url + f'/api/v2/segments/segments/delete-not-by-sync-job/{job_id}'
        self.logger.info('Sending segments delete for job id {}'.format(job_id))
        try:
            session = self.__build_session(token)
            response = session.delete(path)
            self.logger.info((response.status_code, response.json()))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def bulk_clean_user_segments(self, job_id, token=None):
        path = self.url + f'/api/v2/segments/user-segments/delete-not-by-sync-job/{job_id}'
        self.logger.info('Sending user segments delete for job id {}'.format(job_id))
        try:
            session = self.__build_session(token)
            response = session.delete(path)
            self.logger.info((response.status_code, response.json()))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def add_commerce_to_segment(self, commerce_id, segment_id, token=None):
        path = f'{self.url}/api/v2/segments/{segment_id}/add'
        session = self.__build_session(token)

        try:
            body = {
                'commerceId': commerce_id,
            }
            response = session.put(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def get_user_segment_by_commerce(self, commerce_id, token=None):
        path = f'{self.url}/api/v2/segments/user-segments/commerce/{commerce_id}'
        session = self.__build_session(token)

        try:
            response = session.get(path)
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def delete_segment(self, segment_id, token=None):
        path = f'{self.url}/api/v2/segments/{segment_id}'
        session = self.__build_session(token)
        try:
            response = session.delete(path)
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def __get_segments_mapping_page(self, fields, token, page, limit=10000):
        path = self.url + '/api/v2/segments/mapping'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit,
                'field': fields
            }
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def __get_user_segments_mapping_page(self, fields, token, page=0, limit=10000):
        path = self.url + '/api/v2/segments/user-segments/mapping'
        session = self.__build_session(token)

        try:
            params = {
                'page': page,
                'limit': limit,
                'field': fields
            }
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Seller Endpoints
    """
    def update_bulk_sellers(self, batch, fields_not_to_be_updated, token):
        path = self.url + '/api/v2/sellers/bulk'
        session = self.__build_session(token)

        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Supervisor Endpoints
    """
    def update_bulk_supervisors(self, batch, token):
        path = self.url + '/api/v2/supervisors/bulk'
        session = self.__build_session(token)

        try:
            body = {
                'data': batch,
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Routes Endpoints
    """
    def update_bulk_routes(self, data, token=None):
        path = f'{self.url_v3}/api/v3/admin/salesman/routes/bulk'
        session = self.__build_session(token)
    
        try:
            body = {
                'data': data
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Tasks Endpoints
    """
    def update_task(self, status, task_id, count_response=None, error=None):
        path = f'{self.url}/api/v2/task/{task_id}/b2b-loader-task'
        session = self.__build_session()

        try:
            body = {
                'status': status,
                'error': error,
                'count_response': count_response,
            }
            response = session.put(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))
        

    """
    Pending Documents Endpoints
    """
    def update_bulk_pending_documents(self, batch, token, filter_keys=None):
        path = f'{self.url}/api/v2/pending-documents/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
            }
            if filter_keys:
                body['filterKeys'] = filter_keys
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def delete_bulk_pending_documents(self, token):
        path = f'{self.url}/api/v2/pending-documents/bulk-delete'
        session = self.__build_session(token)
        try:
            response = session.delete(path)
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))
        

    """
    Shopping Lists Endpoints
    """
    def update_bulk_shopping_lists(self, batch, token):
        path = f'{self.url}/api/v2/shopping-lists/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Stock Endpoints
    """
    def get_distribution_centers(self, token, page=0, limit=1000):
        path = f'{self.url_v3}/api/v3/admin/catalog/distribution-center'
        session = self.__build_session(token)

        try:
            params = {
                'page': page,
                'limit': limit,
            }
            response = session.get(path, params=params)
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))

    
    def create_distribution_center(self, name, external_id, token):
        path = f'{self.url_v3}/api/v3/admin/catalog/distribution-center'
        session = self.__build_session(token)

        try:
            body = {
                'name': name,
                'externalId': external_id,
            }
            response = session.post(path, json.dumps(body))
            response = json.loads(response.content.decode('utf-8'))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def update_bulk_commerce_distribution_centers(self, batch, token):
        path = f'{self.url_v3}/api/v3/admin/catalog/commerce-distribution-center/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    def update_bulk_stock(self, batch, token):
        path = f'{self.url_v3}/api/v3/admin/catalog/stock/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
            }
            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))


    """
    Orders Endpoint
    """
    def get_orders(self, query):
        currentPage = 0
        totalPages = float('inf')
        orders = []
        while(currentPage < totalPages):
            currentPage += 1
            status, response = self.__getOrdersPage(page=currentPage, limit=100, query=query)
            orders += response['docs']
            totalPages = response['pages']
            self.logger.info('Sending orders query for page {}/{}'.format(currentPage, totalPages))
        return orders


    def send_order_to_erp(self, order_id, token=None):
        origin, url = self.origin, self.url
        path = url + f'/api/v2/orders/admin/{order_id}/integration'

        session = self.__build_session(token)
        headers = {
            'Content-Type': 'application/json',
            'Origin': origin,
            'Authorization': f'Bearer {token}'
        }
                
        response = session.put(path, headers=headers)
        self.logger.info('Sending order {} to ERP with status: {}'.format(order_id, response.status_code))
        return (response.status_code, response.json())


    def __getOrdersPage(self, page, limit, query=None, token=None):
        origin, url = self.origin, self.url
        path = url + '/api/v2/orders/admin'

        session = self.__build_session(token)
        headers = {
            'Content-Type': 'application/json',
            'Origin': origin,
            'Authorization': f'Bearer {token}'
        }
        params = {
            'page': page,
            'limit': limit
        }
        try:
            if query['status']:
                params['status'] = query['status']
            if query['createdFrom']:
                params['createdFrom'] = query['createdFrom']
        except Exception as err:
            pass
        
        response = session.get(path, params=params, headers=headers)
        return (response.status_code, response.json())


    """
    Documents Endpoints
    """
    def update_bulk_documents(self, batch, fields_not_to_be_updated, token):
        path = self.url_v3 + '/api/v3/admin/payments/payment-document/bulk'
        session = self.__build_session(token)
        try:
            body = {
                'data': batch,
                'fieldsNotToBeUpdated': fields_not_to_be_updated
            }

            response = session.put(path, json.dumps(body))
            return response
        except Exception as error:
            raise ApiResponseError(path, str(error))

            
    """
    Categories Endpoints
    """

    def __get_categories_page(self, page, limit, token, input_params=None):
        path = self.url + '/api/v2/categories/admin'
        session = self.__build_session(token)
        try:
            params = {
                'page': page,
                'limit': limit,
                'parent': 'all'
            }
            if input_params:
                if 'parent' in input_params: params['parent'] = input_params['parent']
            response = session.get(path, params=params)
            return (response.status_code, response.json())
        except Exception as error:
            raise ApiResponseError(path, str(error))

    def get_categories(self, token, input_params=None):
        current_page = 0
        total_pages = float('inf')
        products = []
        while(current_page < total_pages):
            current_page += 1
            status, response = self.__get_categories_page(page=current_page, limit=100, token=token, input_params=input_params)
            products += response['docs']
            total_pages = response['pages']
            self.logger.info('Sending categories query for page {}/{}'.format(current_page, total_pages))
        return products

    """
    Integration Job info endpoints
    """
    def create_job_info(self, data, token):
        path = self.url_v3 + '/api/v3/admin/data-import/integration-job-info/'
        session = self.__build_session(token)
        try:
            response = session.post(path, json.dumps(data))
            self.logger.info(f'Create Job Info Message: {data["message"]} Status Code: {response.status_code}')
            jsonResponse = response.json()
        except Exception as error:
            raise ApiResponseError(path, str(error))
        return jsonResponse


    """
    Integration Job info endpoints
    """
    def end_job_info(self, data, token):
        id = data["id"]
        path = self.url_v3 + f'/api/v3/admin/data-import/integration-job-info/{id}'
        session = self.__build_session(token)
        try:
            response = session.put(path, json.dumps(data))
            self.logger.info(f'End Job Info Message: {data["message"]} Status Code: {response.status_code}')
            jsonResponse = response.json()
        except Exception as error:
            raise ApiResponseError(path, str(error))
        return jsonResponse


    """
    Integration Job info endpoints
    """
    def update_job_info_subprocess(self, data, token):        
        id = data["id"]
        path = self.url_v3 + f'/api/v3/admin/data-import/integration-job-info/{id}/subprocess'
        session = self.__build_session(token)
        try:
            response = session.put(path, json.dumps(data))
            self.logger.info(f'Update Job Info Subprocess: {data["processName"]} Status Code: {response.status_code}')            
            if response.status_code < 200 or response.status_code >= 299:
                self.logger.info(response._content)
            jsonResponse = response.json()
        except Exception as error:
            raise ApiResponseError(path, str(error))
        return jsonResponse        

        
