"""
high level support for doing this and that.
"""

import time
import asyncio


async def delivery(name, mealtime):
    """co-routine, await 객체는 coroutine, task, future 유형에 사용"""
    # sleep은 설정한 시간만큼 blocking 하는 데 사용
    print(f"{name}에게 배달 완료")
    await asyncio.sleep(mealtime)
    print(f"{name} 식사 완료, {mealtime} 시간 소요")
    print(f"{name}로부터 회수 완료")


async def main():
    """https://docs.python.org/ko/3/library/asyncio-task.html"""
    # gather은 동시에 task 실행하기_동시성
    result = await asyncio.gather(
        delivery("성용", 1),
        delivery("재석", 1),
        delivery("명수", 1),
    )

    print(result)


async def main_task():
    """task는 미리 변수 선언을 하여, 예약처럼 사용한다"""
    task01 = asyncio.create_task(delivery("준하", 2))
    task02 = asyncio.create_task(delivery("홍철", 4))
    task03 = asyncio.create_task(delivery("하하", 2))

    await task01
    await task02
    await task03

    await delivery("형돈", 3)


async def hello_world():
    """asyncio.run에 대한 test"""
    print("hello world")
    return 123


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
    asyncio.run(hello_world())
    asyncio.run(main_task())
    second_end = time.time()
    print(second_end - start)
