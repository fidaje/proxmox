import logging
import os
import asyncio
import proxmox

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
try:
    AUTHORIZED_USER_IDs = [int(os.getenv(key)) for key in os.environ if key.startswith('AUTHORIZED_USER_ID')]
except ValueError:
    logger.error("One or more AUTHORIZED_USER_ID values in the .env file are not valid.")
    AUTHORIZED_USER_IDs = []
TELEGRAM_CT = os.getenv('TELEGRAM_CT')


def authorized_user(func):
    async def wrapper(update: Update, context) -> None:
        if update.message.chat_id in AUTHORIZED_USER_IDs:
            return await func(update, context)
        else:
            await update.message.reply_text("You are not authorized to use this bot.")
    return wrapper


@authorized_user
async def status_all(update: Update, context) -> None:
    try:
        res = await asyncio.to_thread(proxmox.list_all)
        await update.message.reply_text(res)
    except Exception as e:
        logger.error(f"Error occurred while fetching all status: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching status.\nServer may be offline or there might be an issue with the Proxmox API.")

@authorized_user
async def status_containers(update: Update, context) -> None:
    try:
        res = await asyncio.to_thread(proxmox.list_containers)
        await update.message.reply_text(res)
    except Exception as e:
        logger.error(f"Error occurred while fetching container status: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching container status.")

@authorized_user
async def status_vms(update: Update, context) -> None:
    try:
        res = await asyncio.to_thread(proxmox.list_vms)
        await update.message.reply_text(res)
    except Exception as e:
        logger.error(f"Error occurred while fetching VM status: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching VM status.")


@authorized_user
async def summary(update: Update, context) -> None:
    try:
        res = await asyncio.to_thread(proxmox.summary)
        await update.message.reply_text(res)
    except Exception as e:
        logger.error(f"Error occurred while fetching system information: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching system information.")

@authorized_user
async def change_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        vmid = ' '.join(context.args)
        if not vmid.isdigit():
            await update.message.reply_text("VMID must be a number")
            return
        
        if vmid == TELEGRAM_CT:
            await update.message.reply_text("You cannot change the status of this container.")
            return
        
        try:
            res = await asyncio.to_thread(proxmox.stop_or_start, int(vmid))
            await update.message.reply_text(f"Changing status of VMID: {vmid}\n{res}")
        except Exception as e:
            logger.error(f"Error occurred while changing status of VMID {vmid}: {e}")
            await update.message.reply_text("⚠️ An error occurred while changing the status.")
    else:
        await update.message.reply_text("Please specify a VMID to change its status.\nE.g. /change 101")


@authorized_user
async def shutdown_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = await asyncio.to_thread(proxmox.shutdown_system)
        await update.message.reply_text(res)
    except Exception as e:
        logger.error(f"Error occurred while shutting down the system: {e}")
        await update.message.reply_text("⚠️ An error occurred while shutting down the system.")


@authorized_user
async def help(update: Update, context) -> None:
    help_text = (
        "Available commands:\n"
        "/list - Show the status of all containers and virtual machines\n"
        "/containers - Show the status of containers\n"
        "/vms - Show the status of virtual machines\n"
        "/info - Show system information\n"
        "/change <vmid> - Change the status of the specified virtual machine or container\n"
        "/shutdown - Shut down the Proxmox host system\n"
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
    application.add_handler(CommandHandler("shutdown", shutdown_system))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", help))


    application.run_polling()



if __name__ == '__main__':
    main()
