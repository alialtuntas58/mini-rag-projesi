import os
import sys

# src klasöründeki modüllerin testlerden import edilebilmesi için
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
