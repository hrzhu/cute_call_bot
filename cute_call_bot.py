from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultPhoto
from telegram.ext.dispatcher import run_async

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from uuid import uuid4
from glob import glob
import logging

from config import token, url

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

updater = Updater(token=token)
dispatcher = updater.dispatcher


@run_async
def cute_call(bot, update):
    query = update.inline_query.query

    if not query:
        return

    results = list()

    for img in map(Image.open, sorted(glob('*.jpg'))):
        _id = uuid4().hex

        font_file = 'NotoSansCJK-Regular.ttc'

        img_size = img.size
        font_size = int(img_size[1]/6)
        font = ImageFont.truetype(font_file, font_size)
        text_size = font.getsize(query)

        while text_size[0] > img_size[0]*0.98:
            font_size = font_size - 1
            font = ImageFont.truetype(font_file, font_size)
            text_size = font.getsize(query)

        text_position_x = img_size[0]/2 - text_size[0]/2
        text_position_y = img_size[1]*310/512 + (img_size[1] - img_size[1]*310/512 - text_size[1])/2
        text_position = (text_position_x, text_position_y)

        draw = ImageDraw.Draw(img)
        draw.text(text_position, query, (0, 0, 0), font=font)
        img.save('./memes/'+ _id + '.jpg')

        img.thumbnail((128,128), Image.ANTIALIAS)
        img.save('./memes/' + _id + '_thumbnail' + '.jpg')

        img_url = url + _id + '.jpg'
        thumb_url = url + _id + '_thumbnail' + '.jpg'

        results.append(
            InlineQueryResultPhoto(
                id=_id,
                photo_width=img_size[0],
                photo_height=img_size[1],
                photo_url=img_url,
                thumb_url=thumb_url
            )
        )

    bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(cute_call)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()
updater.idle()
