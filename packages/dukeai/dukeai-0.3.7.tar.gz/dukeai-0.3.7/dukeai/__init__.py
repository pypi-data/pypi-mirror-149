from .auto.auto import rpa_auto, ralock_auto, duke_auto
from .ocr.ocr import duke_ocr
# from .rpa.rpa import upload_document
from .rpa_functions.ratecon_schema_check import check_rate_con_schema
from .rpa_functions.ratecon_data_check import check_rate_con_data
from .rpa_functions.get_ratecon_schemas import get_rate_confirmation_schema,  get_stops_schema, get_note_schema, get_dates_schema, get_entity_schema, get_reference_schema, get_purchase_order_schema
from .rpa_functions.text_clean import data_clean
from .rpa_functions.ratecon_mapping import ratecon_map
# from .bookeeping.bookeeping_categories import get_new_categoryInfo
# from .bookeeping.bookkeeping_apis import BookkeepingApi
from .config import img_ocr_function_arn, pdf_ocr_function_arn, rpa_auto_lambda_arn, ralock_auto_lambda_arn, duke_auto_lambda_arn, rpa_endpoint, bookkeeping_endpoint, version