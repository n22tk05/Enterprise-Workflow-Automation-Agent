from langchain_core.tools import tool
from prisma import Prisma
from datetime import datetime
import json

@tool
async def get_employee_profile(employee_code: str) -> str:
    """
    Tìm kiếm thông tin hồ sơ nhân viên (Employee profile).
    Args:
        employee_code: Mã nhân viên (ví dụ NV001)
    """
    db = Prisma()
    await db.connect()
    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    await db.disconnect()
    
    if not employee:
        return json.dumps({"error": "Không tìm thấy nhân viên"})
    return employee.model_dump_json()

@tool
async def check_leave_balance(employee_code: str) -> str: 
    """
    Kiểm tra số ngày nghỉ phép còn lại của nhân viên và lịch sử xin phép.
    Args:
        employee_code: Mã nhân viên
    """
    db = Prisma()
    await db.connect()

    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    if not employee:
        await db.disconnect()
        return json.dumps({"error": "Không tìm thấy nhân viên"})

    leave_info = await db.leaverequest.find_many(where={'employeeId': employee.id})
    await db.disconnect()
    
    result = {
        "leaveBalance": employee.leaveBalance,
        "history": [req.model_dump() for req in leave_info]
    }
    return json.dumps(result, default=str)

@tool
async def submit_leave_request(employee_code: str, start_date: str, end_date: str, reason: str) -> str:
    """
    Tạo đơn xin nghỉ phép cho nhân viên.
    Args:
        employee_code: Mã nhân viên
        start_date: Ngày bắt đầu nghỉ (Format: YYYY-MM-DDTHH:MM:SS)
        end_date: Ngày kết thúc nghỉ (Format: YYYY-MM-DDTHH:MM:SS)
        reason: Lý do nghỉ phép
    """
    db = Prisma()
    await db.connect()

    # Xử lý ngày tháng chuẩn hoá
    start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    total_days = (end_dt - start_dt).days + 1
    
    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    if not employee:
        await db.disconnect()
        return json.dumps({"error": "Không tìm thấy nhân viên"})

    if employee.leaveBalance < total_days:
        await db.disconnect()
        return json.dumps({"error": f"Không đủ ngày phép. Bạn chỉ còn {employee.leaveBalance} ngày."})

    await db.leaverequest.create(data={
        'employeeId': employee.id,
        'startDate': start_dt,
        'endDate': end_dt,
        'reason': reason
    })
    
    await db.employee.update(
        where={'employeeCode': employee_code},
        data={'leaveBalance': employee.leaveBalance - total_days}
    )
    
    await db.disconnect()
    return json.dumps({'message': f'Gửi đơn thành công. Đã trừ {total_days} ngày phép.'})

@tool
async def create_it_ticker(request: str): 
    """
    Receive a bug fix request, automatically assess its severity, and save it to the database.
    Arg:
        
    """