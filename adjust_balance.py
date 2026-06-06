# 793235992458035201
import asyncio
import aiosqlite

DB_PATH = "economy.db"

USER_ID = 793235992458035201  # <-- paste the user ID here
AMOUNT = 2500  # <-- set the amount (negative to remove)


async def update_balance():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (AMOUNT, USER_ID)
        )
        await db.commit()
        print(f"Done. Added {AMOUNT} to user {USER_ID}.")


asyncio.run(update_balance())

