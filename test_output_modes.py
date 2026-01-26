#!/usr/bin/env python3
"""
Test script to verify output mode logic without calling LLM
"""

from pathlib import Path
import sys

# Add parent directory to path to import from extract_metrics
sys.path.insert(0, str(Path(__file__).parent))

from extract_metrics import get_output_path


def test_output_modes():
    """Test all output mode combinations"""

    print("Testing Output Mode Logic")
    print("=" * 60)

    # Test inputs
    input_file = Path("/specs/auth.md")
    default_output = Path("sib_metrics.json")
    custom_dir = Path("./metrics_output")

    # Test 1: Default mode
    result = get_output_path(input_file, "default", default_output, None)
    expected = Path("sib_metrics.json")
    status = "✅" if result == expected else "❌"
    print(f"\n{status} Test 1: Default mode")
    print(f"   Input:    {input_file}")
    print(f"   Expected: {expected}")
    print(f"   Got:      {result}")

    # Test 2: Alongside mode
    result = get_output_path(input_file, "alongside", default_output, None)
    expected = Path("/specs/auth_metrics.json")
    status = "✅" if result == expected else "❌"
    print(f"\n{status} Test 2: Alongside mode")
    print(f"   Input:    {input_file}")
    print(f"   Expected: {expected}")
    print(f"   Got:      {result}")

    # Test 3: Custom mode
    result = get_output_path(input_file, "custom", default_output, custom_dir)
    expected = Path("./metrics_output/auth_metrics.json")
    status = "✅" if result == expected else "❌"
    print(f"\n{status} Test 3: Custom mode")
    print(f"   Input:    {input_file}")
    print(f"   Custom:   {custom_dir}")
    print(f"   Expected: {expected}")
    print(f"   Got:      {result}")

    # Test 4: Alongside mode with nested path
    nested_input = Path("/project/specs/api/auth.md")
    result = get_output_path(nested_input, "alongside", default_output, None)
    expected = Path("/project/specs/api/auth_metrics.json")
    status = "✅" if result == expected else "❌"
    print(f"\n{status} Test 4: Alongside mode (nested)")
    print(f"   Input:    {nested_input}")
    print(f"   Expected: {expected}")
    print(f"   Got:      {result}")

    # Test 5: Custom mode with custom output filename
    custom_output = Path("custom_name.json")
    result = get_output_path(input_file, "custom", custom_output, custom_dir)
    expected = Path("./metrics_output/auth_metrics.json")
    status = "✅" if result == expected else "❌"
    print(f"\n{status} Test 5: Custom mode (ignores output name)")
    print(f"   Input:    {input_file}")
    print(f"   Output:   {custom_output}")
    print(f"   Custom:   {custom_dir}")
    print(f"   Expected: {expected}")
    print(f"   Got:      {result}")

    print("\n" + "=" * 60)
    print("All tests completed!")


if __name__ == "__main__":
    test_output_modes()
