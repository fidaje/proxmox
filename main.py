import logging
import os
import proxmox

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))
TELEGRAM_CT = os.getenv('TELEGRAM_CT')


def authorized_user(func):
    async def wrapper(update: Update, context) -> None:
        if update.message.chat_id == AUTHORIZED_USER_ID:
            return await func(update, context)
        else:
            await update.message.reply_text("You are not authorized to use this bot.")
    return wrapper


@authorized_user
async def status_all(update: Update, context) -> None:
    await update.message.reply_text(proxmox.list_all())

@authorized_user
async def status_containers(update: Update, context) -> None:
    await update.message.reply_text(proxmox.list_containers())

@authorized_user
async def status_vms(update: Update, context) -> None:
    await update.message.reply_text(proxmox.list_vms())


@authorized_user
async def summary(update: Update, context) -> None:
    await update.message.reply_text(proxmox.summary())


@authorized_user
async def change_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        vmid = ' '.join(context.args)
        if not vmid.isdigit():
            await update.message.reply_text("VMID must be a number")
        if int(vmid) == TELEGRAM_CT:
            await update.message.reply_text("You cannot change the status of this container.")
            return
        res = proxmox.stop_or_start(int(vmid))
        await update.message.reply_text(f"Changing status of VMID: {vmid}\n{res}")
    else:
        await update.message.reply_text("Please specify a VMID to change its status.")

@authorized_user
async def help(update: Update, context) -> None:
    help_text = (
        "Available commands:\n"
        "/list - Show the status of all containers and virtual machines\n"
        "/containers - Show the status of containers\n"
        "/vms - Show the status of virtual machines\n"
        "/info - Show system information\n"
        "/change <vmid> - Change the status of the specified virtual machine or container\n"
        "/help - Show this help message \n"
    )
    await update.message.reply_text(help_text)


def main() -> None:
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("list", status_all))
    application.add_handler(CommandHandler("containers", status_containers))
    application.add_handler(CommandHandler("vms", status_vms))
    application.add_handler(CommandHandler("info", summary))
    application.add_handler(CommandHandler("change", change_status))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", help))


    application.run_polling()




if __name__ == '__main__':
    main()
