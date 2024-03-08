# Add wallet address to db and display wallet provider and address
# MetaMask: 0x6382eaC3afAe5CF947f27FA8dEc6E6b867b9404f
# Leather STX: SP34XE6SE6WKPV9AZF4G2SY6NYHZC8R0DBN3ES1EE
# Leather BTC: bc1qdwhu03nnfcyx8ztdk2xv6xa4zlsap0rsv6stz3

"""
{
    "users": [
        {
            "email": "bob@mail.com",
            "full name": Bob Charles,
            "username": bob
            "password": "password",
            "image_url": "image",
            "balance": 5093.90,
            "account number": 9993 0003 9381 3950,
            "transaction": [
                {
                    amount: 894.90,
                    reciever: "bank user",
                    time: datetime
                }
            ]
        }
    ]
    
    "wallet_address": {
        "Bob Charles": 5939 3912 2929 5533,
    }
}
"""


def user_info(users, username):
    for user in users:
        if user["username"] == username:
            return user