import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove

from .core import Photo, Coordinates
from .filters import IsAdmin
from .keyboards import geo_request_kb


logger = logging.getLogger(__name__)

router = Router()
router.message.filter(IsAdmin())


class PhotoInfo(StatesGroup):
    coordinates = State()


@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer("Hi, you are an admin!")


@router.message(F.photo)
async def photo_handler(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    logger.info(f"Received photo: {photo_id} from {message.from_user.id}")

    file_path = (await message.bot.get_file(photo_id)).file_path
    input_photo = f"resources/photos/input/{photo_id}.jpg"
    await message.bot.download_file(file_path, input_photo)

    await state.update_data(photo=photo_id)
    await state.set_state(PhotoInfo.coordinates)
    await message.answer("Send me your location", reply_markup=geo_request_kb)


@router.message(F.location, PhotoInfo.coordinates)
async def coordinates_handler(message: Message, state: FSMContext):
    coordinates = Coordinates(message.location.latitude, message.location.longitude)
    logger.info(f"Received coordinates: {coordinates.latitude}, {coordinates.longitude} from {message.from_user.id}")

    photo_id = (await state.get_data()).get("photo")
    photo = Photo(photo_id, coordinates)
    output_photo = photo.save()
    logger.info(f"Generated photo {output_photo} with coordinates: {coordinates.latitude}, {coordinates.longitude}")

    await state.clear()
    await message.answer_photo(photo=FSInputFile(output_photo), reply_markup=ReplyKeyboardRemove())


@router.message(PhotoInfo.coordinates, F.text.lower().contains("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Operation cancelled", reply_markup=ReplyKeyboardRemove())
