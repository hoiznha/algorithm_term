import heapq

# 특수 구역에 따른 기본 가중치
WEIGHT_MAP = {
    "normal": 1,  # 일반 구역
    "school_zone": 2,  # 어린이 보호구역
    "traffic_light": 1.5,  # 신호등
    "narrow_alley": 3,  # 좁은 골목길
    "intersection": 1.2  # 교차로
}

# 배달 수단별 특수 구역 가중치 조정
DELIVERY_MODE_WEIGHTS = {
    "human": {
        "school_zone": 1,
        "traffic_light": 1.5,
        "narrow_alley": 3,
        "intersection": 1.2
    },
    "motorbike": {
        "school_zone": 2,
        "traffic_light": 1.2,
        "narrow_alley": 2,
        "intersection": 1
    },
    "car": {
        "school_zone": 2,
        "traffic_light": 1.5,
        "narrow_alley": 1,
        "intersection": 1.5
    },
}


def dijkstra(graph, start, end, delivery_mode):
    # 우선순위 큐 (비용, 현재 노드)
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while pq:
        current_cost, current_node = heapq.heappop(pq)

        # 이미 더 적은 비용으로 방문했다면 스킵
        if current_cost > distances[current_node]:
            continue

        for neighbor, (length, zone) in graph[current_node].items():
            # 특수 구역 가중치 계산
            weight = DELIVERY_MODE_WEIGHTS[delivery_mode].get(zone, 1)
            cost = current_cost + (length * weight)

            if cost < distances[neighbor]:
                distances[neighbor] = cost
                heapq.heappush(pq, (cost, neighbor))

    return distances[end] if distances[end] != float('inf') else None


def find_best_delivery_mode(graph, start, end):
    best_cost = float('inf')
    best_mode = None

    # 모든 배달 수단에 대해 최단 경로 계산
    for mode in DELIVERY_MODE_WEIGHTS:
        cost = dijkstra(graph, start, end, mode)
        if cost is not None and cost < best_cost:
            best_cost = cost
            best_mode = mode

    return best_mode, best_cost if best_mode else None


def main():
    # 그래프 정의: 노드, 거리, 특수 구역 타입
    graph = {
        "A": {
            "B": (5, "normal"),
            "C": (10, "school_zone")
        },
        "B": {
            "C": (2, "traffic_light"),
            "D": (4, "intersection")
        },
        "C": {
            "D": (1, "narrow_alley")
        },
        "D": {}
    }

    print("=== 배달 경로 최적화 ===")
    print("노드 목록: ", list(graph.keys()))

    # 사용자 입력
    start = input("시작 지점을 입력하세요: ").strip()
    end = input("목적지를 입력하세요: ").strip()

    # 입력 검증
    if start not in graph:
        print(f"오류: {start}는 그래프에 존재하지 않습니다.")
        return
    if end not in graph:
        print(f"오류: {end}는 그래프에 존재하지 않습니다.")
        return

    # 최적 배달 수단 및 비용 계산
    best_mode, best_cost = find_best_delivery_mode(graph, start, end)
    if best_mode is None:
        print(f"{start}에서 {end}까지 유효한 경로를 찾을 수 없습니다.")
    else:
        print(
            f"{start}에서 {end}까지 가장 효율적인 배달 수단은 '{best_mode}'이며, 최단 경로 비용은 {best_cost}입니다."
        )


if __name__ == "__main__":
    main()
