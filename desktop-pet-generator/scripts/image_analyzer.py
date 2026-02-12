#!/usr/bin/env python3
"""
Image Analyzer for Desktop Pet Generator
Extracts features, colors, and metadata from uploaded images
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Missing dependencies. Install with: pip install Pillow numpy", file=sys.stderr)
    sys.exit(1)


class ImageAnalyzer:
    """Analyzes images for desktop pet generation"""

    def __init__(self, image_path: str):
        self.image_path = Path(image_path)
        self.image = None
        self.load_image()

    def load_image(self):
        """Load and validate image file"""
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        try:
            self.image = Image.open(self.image_path)
            # Convert to RGBA if not already
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
        except Exception as e:
            raise ValueError(f"Failed to load image: {e}")

    def get_dimensions(self) -> Dict[str, int]:
        """Get image dimensions"""
        return {
            "width": self.image.width,
            "height": self.image.height,
            "aspect_ratio": round(self.image.width / self.image.height, 2)
        }

    def has_transparency(self) -> bool:
        """Check if image has transparent pixels"""
        if self.image.mode != 'RGBA':
            return False

        # Check if alpha channel has any transparency
        alpha = np.array(self.image)[:, :, 3]
        return np.any(alpha < 255)

    def get_dominant_colors(self, num_colors: int = 5) -> List[Dict[str, any]]:
        """Extract dominant colors using k-means clustering"""
        # Resize for faster processing
        img_small = self.image.resize((100, 100))
        pixels = np.array(img_small)

        # Flatten to 2D array of RGB values (ignore alpha)
        pixels_rgb = pixels[:, :, :3].reshape(-1, 3)

        # Remove duplicates for efficiency
        unique_colors, counts = np.unique(pixels_rgb, axis=0, return_counts=True)

        # Sort by frequency
        sorted_indices = np.argsort(-counts)
        top_colors = unique_colors[sorted_indices[:num_colors]]
        top_counts = counts[sorted_indices[:num_colors]]

        # Format results
        colors = []
        total_pixels = len(pixels_rgb)

        for color, count in zip(top_colors, top_counts):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            percentage = round((count / total_pixels) * 100, 1)
            colors.append({
                "hex": hex_color,
                "rgb": color.tolist(),
                "percentage": percentage,
                "name": self._get_color_name(color)
            })

        return colors

    def _get_color_name(self, rgb: np.ndarray) -> str:
        """Get human-readable color name from RGB"""
        r, g, b = rgb

        # Simple color naming logic
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > g and r > b:
            if r > 200:
                return "red"
            else:
                return "dark red"
        elif g > r and g > b:
            if g > 200:
                return "green"
            else:
                return "dark green"
        elif b > r and b > g:
            if b > 200:
                return "blue"
            else:
                return "dark blue"
        elif r > 150 and g > 150:
            return "yellow"
        elif r > 150 and b > 150:
            return "magenta"
        elif g > 150 and b > 150:
            return "cyan"
        elif r > 100 and g > 100 and b > 100:
            return "gray"
        else:
            return "brown"

    def detect_complexity(self) -> str:
        """Determine if image is simple or complex"""
        # Calculate edge density as complexity metric
        img_gray = self.image.convert('L')
        img_array = np.array(img_gray)

        # Simple edge detection using gradient
        edges_x = np.abs(np.diff(img_array, axis=1))
        edges_y = np.abs(np.diff(img_array, axis=0))

        edge_density = (edges_x.mean() + edges_y.mean()) / 2

        if edge_density < 10:
            return "simple"
        elif edge_density < 30:
            return "moderate"
        else:
            return "complex"

    def suggest_mode(self) -> str:
        """Suggest CSS or Sprite mode based on image characteristics"""
        complexity = self.detect_complexity()
        has_alpha = self.has_transparency()
        dims = self.get_dimensions()

        # Simple images with transparency work well with CSS
        if complexity == "simple" and has_alpha:
            return "css"

        # Complex images need sprite mode
        if complexity == "complex":
            return "sprite"

        # Very large images are better as sprites
        if dims["width"] > 500 or dims["height"] > 500:
            return "sprite"

        return "css"

    def get_suggested_size(self) -> str:
        """Suggest appropriate display size"""
        dims = self.get_dimensions()

        # Based on original dimensions
        max_dim = max(dims["width"], dims["height"])

        if max_dim < 100:
            return "100px"
        elif max_dim < 200:
            return "150px"
        elif max_dim < 400:
            return "200px"
        else:
            return "300px"

    def detect_features(self) -> List[str]:
        """Detect potential features for animation (eyes, limbs, etc.)"""
        features = []

        # Analyze transparency for cutout features
        if self.has_transparency():
            features.append("transparent_background")

        # Check aspect ratio for feature detection
        dims = self.get_dimensions()
        ratio = dims["aspect_ratio"]

        if 0.8 <= ratio <= 1.2:
            features.append("square_shape")
        elif ratio > 1.5:
            features.append("wide_shape")
        elif ratio < 0.7:
            features.append("tall_shape")

        # Detect predominant color types
        colors = self.get_dominant_colors(3)
        color_names = [c["name"] for c in colors]

        if "black" in color_names and "white" in color_names:
            features.append("high_contrast")

        return features

    def analyze(self) -> Dict:
        """Run full analysis and return results"""
        return {
            "file": {
                "path": str(self.image_path),
                "name": self.image_path.name,
                "format": self.image.format,
                "size_kb": round(self.image_path.stat().st_size / 1024, 2)
            },
            "dimensions": self.get_dimensions(),
            "transparency": self.has_transparency(),
            "dominant_colors": self.get_dominant_colors(),
            "complexity": self.detect_complexity(),
            "features": self.detect_features(),
            "suggestions": {
                "mode": self.suggest_mode(),
                "display_size": self.get_suggested_size(),
                "mode_reason": self._get_mode_reason()
            }
        }

    def _get_mode_reason(self) -> str:
        """Explain why a particular mode was suggested"""
        mode = self.suggest_mode()
        complexity = self.detect_complexity()

        if mode == "css":
            return f"Image is {complexity} with good transparency support - CSS animations will work well"
        else:
            return f"Image is {complexity} with intricate details - sprite-based animation recommended for best results"


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python image_analyzer.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        analyzer = ImageAnalyzer(image_path)
        results = analyzer.analyze()

        # Output as JSON
        print(json.dumps(results, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
