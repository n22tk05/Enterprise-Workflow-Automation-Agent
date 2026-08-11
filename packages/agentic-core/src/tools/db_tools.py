from langchain_core.tools import tool
from prisma import Prisma
from datetime import datetime
import json

@tool
async def get_employee_profile(employee_code: str) -> str:
    """
    Search for employee profile information.
    Args:
        employee_code: The unique code of the employee (e.g., NV001)
    """
    db = Prisma()
    await db.connect()
    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    await db.disconnect()
    
    if not employee:
        return json.dumps({"error": "Employee not found"})
    return employee.model_dump_json()

@tool
async def check_leave_balance(employee_code: str) -> str: 
    """
    Check the remaining leave balance and leave history of an employee.
    Args:
        employee_code: The unique code of the employee
    """
    db = Prisma()
    await db.connect()

    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    if not employee:
        await db.disconnect()
        return json.dumps({"error": "Employee not found"})

    leave_info = await db.leaverequest.find_many(where={'employeeId': employee.id})
    await db.disconnect()
    
    result = {
        "leaveBalance": employee.leaveBalance,
        "history": [req.model_dump() for req in leave_info]
    }
    return json.dumps(result, default=str)

@tool
async def submit_leave_request(employee_code: str, start_date: str, end_date: str, reason: str) -> dict:
    """
    Create and submit a leave request for an employee.
    Args:
        employee_code: The unique code of the employee
        start_date: Start date of the leave (Format: YYYY-MM-DDTHH:MM:SS)
        end_date: End date of the leave (Format: YYYY-MM-DDTHH:MM:SS)
        reason: Reason for taking leave
    """
    db = Prisma()
    await db.connect()

    try:
        # Process and normalize dates
        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        total_days = (end_dt - start_dt).days + 1
        
        employee = await db.employee.find_unique(where={'employeeCode': employee_code})
        if not employee:
            return {"error": "Employee not found"}

        if employee.leaveBalance < total_days:
            return {"error": f"Insufficient leave balance. You only have {employee.leaveBalance} days remaining."}

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
        
        return {'message': f'Leave request submitted successfully. Deducted {total_days} leave days.'}
    
    finally:
        await db.disconnect() # Đảm bảo luôn ngắt kết nối database dù có lỗi xảy ra
        
@tool
async def create_it_ticket(employee_code: str, issue: str, priority: str) -> str: 
    """
    Receive a bug report, hardware fix request, or IT issue, automatically assess its severity, and save it to the database as an IT Ticket.
    Args:
        employee_code: The unique code of the employee reporting the issue
        issue: Description of the issue or bug
        priority: Priority level of the issue (Must be one of: HIGH, MEDIUM, LOW)
    """
    db = Prisma()
    await db.connect()

    employee = await db.employee.find_unique(where={'employeeCode': employee_code})
    if not employee:
        await db.disconnect()
        return json.dumps({'error': "Employee not found"})

    await db.ticket.create(data={
        'employeeId': employee.id,
        'issue': issue,
        'priority': priority
    })

    await db.disconnect()
    return json.dumps({'message': 'IT ticket created successfully'})

@tool
async def search_policy(keyword: str) -> str:
    """
    Search for company policies, rules, or regulations based on a keyword. Use this tool when employees ask about company rules (e.g., maternity leave, late arrival, dress code).
    Args:
        keyword: The keyword to search for (e.g., "maternity", "late", "wedding")
    """
    db = Prisma()
    await db.connect()

    policies = await db.policy.find_many(
        where={
            'rule': {
                'contains': keyword,
                'mode': 'insensitive'
            }
        }
    )
    await db.disconnect()

    if not policies:
        return json.dumps({'message': f'No company policies found containing the keyword: {keyword}'})

    rules = [p.rule for p in policies]
    return json.dumps({'found_policies': rules})

@tool
async def get_manager_report() -> str:
    """
    Generate an executive summary report for management. 
    Retrieves all pending leave requests and unresolved (OPEN) IT tickets. Use this tool when a manager asks for a status report.
    """
    db = Prisma()
    await db.connect()

    leave_report = await db.leaverequest.find_many(
        where={
            'status': "PENDING"
        },
        include={
            'employee': True,
        }
    )

    ticket_report = await db.ticket.find_many(
        where={
            'status': 'OPEN'
        },
        include={
            'employee': True
        }
    )
    
    await db.disconnect()

    result = {
        'Pending_Leave_Requests': [req.model_dump() for req in leave_report] if leave_report else "All leave requests have been processed",
        'Open_IT_Tickets': [ticket.model_dump() for ticket in ticket_report] if ticket_report else "No pending IT issues"
    }

    return json.dumps(result, default=str)