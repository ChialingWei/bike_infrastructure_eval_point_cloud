import open3d as o3d
import numpy as np
import cv2
import os
import tqdm

def ply_to_jpg(ply):
# Load point c  loud
    point_cloud = o3d.io.read_point_cloud(ply)

    # Get XYZ coordinates and RGB colors of the points
    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors)

    # Project points onto the XY plane
    projected_points = points[:, :2]
    projected_points[:, 1] = -projected_points[:, 1] 

    # Define image resolution
    image_resolution = (1280, 1280)

    # Create an empty image
    bird_eye_view_image = np.zeros((image_resolution[0], image_resolution[1], 3), dtype=np.uint8)

    # Map points and enhanced colors to the image grid
    scaled_points = (projected_points - projected_points.min(axis=0)) / (projected_points.max(axis=0) - projected_points.min(axis=0))
    scaled_points *= np.array((1279, 1279))  # Invert Y-axis

    # Enhance color contrast
    enhancement_factor = 1.5  # Adjust this value to control the contrast enhancement

    for point, color in zip(scaled_points, colors):
        x, y = point.astype(int)
        enhanced_color = (color * enhancement_factor).clip(0, 1)
        bird_eye_view_image[y, x] = (enhanced_color * 255).astype(np.uint8)

    return bird_eye_view_image



original_path = '21_2'
save_path = '21_2'
for img in tqdm.tqdm(os.listdir(original_path)):
    img_path = os.path.join(original_path, img)
    bird_eye_view_image = ply_to_jpg(img_path)
    save_img_name = img.replace('.ply', '.jpg')
    save_img = os.path.join(save_path, save_img_name)
    cv2.imwrite(save_img, bird_eye_view_image)

    
