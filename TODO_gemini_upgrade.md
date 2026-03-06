# 🚀 Gemini Model Upgrade Plan

**Recommended Model:** `gemini-3-flash-preview` (JSON) & `gemini-3-pro-image-preview` (Vision)
**Reason:** Flash excels at reliably outputting complex JSON structures at scale, while Pro creates rich visual assets based on those instructions.

## Action Items
- [x] Update `generate_assets_hybrid.py` to target `gemini-3-flash-preview` for all structural/JSON generating endpoints.
- [x] Verify that the visual generation steps route to `gemini-3-pro-image-preview`.
- [x] Test a complete sequence of world-building asset generation for quality and parsing errors.
