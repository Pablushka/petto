#!/usr/bin/env python3
"""
Test script for PDF generation using Playwright Chrome engine
"""
import asyncio
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pdf_generator import get_pdf_generator

async def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    # Sample pet data
    sample_data = {
        "pet_name": "Test Dog",
        "pet_type": "Dog",
        "pet_age": "3 years",
        "pet_breed": "Golden Retriever",
        "pet_color": "Golden",
        "pet_gender": "Male",
        "pet_last_seen": "Yesterday",
        "pet_location": "Central Park",
        "pet_description": "Friendly golden retriever, responds to 'Buddy'. Has a red collar.",
        "pet_picture": "https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Test+Dog",
        "pet_picture2": "https://via.placeholder.com/200x200/4ECDC4/FFFFFF?text=Photo+2",
        "pet_picture3": "",
        "pet_picture4": "",
        "pet_picture5": "",
        "qr_code_url": "https://via.placeholder.com/100x100/000000/FFFFFF?text=QR",
        "owner_name": "John Doe",
        "owner_phone": "555-0123",
        "owner_email": "john@example.com",
        "owner_address": "123 Main St, City, State",
        "reward_amount": "$500",
        "show_reward": True,
        "print_mode": "color",
        "pet_id": 1
    }
    
    try:
        print("🚀 Starting PDF generation test...")
        
        # Get PDF generator
        generator = get_pdf_generator()
        
        # Generate PDF
        print("📄 Generating PDF...")
        pdf_bytes = await generator.generate_flyer_pdf(
            pet_data=sample_data,
            format="a4",
            orientation="portrait",
            color_mode="color",
            quality="high"
        )
        
        # Save PDF to file
        output_file = "test_flyer.pdf"
        with open(output_file, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generated successfully! Saved as: {output_file}")
        print(f"📊 PDF size: {len(pdf_bytes)} bytes")
        
        print("🧹 Test completed")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pdf_generation())