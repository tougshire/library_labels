from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

from .forms import BarcodeForm, SSIDForm

from django.views.generic import FormView,CreateView,DetailView


def make_ssid_label(
            ssid_text,
            password_text,
            notice1_text,
            notice2_text,
            ssid_fontsize,
            ssid_fontfamily,
            password_fontsize,
            password_fontfamily,
            notice1_fontsize,
            notice1_fontfamily,
            notice2_fontsize,
            notice2_fontfamily,
):

        ssid_y=0
        img_height = ssid_fontsize + password_fontsize
        if notice1_text > "":
            img_height = img_height + notice1_fontsize
        if notice2_text > "":
            img_height = img_height + notice2_fontsize
        img_height = img_height + 10 

        init_img_width = 10000

        init_img = Image.new("RGB", (init_img_width, img_height),"#ffffff")

        init_draw = ImageDraw.Draw(init_img)


        try:
            font_ssid_text = ImageFont.truetype(ssid_fontfamily, size=ssid_fontsize)
        except IOError:
            font_ssid_text = ImageFont.load_default()

        bbox = init_draw.textbbox((0,0), ssid_text, font=font_ssid_text)
        ssid_width=bbox[2] - bbox[0]

        try:
            font_password_text = ImageFont.truetype(password_fontfamily, size=password_fontsize)
        except IOError:
            font_password_text = ImageFont.load_default()

        bbox = init_draw.textbbox((0,0), password_text, font=font_password_text)
        password_width=bbox[2] - bbox[0]

        if notice1_text > "":
            try:
                font_notice1_text = ImageFont.truetype(notice1_fontfamily, size=notice1_fontsize)
            except IOError:
                font_notice1_text = ImageFont.load_default()

            bbox = init_draw.textbbox((0,0), notice1_text, font=font_notice1_text)
            notice1_width=bbox[2] - bbox[0]
        else:
            notice1_width = 0

        if notice2_text > "":
            try:
                font_notice2_text = ImageFont.truetype(notice2_fontfamily, size=notice2_fontsize)
            except IOError:
                print("some kind of error with notice2_text=", notice2_text)
                font_notice2_text = ImageFont.load_default()

            bbox = init_draw.textbbox((0,0), notice2_text, font=font_notice2_text)
            notice2_width=bbox[2] - bbox[0]
        else:
            notice2_width = 0


        img_width = max(ssid_width, password_width, notice1_width, notice2_width)


##########

        img = Image.new("RGB", (img_width, img_height),"#ffffff")

        draw = ImageDraw.Draw(img)

        text_y = 0

        try:
            font_ssid_text = ImageFont.truetype(ssid_fontfamily, size=ssid_fontsize)
        except IOError:
            font_ssid_text = ImageFont.load_default()

        bbox = draw.textbbox((0,0), ssid_text, font=font_ssid_text)
        text_width=bbox[2] - bbox[0]

        text_x = (img_width - text_width) // 2

        draw.text((text_x, text_y ), ssid_text, fill="black", font=font_ssid_text, align="center")

        text_y = text_y + ssid_fontsize

        try:
            font_password_text = ImageFont.truetype(password_fontfamily, size=password_fontsize)
        except IOError:
            font_password_text = ImageFont.load_default()

        bbox = draw.textbbox((0,0), password_text, font=font_password_text)
        text_width=bbox[2] - bbox[0]

        text_x = (img_width - text_width) // 2

        draw.text((text_x, text_y ), password_text, fill="black", font=font_password_text, align="center")

        text_y = text_y + password_fontsize

        if notice1_text > "":

            try:
                font_notice1_text = ImageFont.truetype(notice1_fontfamily, size=notice1_fontsize)
            except IOError:
                font_notice1_text = ImageFont.load_default()

            bbox = draw.textbbox((0,0), notice1_text, font=font_notice1_text)
            text_width=bbox[2] - bbox[0]

            text_x = (img_width - text_width) // 2

            draw.text((text_x, text_y ), notice1_text, fill="black", font=font_notice1_text, align="center")

            text_y = text_y + notice1_fontsize

        if notice2_text > "":

            try:
                font_notice2_text = ImageFont.truetype(notice2_fontfamily, size=notice2_fontsize)
            except IOError:
                font_notice2_text = ImageFont.load_default()

            bbox = draw.textbbox((0,0), notice2_text, font=font_notice2_text)
            text_width=bbox[2] - bbox[0]

            text_x = (img_width - text_width) // 2

            print("***** Drawing at ", text_x, text_y, notice2_text)

            draw.text((text_x, text_y ), notice2_text, fill="black", font=font_notice2_text, align="center")

            text_y = text_y + notice2_fontsize

        byio = BytesIO()
        img.save(byio, format="jpeg")
        img_data=byio.getvalue()

        return(img_data)

def make_barcode_label(
            barcode_number,
            show_barcode_number,
            show_startstop,
            start_code,
            stop_code,
            above_bar1_text,
            above_bar2_text,
            barcode_height,
            barcode_width,
            barcode_fontsize,
            barcode_fontfamily,
            above_bar1_fontsize,
            above_bar2_fontsize,
            above_bar1_fontfamily,
            above_bar2_fontfamily,
):

        qzone=10
        nwratio = 3
        bar_color="#000"
        space_color="#FFF"
        barcode_y=0
        img_height = barcode_height
        if show_barcode_number:
            img_height=img_height +barcode_fontsize
        if above_bar1_text > "":
            img_height=img_height + above_bar1_fontsize
            barcode_y = barcode_y + above_bar1_fontsize
        if above_bar2_text > "":
            img_height=img_height + above_bar2_fontsize
            barcode_y = barcode_y + above_bar2_fontsize
        show_startstop=False

        barcode_data = start_code + barcode_number.replace(" ","") + stop_code

        charpats={

            "0": {"pat":"0000011"},
            "1": {"pat":"0000110"},
            "2": {"pat":"0001001"},
            "3": {"pat":"1100000"},
            "4": {"pat":"0010010"},
            "5": {"pat":"1000010"},
            "6": {"pat":"0100001"},
            "7": {"pat":"0100100"},
            "8": {"pat":"0110000"},
            "9": {"pat":"1001000"},
            "A": {"pat":"0011010"},
            "B": {"pat":"0101001"},
            "C": {"pat":"0001011"},
            "D": {"pat":"0001110"},
            "-": {"pat":"0001100"},
            "$": {"pat":"0011000"},
            ":": {"pat":"1000101"},
            "/": {"pat":"1010001"},
            ".": {"pat":"1010100"},
            "+": {"pat":"0010101"},
        }

        dry_narobar_width = 60

        numchars =len(barcode_data)

        # dry run to calculate width of barcode
        xpos = qzone * dry_narobar_width
        for codepos in range(numchars):

            charpat = charpats[barcode_data[codepos]]["pat"]
            if charpat.count("1") == 2:
                xpos = xpos + 5 * dry_narobar_width + 2 * dry_narobar_width * nwratio
            else:
                xpos = xpos + 4 * dry_narobar_width + 3 * dry_narobar_width * nwratio
            xpos = xpos + dry_narobar_width

        xpos = xpos - dry_narobar_width
        xpos = xpos + qzone * dry_narobar_width

        narobar_width = dry_narobar_width * barcode_width / xpos

        img_width = barcode_width

        img = Image.new("RGB", (img_width, img_height),"#ffffff")

        draw = ImageDraw.Draw(img)

        xpos = qzone * narobar_width

        for codepos in range(numchars):
            fillcolor=bar_color
            charpat = charpats[barcode_data[codepos]]["pat"]

            for charpos in range(len(charpat)):

                bandwidth = narobar_width if charpat[charpos] == "0" else narobar_width * nwratio
                shape = [(xpos, barcode_y), (xpos + bandwidth, barcode_y + barcode_height)]
                draw.rectangle(shape, fill=fillcolor)
                xpos = xpos + bandwidth
                fillcolor = space_color if fillcolor==bar_color else bar_color
            xpos = xpos + narobar_width

        xpos = xpos - narobar_width
        xpos = xpos + qzone * narobar_width

        barcode_text = barcode_number
        if show_startstop:
            barcode_text = start + barcode_text + stop

        try:
            font_barcode_text = ImageFont.truetype(barcode_fontfamily, size=barcode_fontsize)
        except IOError:
            font_barcode_text = ImageFont.load_default()

        bbox = draw.textbbox((0,0), barcode_text, font=font_barcode_text)
        text_width=bbox[2] - bbox[0]

        text_x = (img_width - text_width) // 2


        draw.text((text_x, barcode_y + barcode_height ), barcode_text, fill="black", font=font_barcode_text, align="center")

        if above_bar1_text> "":
            try:
                above_bar1_fontfamily= ImageFont.truetype(above_bar1_fontfamily, size=above_bar1_fontsize)
            except IOError:
                above_bar1_fontfamily= ImageFont.load_default()

            bbox = draw.textbbox((0,0), above_bar1_text, font=above_bar1_fontfamily)
            text_width=bbox[2] - bbox[0]

            text_x = (img_width - text_width) // 2

            draw.text((text_x, 0 ), above_bar1_text, fill="black", font=above_bar1_fontfamily, align="center")

        if above_bar2_text> "":
            try:
                above_bar2_fontfamily= ImageFont.truetype(above_bar2_fontfamily, size=above_bar2_fontsize)
            except IOError:
                above_bar2_fontfamily= ImageFont.load_default()

            bbox = draw.textbbox((0,0), above_bar2_text, font=above_bar2_fontfamily)
            text_width=bbox[2] - bbox[0]

            text_x = (img_width - text_width) // 2

            draw.text((text_x, above_bar1_fontsize ), above_bar2_text, fill="black", font=above_bar2_fontfamily, align="center")

        byio = BytesIO()
        img.save(byio, format="jpeg")
        img_data=byio.getvalue()

        return(img_data)

class BarcodeLabelCreate(FormView):


    form_class = BarcodeForm
    template_name = 'library_labels/barcode_label.html'

    def form_valid(self, form):

        clean_data = form.cleaned_data

        barcode_label_data = make_barcode_label(
            clean_data["barcode_number"],
            clean_data["show_barcode_number"],
            clean_data["show_startstop"],
            clean_data["start_code"],
            clean_data["stop_code"],
            clean_data["above_bar1_text"],
            clean_data["above_bar2_text"],
            clean_data["barcode_height"],
            clean_data["barcode_width"],
            clean_data["barcode_fontsize"],
            clean_data["barcode_fontfamily"],
            clean_data["above_bar1_fontsize"],
            clean_data["above_bar2_fontsize"],
            clean_data["above_bar1_fontfamily"],
            clean_data["above_bar2_fontfamily"],

        )

        codabar_image = base64.standard_b64encode(barcode_label_data).decode("utf-8")


        context_data = self.get_context_data()
        context_data["form"] = form

        context_data["codabar_image"] = codabar_image
        context_data["barcode_number"] = clean_data["barcode_number"], 
        context_data["show_barcode_number"] = clean_data["show_barcode_number"], 
        context_data["show_startstop"] = clean_data["show_startstop"], 
        context_data["start_code"] = clean_data["start_code"], 
        context_data["stop_code"] = clean_data["stop_code"], 
        context_data["above_bar1_text"] = clean_data["above_bar1_text"]
        context_data["above_bar2_text"] = clean_data["above_bar2_text"]
        context_data["barcode_height"] = clean_data["barcode_height"]
        context_data["barcode_width"] = clean_data["barcode_width"]
        context_data["barcode_fontsize"] = clean_data["barcode_fontsize"]
        context_data["barcode_fontfamily"] = clean_data["barcode_fontfamily"]
        context_data["above_bar1_fontsize"] = clean_data["above_bar1_fontsize"]
        context_data["above_bar2_fontsize"] = clean_data["above_bar2_fontsize"]
        context_data["above_bar1_fontfamily"] = clean_data["above_bar1_fontfamily"]
        context_data["above_bar2_fontfamily"] = clean_data["above_bar2_fontfamily"]

        return render( self.request, self.template_name, context_data )


class SSIDLabelCreate(FormView):


    form_class = SSIDForm
    template_name = 'library_labels/ssid_label.html'

    def form_valid(self, form):

        clean_data = form.cleaned_data

        ssid_label_data = make_ssid_label(
            clean_data["ssid_text"],
            clean_data["password_text"],
            clean_data["notice1_text"],
            clean_data["notice2_text"],
            clean_data["ssid_fontsize"],
            clean_data["ssid_fontfamily"],
            clean_data["password_fontsize"],
            clean_data["password_fontfamily"],
            clean_data["notice1_fontsize"],
            clean_data["notice1_fontfamily"],
            clean_data["notice2_fontsize"],
            clean_data["notice2_fontfamily"],
        )

        ssid_image = base64.standard_b64encode(ssid_label_data).decode("utf-8")


        context_data = self.get_context_data()
        context_data["form"] = form
        context_data["ssid_image"] = ssid_image
        context_data["ssid_text"] = clean_data["ssid_text"]
        context_data["password_text"] = clean_data["password_text"]
        context_data["notice1_text"] = clean_data["notice1_text"]
        context_data["notice2_text"] = clean_data["notice2_text"]
        context_data["ssid_fontsize"] = clean_data["ssid_fontsize"]
        context_data["ssid_fontfamily"] = clean_data["ssid_fontfamily"]
        context_data["password_fontsize"] = clean_data["password_fontsize"]
        context_data["password_fontfamily"] = clean_data["password_fontfamily"]
        context_data["notice1_fontsize"] = clean_data["notice1_fontsize"]
        context_data["notice1_fontfamily"] = clean_data["notice1_fontfamily"]
        context_data["notice2_fontsize"] = clean_data["notice2_fontsize"]
        context_data["notice2_fontfamily"] = clean_data["notice2_fontfamily"]


        return render( self.request, self.template_name, context_data )


