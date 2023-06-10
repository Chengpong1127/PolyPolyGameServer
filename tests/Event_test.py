import pytest
from Basic.Event import Event
def test_iadd():
    event = Event()

    # Test that subscribing a function works correctly
    def callback():
        print("callback called")

    event += callback

    assert len(event) == 1

    # Test that trying to subscribe something other than a function raises an exception
    with pytest.raises(Exception) as exc:
        event += "not a function"

    assert str(exc.value) == "subscriber must be a function"


def test_invoke():
    event = Event()

    # Set up some subscribers for the event
    calls = []
    def callback1(arg):
        calls.append(("callback1", arg))
    event += callback1

    def callback2(arg):
        calls.append(("callback2", arg))
    event += callback2

    # Invoke the event and check that both subscribers were called
    event.Invoke("testarg")
    assert calls == [("callback1", "testarg"), ("callback2", "testarg")]


def test_isub():
    event = Event()

    # Set up some subscribers for the event
    calls = []
    def callback1(arg):
        calls.append(("callback1", arg))
    event += callback1

    def callback2(arg):
        calls.append(("callback2", arg))
    event += callback2

    # Unsubscribe one of the subscribers and verify that only one is called
    event -= callback1
    event.Invoke("testarg")
    assert calls == [("callback2", "testarg")]


if __name__ == "__main__":
    pytest.main()