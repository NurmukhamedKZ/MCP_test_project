from langchain_core.tools import tool

tool()
def add(a: float, b: float) -> float:
    """Add two numbers together

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a.
    
    Args:
        a: The number to subtract from
        b: The number to subtract
    """
    return a - b

tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    return a * b


tool()
def divide(a: float, b: float) -> str:
    """Divide two numbers with zero check

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Result of division or error message if dividing by zero
    """
    if b == 0:
        return "Error: Cannot divide by zero"
    result = a / b
    return f"{a} ÷ {b} = {result}"


tool()
def power(base: float, exponent: float) -> float:
    """Raise a number to a power

    Args:
        base: The base number
        exponent: The exponent

    Returns:
        base raised to the power of exponent
    """
    return base ** exponent

@tool
def calculate_percentage(total: float, percentage: float) -> float:
    """Calculate a percentage of a given total value.
    Useful for calculating discounts or taxes.
    
    Args:
        total: The full value (100%)
        percentage: The percentage to calculate (e.g., 15 for 15%)
    """
    return (total * percentage) / 100