@echo off
echo Voice Processing Project - Audio Validation
echo ==========================================
echo.
echo Testing generated audio samples...
echo If you can hear these, your audio pipeline is working!
echo.
pause

echo Playing synthetic vowel...
start /wait "" "synthetic_vowel.wav"
timeout /t 1 >nul
echo.
echo Playing voice harmonics...
start /wait "" "voice_harmonics.wav"
timeout /t 1 >nul
echo.
echo Playing frequency sweep...
start /wait "" "frequency_sweep.wav"
timeout /t 1 >nul
echo.
echo.
echo Voice processing pipeline validated!
pause