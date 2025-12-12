def analyze_data(data: object) -> str:
    match data:
        case int() | float() as num if num > 0:
            return f"Positive number: {num}"
        case str() as text if text.strip():
            return f"Non empty string: {text}"
        case list() | tuple() as seq if seq:
            return f"non empty sequence of length: {len(seq)}"
        case dict() as d if d:
            return f"dictionary with keys: {','.join(d.keys())}"
        case _ :
            return "unhandled data type or empty value"


#enhanced switch with pattern matching
def process_event(event: dict) -> str:
    match event:
        case {'type': 'user', 'action': 'login', 'id': id}:
            return f"User {id} logged in"
        case {'type': 'user', 'action': 'logout', 'id': id}:
            return f"User {id} logged out"
        case {'type': 'error', 'code': code, 'message': msg}:
            return f"Error {code} : {msg}"
        case {'type': 'system', **details}:
            return f"System event with details: {details}"
        case _ :
            return "unknown event"

analyze_result = analyze_data({'if': 'you'})
print(analyze_result)


event_result = process_event({'type': 'user', 'action': 'logout', 'id': 123})
print(event_result)

event_result = process_event({'type': 'error', 'code': '400', 'message':'failure'})
print(event_result)

event_result = process_event({'type':'system', 'position': 'its fine'})
print(event_result)



