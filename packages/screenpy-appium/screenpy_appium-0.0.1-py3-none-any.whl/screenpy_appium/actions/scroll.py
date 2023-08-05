from typing import Optional

from appium.webdriver.common.appiumby import AppiumBy
from screenpy import Actor
from screenpy.pacing import beat
from screenpy.exceptions import UnableToAct

from screenpy_appium import Target
from screenpy_appium.abilities import (
    UseAMobileDevice,
    UseAnAndroidDevice,
    UseAnIOSDevice,
)


class Scroll:
    """Scroll the screen in a direction or to an element.

    Abilities Required:
        :class:`~screenpy_appium.abilities.UseAnAndroidDevice`
        :class:`~screenpy_appium.abilities.UseAnIOSDevice`

    Examples::

        the_actor.attempts_to(Scroll.up())

        the_actor.attempts_to(Scroll.down())

        the_actor.attempts_to(Scroll.to(ACCEPT_BUTTON))
    """

    @classmethod
    def to(cls, target: Target) -> "Scroll":
        """Set the end point for the swipe."""
        return cls(target=target)

    @classmethod
    def up(cls) -> "Scroll":
        "Scroll up!"
        return cls(direction="up")

    @classmethod
    def down(cls) -> "Scroll":
        "Scroll down!"
        return cls(direction="down")

    @classmethod
    def left(cls) -> "Scroll":
        "Scroll left!"
        return cls(direction="left")

    @classmethod
    def right(cls) -> "Scroll":
        "Scroll right!"
        return cls(direction="right")

    def __call__(self, num: int) -> "Scroll":
        """Set how many times to scroll."""

    @property
    def log_description(self) -> str:
        """Get a nice description for the beat."""
        if self.target is not None:
            desc = f"to the {self.target}"
        else:
            desc = self.direction
            if self.repeat > 1:
                desc += f" {self.repeat} times."

        return desc

    @beat("{} scrolls {log_description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to scroll the screen."""
        if self.direction is None and self.target is None:
            raise UnableToAct(
                "Must either set direction or supply a target to scroll to."
            )

        ability = the_actor.ability_to(UseAMobileDevice)
        driver = ability.driver

        if self.direction is not None:
            dimensions = driver.get_window_size()["height"]
            driver.execute_script(
                "mobile:scrollGesture",
                {
                    "direction": self.direction,
                    "left": dimensions.width // 2,
                    "top": dimensions.height // 10,
                    "width": 200,
                    "height": dimensions.height // 4,
                    "percent": 3.5,
                },
            )

        if self.target is not None:
            if the_actor.has_ability_to(UseAnAndroidDevice):
                strategy, locator = self.target
                if strategy == AppiumBy.ANDROID_UIAUTOMATOR:
                    if "scrollIntoView" in locator:
                        self.target.found_by(the_actor)
                    else:
                        raise UnableToAct(
                            "Cannot scroll to element on Android"
                            " using UIAutomator locator"
                            " without a scrollIntoView directive."
                        )
                elif strategy == AppiumBy.ACCESSIBILITY_ID:
                    scroll_target = Target.the(self.target.description).located(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        "new UiScrollable(new UiSelector().scrollable(true))"
                        + f'.scrollIntoView(new UiSelector().text("{locator}"))'
                    )
                    scroll_target.found_by(the_actor)

            elif the_actor.has_ability_to(UseAnIOSDevice):
                element = self.target.found_by(the_actor)
                driver.execute_script(
                    "mobile:scroll", {"elementId": element.id, "toVisible": "true"}
                )

    def __init__(
        self, direction: Optional[str] = None, target: Optional[Target] = None
    ) -> None:
        self.direction = direction
        self.target = target
        self.repeat = 1
