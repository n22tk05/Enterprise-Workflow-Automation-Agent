from langchain_core.tools import tool
import json

@tool
def get_employee_profile(user_id: str) -> str:
    """
    Search employee_profile
    Arg:
        user_id: Id employee
    """
    print('\n[ERP GIẢ LẬP] Đang tìm kiếm nhân viên')
    print(f'    [Mã nhân viên]: {user_id}')
    print(f'    [Tên nhân viên]: Nguyễn Văn A')
    print(f'    [Phòng ban]: IT')
    print(f'    [Chức vụ]: Developer')
    print('\n[ERP GIẢ LẬP] Xử lý thành công')

    data = {"name": "Nguyễn Văn A", "department": "IT", "role": "Developer"}
    return json.dumps(data)

@tool
def check_leave_balance(user_id: str, leave_type: str) -> dict:
    """
    Check how many days of annual leave the employee has remaining.
    Arg: 
        user_id: Id employee
        leave_type: type of leave
    """

    print('\n[ERP GIẢ LẬP] Đang kiểm tra số lượng ngày nghỉ còn lại của nhân viên')
    print(f'    [Mã nhân viên]: {user_id}')
    print(f'    [Tên nhân viên]: Nguyễn Văn A')
    print(f'    [Loại nghỉ phép]: Phép ốm')
    print(f'    [Số ngày còn lại]: 5 ngày')
    print('\n[ERP GIẢ LẬP] Xử lý thành công')

    data = {"leave_type": leave_type, "remaining_days": 5}
    return json.dumps(data)

@tool
def create_leave_request(user_id:str,start_date: str ,days: int, reason: str) -> str:
    """
    Create a leave request in the system for the employee.
    Arg:
        user_id: Id employee
        start_date: start date of leave
        days: Number off leave days
        reason: Reason for leave
    """

    print('\n[ERP GIẢ LẬP] Đang tiếp nhận yêu cầu tạo đơn')
    print(f'    [Mã nhân viên]: {user_id}')
    print(f'    [Ngày nghỉ]: {start_date}')
    print(f'    [Số ngày nghỉ]: {days}')
    print(f'    [Lý do]: {reason}')
    print('\n[ERP GIẢ LẬP] Xử lý thành công')

    data = {'message': 'Đã tạo đơn thành công trên hệ thống. Mã đơn là #LEAVE-00001'}
    return json.dumps(data) 

@tool 
def search_company_policy(query: str) -> str:
    """
    Search the company's internal document repository
    Args:
        query: Search policy to look for
    """
    print('\n[ERP GIẢ LẬP] Đang tiếp nhận yêu cầu')
    print(f'    [Yêu cầu]: {query}')
    print('\n[ERP GIẢ LẬP] Xử lý thành công')

    data = {'message': "Theo quy định của công ty, nghỉ ốm trên 3 ngày yêu cầu phải có giấy khám bệnh xác nhận của bệnh viện cấp huyện trở lên."}
    return json.dumps(data)