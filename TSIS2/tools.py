import pygame

def flood_fill(surface, x, y, new_color):
    """Алгоритм заливки (Flood Fill) через очередь (BFS)"""
    
    target_color = surface.get_at((x, y))
    
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    pixels = [(x, y)]
    
    while pixels:
        cx, cy = pixels.pop()
        
        
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), new_color)
            
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    pixels.append((nx, ny))