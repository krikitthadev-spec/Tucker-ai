"""Vision Processor - Analyzes tablet screenshots.

Uses OCR and image processing to understand what's on the tablet screen.
"""

from typing import Optional, List, Dict
from pathlib import Path
from loguru import logger

class VisionProcessor:
    """Processes and analyzes screenshots from the tablet."""
    
    def __init__(self):
        """Initialize vision processor."""
        self.cv2 = None
        self.pytesseract = None
        self.PIL = None
        
        self._initialize_libraries()
        logger.info("VisionProcessor initialized")
    
    def _initialize_libraries(self):
        """Initialize computer vision libraries."""
        try:
            import cv2
            self.cv2 = cv2
            logger.info("✓ OpenCV available")
        except ImportError:
            logger.warning("OpenCV not available: pip install opencv-python")
        
        try:
            import pytesseract
            self.pytesseract = pytesseract
            logger.info("✓ Tesseract OCR available")
        except ImportError:
            logger.warning("Tesseract not available: pip install pytesseract")
        
        try:
            from PIL import Image
            self.PIL = Image
            logger.info("✓ PIL available")
        except ImportError:
            logger.warning("PIL not available: pip install Pillow")
    
    def analyze_screenshot(self, image_path: str) -> Dict:
        """Analyze a screenshot.
        
        Args:
            image_path: Path to screenshot file
            
        Returns:
            Dict with analysis results
        """
        if not Path(image_path).exists():
            logger.error(f"Screenshot not found: {image_path}")
            return {"success": False, "error": "File not found"}
        
        result = {
            "file": image_path,
            "text": "",
            "objects": [],
            "colors": []
        }
        
        # Extract text using OCR
        text = self.extract_text(image_path)
        if text:
            result["text"] = text
        
        # Analyze colors
        colors = self.analyze_colors(image_path)
        if colors:
            result["colors"] = colors
        
        result["success"] = True
        return result
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from screenshot using OCR.
        
        Args:
            image_path: Path to screenshot
            
        Returns:
            Extracted text
        """
        if not self.pytesseract:
            logger.warning("Tesseract not available")
            return ""
        
        try:
            from PIL import Image
            image = Image.open(image_path)
            text = self.pytesseract.image_to_string(image)
            logger.debug(f"Extracted text length: {len(text)}")
            return text
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return ""
    
    def analyze_colors(self, image_path: str) -> List[str]:
        """Analyze dominant colors in screenshot.
        
        Args:
            image_path: Path to screenshot
            
        Returns:
            List of dominant colors
        """
        if not self.cv2:
            logger.warning("OpenCV not available")
            return []
        
        try:
            image = self.cv2.imread(image_path)
            # Convert to RGB
            image = self.cv2.cvtColor(image, self.cv2.COLOR_BGR2RGB)
            # Simple color analysis - get average color
            avg_color = image.mean(axis=(0, 1))
            return [f"RGB({int(avg_color[0])}, {int(avg_color[1])}, {int(avg_color[2])})"]
        except Exception as e:
            logger.error(f"Color analysis error: {e}")
            return []
    
    def detect_objects(self, image_path: str) -> List[Dict]:
        """Detect objects in screenshot.
        
        Args:
            image_path: Path to screenshot
            
        Returns:
            List of detected objects
        """
        # This is a placeholder for future enhancement
        # Could use YOLO, TensorFlow, or other object detection models
        return []
    
    def find_similar_image(self, image_path: str, template_path: str) -> Optional[tuple]:
        """Find a template image within a screenshot.
        
        Args:
            image_path: Screenshot path
            template_path: Template image path
            
        Returns:
            (x, y) coordinates if found, None otherwise
        """
        if not self.cv2:
            logger.warning("OpenCV not available")
            return None
        
        try:
            image = self.cv2.imread(image_path)
            template = self.cv2.imread(template_path)
            
            result = self.cv2.matchTemplate(image, template, self.cv2.TM_CCOEFF)
            _, max_val, _, max_loc = self.cv2.minMaxLoc(result)
            
            if max_val > 0.8:  # Confidence threshold
                return max_loc
        except Exception as e:
            logger.error(f"Template matching error: {e}")
        
        return None

if __name__ == '__main__':
    # Test vision processor
    vision = VisionProcessor()
    print("Vision processor ready!")
