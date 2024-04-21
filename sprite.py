from pygame import Surface, Rect
from camera import Camera


class Sprite:
    """
    Class to generate the character
    """

    def __init__(self, x: int, y: int, w: int, h: int, color: tuple):
        """
        Initializes the gameplay character.

        Args:
            x (int): An int representing that initial x position
            y (int): An int representing that initial y position
            w (int): An int representing that initial w position
            h (int): An int representing that initial h position
            color (tuple): A tuple representing the color code of
            the sprite
        """
        self.__color = color
        self._image = Surface((w, h))
        self._image.fill(self.color)
        self._image = self._image.convert()
        self.rect = Rect(x, y, w, h)
        self.camera_rect = self.rect.copy()

    @property
    def image(self) -> Surface:
        """
        Public getter for _image so it can remain a private
        attribute

        Returns:
            The image atttribute Surface
        """
        return self._image

    @property
    def color(self) -> tuple:
        """
        Public getter for _image so it can remain a private
        attribute

        Returns:
            The color atttribute tuple.
        """
        return self.__color

    @color.setter
    def color(self, new: tuple) -> None:
        """
        Sets the color of the sprite.

        Args:
            new (tuple): A tuple representing the color
            for the sprite to be genertaed as
        """
        assert isinstance(new, tuple) and len(new) == 3, "Value is not a color"
        self.__color = new

        self._image.fill(self.color)

    def draw(self, surface: Surface) -> None:
        """
        Renders the sprite into user view.
        Should be called every frame after updates occur.

        Surface: the pygame surface to draw on.
        """

        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self._image, self.camera_rect)
        else:
            surface.blit(self._image, self.rect)
