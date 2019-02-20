from PIL import Image, ImageMath, ImageChops


def color_dodge(im1, im2):
    """Brightens the backdrop color to reflect the source color.

    The color dodge formula is defined as:

        if(Cb == 0)
            B(Cb, Cs) = 0
        else if(Cs == 1)
            B(Cb, Cs) = 1
        else
            B(Cb, Cs) = min(1, Cb / (1 - Cs))

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingcolordodge

    Arguments:
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    cs_inverted = ImageChops.invert(im2)
    bands = [
        ImageMath.eval(
            '(cb / cs_inv) * 255', cb=cb, cs_inv=cs_inv).convert('L')
        for cb, cs_inv in zip(im1.split(), cs_inverted.split())
    ]

    return Image.merge('RGB', bands)
