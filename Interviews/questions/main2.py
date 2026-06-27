

def fibonacci_tuples(limit: int) -> list[tuple[int, int]]:
    try:
        result = [(1, 2), (3, 4)]

        while result[-1][1] <= limit:
            prev2 = result[-2]
            prev1 = result[-1]

            next_tuple = (
                prev2[0] + prev1[0],
                prev2[1] + prev1[1],
            )

            print(f"Generated tuple: {next_tuple}")
            result.append(next_tuple)

        return result[:-1] if result[-1][1] > limit else result

    except Exception as e:
        print(f"Error generating tuples: {e}")
        raise


print(fibonacci_tuples(30))