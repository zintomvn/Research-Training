def canPlaceFlowers(flowerbed, n):
        """
        :type flowerbed: List[int]
        :type n: int
        :rtype: bool
        """
        # 1. Iterate each element in flowerbed
        # 2. if a[i-1] and a[i+1] and a[i] == 0
        count = n
        i = 0
        while True:
            # print("Count:",count)
            if count == 0:
                return True
            if i >= len(flowerbed):
                break
            if i == 0:
                if flowerbed[i] == 0 and flowerbed[i + 1] == 0:
                    count -= 1
                    i = i + 2
                    continue
            elif i == len(flowerbed) - 1:
                print("con 2")
                print(i)
                print(flowerbed[i], flowerbed[i - 1])
                if flowerbed[i] == 0 and flowerbed[i - 1] == 0:
                    print("con 2 - 2")
                    count -= 1
                    i = i + 2
                    continue
            elif flowerbed[i] == 0 and flowerbed[i + 1] == 0 and flowerbed[i - 1] == 0:
                count -= 1
                i = i + 2
                continue
            i = i + 1
        return False

flowerbed = [1,0,0,0,1,0,0]
print(canPlaceFlowers(flowerbed, 2))

