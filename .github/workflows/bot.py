import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from collections import Counter

BOT_TOKEN = os.getenv("8056021654:AAHWp2QZvM2LuAUeY_lHi3DmVlrRLcVdCMY")
if not BOT_TOKEN:
    raise ValueError("请在平台环境变量中设置 BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **TRC20地址重复核对机器人** 已重置\n\n"
        "直接发送地址列表即可检查重复（支持换行或逗号分隔）。\n"
        "示例：\nTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nTyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    )

async def check_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    addresses = [addr.strip().upper() for line in text.splitlines() for addr in line.split(',') 
                 if addr.strip().startswith('T') and len(addr.strip()) == 34 and addr.strip().isalnum()]
    
    if not addresses:
        await update.message.reply_text("❌ 未找到有效TRC20地址（T + 34位）。")
        return
    
    count = Counter(addresses)
    duplicates = {addr: cnt for addr, cnt in count.items() if cnt > 1}
    
    if duplicates:
        msg = f"✅ **发现 {len(duplicates)} 个重复地址：**\n\n"
        for addr, cnt in sorted(duplicates.items(), key=lambda x: -x[1]):
            msg += f"`{addr}` × **{cnt}**\n"
        msg += f"\n📊 总计 {len(addresses)} 个地址 | 唯一 {len(count)} 个"
    else:
        msg = f"✅ **无重复！** 共处理 **{len(addresses)}** 个地址。"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_duplicates))
    app.run_polling()

if __name__ == '__main__':
    main()
