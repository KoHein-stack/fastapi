from time import time

from fastapi import HTTPException, status


MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_LOCKOUT_SECONDS = 15 * 60

_login_attempts: dict[str, list[float]] = {}
_login_lockouts: dict[str, float] = {}


def _now() -> float:
    return time()


def check_login_rate_limit(identifier: str) -> None:
    current_time = _now()
    locked_until = _login_lockouts.get(identifier)

    if locked_until and locked_until > current_time:
        retry_after = int(locked_until - current_time)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
            headers={"Retry-After": str(retry_after)},
        )

    attempts = _login_attempts.get(identifier, [])
    _login_attempts[identifier] = [
        attempt_time
        for attempt_time in attempts
        if current_time - attempt_time < LOGIN_WINDOW_SECONDS
    ]


def record_failed_login(identifier: str) -> None:
    current_time = _now()
    attempts = _login_attempts.setdefault(identifier, [])
    attempts.append(current_time)

    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        _login_lockouts[identifier] = current_time + LOGIN_LOCKOUT_SECONDS
        _login_attempts[identifier] = []


def clear_login_rate_limit(identifier: str) -> None:
    _login_attempts.pop(identifier, None)
    _login_lockouts.pop(identifier, None)
