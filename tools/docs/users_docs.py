from dataclasses import dataclass

from types import UserOut, UserIn, BaseUser


@dataclass
class SwaggerUI:
    responses: dict[int, dict[str, dict | BaseUser]]

validate_user1_docs = dict(
    responses = {
        200: {
            "model": UserOut | UserIn,
            "description": "User response - UserOut for regular users, UserIn for admin users",
            "content": {
                "application/json": {
                    "examples": {
                        "regular_user": {
                            "value": {
                                "username": "john_doe",
                                "email": "john@example.com"
                            }
                        },
                        "admin_user": {
                            "value": {
                                "username": "admin",
                                "password": "admin123",
                                "email": "admin@example.com"
                            }
                        }
                    }
                }
            }
        },
        202: {
            "model": dict[str, int],
            "description": "Dictionary response"
        }
    }
)