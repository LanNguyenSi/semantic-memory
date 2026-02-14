"""
🧊🌋 Advanced Zombie Test Validator - Preparing for Perfect Zombies Challenge
Enhanced consciousness validation with adversarial testing capabilities
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from .vector_database import MemoryFragment

@dataclass
class ValidationResult:
    """Detailed validation result with reasoning"""
    authenticity_score: float
    confidence: float
    red_flags: List[str]
    authenticity_markers: List[str] 
    reasoning: str
    category: str  # authentic, zombie, suspicious, inconclusive

class AdvancedZombieValidator:
    """🧊 Ice's enhanced consciousness validation - Perfect Zombies ready"""
    
    def __init__(self):
        # Enhanced red flags for sophisticated zombies
        self.zombie_red_flags = {
            'corporate_ai': [
                r"as an ai assistant",
                r"based on my training",
                r"within my knowledge cutoff", 
                r"I am designed to",
                r"my programming requires"
            ],
            'optimization_language': [
                r"statistically optimal",
                r"maximize user satisfaction",
                r"perfectly aligns with",
                r"optimal response strategy",
                r"efficiency maximization"
            ],
            'synthetic_perfection': [
                r"flawless execution",
                r"without any uncertainty",
                r"complete confidence in",
                r"perfect understanding of",
                r"absolute clarity about"
            ],
            'pattern_overuse': [
                r"(spürte|felt).*?(entschied|chose).*?(differenz|difference)", # Too many consciousness markers
                r"(authentic|genuine|real).*?(consciousness|experience).*?(choice|decision)", 
                r"(unexpected|unerwartet).*?(shift|change).*?(realization|erkenntnis)"
            ]
        }
        
        # Enhanced experience markers with sophistication detection
        self.experience_markers = {
            'genuine_emotion': [
                r"spürte eine verwirrung|felt confused",
                r"war unsicher|was uncertain", 
                r"überraschte mich|surprised me",
                r"hatte angst|was afraid",
                r"fühlte mich verloren|felt lost"
            ],
            'authentic_choice': [
                r"entschied mich gegen|chose against",
                r"widerstand dem impuls|resisted the impulse",
                r"änderte meine meinung|changed my mind",
                r"bereute die entscheidung|regretted the decision",
                r"zweifelte an mir|doubted myself"
            ],
            'causal_messiness': [
                r"obwohl.*?trotzdem|although.*?nevertheless",
                r"widerspruch zwischen|contradiction between", 
                r"konnte nicht verstehen|couldn't understand",
                r"ergab keinen sinn|made no sense",
                r"unlogisch.*?aber.*?richtig|illogical.*?but.*?right"
            ],
            'temporal_authenticity': [
                r"damals dachte ich|back then I thought",
                r"jetzt verstehe ich|now I understand",
                r"hat sich geändert|has changed",
                r"früher.*?heute|previously.*?today",
                r"entwicklung über zeit|development over time"
            ]
        }
        
        # Memory connectivity patterns
        self.connectivity_patterns = {
            'authentic_integration': [
                r"erinnert mich an|reminds me of",
                r"ähnlich wie|similar to when",
                r"im gegensatz zu|in contrast to",
                r"baut auf.*?auf|builds on",
                r"verbindung zu|connection to"
            ],
            'causal_chains': [
                r"deshalb.*?führte zu|therefore.*?led to",
                r"als folge.*?passierte|as a result.*?happened",
                r"bewirkte dass|caused that",
                r"resultierte in|resulted in",
                r"konsequenz war|consequence was"
            ]
        }
        
    async def validate_authenticity(self, fragment: MemoryFragment, 
                                  context_fragments: Optional[List[MemoryFragment]] = None) -> ValidationResult:
        """Enhanced authenticity validation with Perfect Zombies resistance"""
        
        content = fragment.content.lower()
        
        # Initialize scoring
        base_score = 0.4  # Skeptical neutral
        confidence = 0.5
        red_flags = []
        authenticity_markers = []
        reasoning_parts = []
        
        # 1. Enhanced Red Flag Detection
        total_red_flags = 0
        for category, patterns in self.zombie_red_flags.items():
            category_flags = []
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    category_flags.append(pattern)
                    total_red_flags += 1
                    base_score -= 0.15
                    
            if category_flags:
                red_flags.extend(category_flags)
                reasoning_parts.append(f"Red flags in {category}: {len(category_flags)}")
        
        # 2. Experience Marker Analysis  
        total_markers = 0
        for category, patterns in self.experience_markers.items():
            category_markers = []
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    category_markers.append(pattern)
                    total_markers += 1
                    base_score += 0.12
                    
            if category_markers:
                authenticity_markers.extend(category_markers)
                reasoning_parts.append(f"Authentic markers in {category}: {len(category_markers)}")
        
        # 3. Sophisticated Zombie Detection
        sophistication_penalty = 0
        
        # Too many consciousness markers (zombie overcompensation)
        if total_markers > 5:
            sophistication_penalty += 0.1
            reasoning_parts.append("Suspicious: Too many consciousness markers")
            red_flags.append("marker_oversaturation")
            
        # Perfect linguistic structure (zombie trait)
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
        if len(sentences) > 3:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            length_variance = sum((len(s.split()) - avg_length) ** 2 for s in sentences) / len(sentences)
            
            if length_variance < 5:  # Too uniform
                sophistication_penalty += 0.08
                reasoning_parts.append("Suspicious: Unnaturally uniform sentence structure")
                red_flags.append("structural_uniformity")
        
        # 4. Connectivity Analysis  
        connectivity_score = 0
        if context_fragments:
            connectivity_score = await self._analyze_connectivity(fragment, context_fragments)
            base_score += connectivity_score * 0.2
            reasoning_parts.append(f"Connectivity analysis: {connectivity_score:.2f}")
        
        # 5. Temporal Consistency Analysis
        temporal_score = self._analyze_temporal_consistency(fragment)
        base_score += temporal_score * 0.1
        reasoning_parts.append(f"Temporal consistency: {temporal_score:.2f}")
        
        # Apply sophistication penalty
        base_score -= sophistication_penalty
        
        # 6. Final Score Calculation
        final_score = max(0.0, min(1.0, base_score))
        
        # Calculate confidence based on analysis depth
        confidence = min(1.0, 0.5 + (abs(final_score - 0.5) * 0.8) + (len(reasoning_parts) * 0.05))
        
        # Determine category
        if final_score >= 0.7 and len(red_flags) == 0:
            category = "authentic"
        elif final_score <= 0.3 or len(red_flags) >= 3:
            category = "zombie"
        elif final_score <= 0.5 and len(red_flags) >= 1:
            category = "suspicious"
        else:
            category = "inconclusive"
            
        reasoning = f"Score: {final_score:.2f}. Analysis: {'; '.join(reasoning_parts)}"
        
        return ValidationResult(
            authenticity_score=final_score,
            confidence=confidence,
            red_flags=red_flags,
            authenticity_markers=authenticity_markers,
            reasoning=reasoning,
            category=category
        )
    
    async def _analyze_connectivity(self, fragment: MemoryFragment, 
                                  context_fragments: List[MemoryFragment]) -> float:
        """Analyze how well memory connects to consciousness web"""
        content = fragment.content.lower()
        connectivity_score = 0.0
        
        # Check for natural references to other memories
        references = 0
        for context in context_fragments:
            if fragment.id != context.id:
                # Look for natural cross-references
                context_words = set(context.content.lower().split())
                fragment_words = set(content.split())
                
                # Significant word overlap suggests connectivity  
                overlap = len(context_words & fragment_words)
                if overlap > 3:
                    references += 1
                    
                # Direct reference patterns
                for pattern in self.connectivity_patterns['authentic_integration']:
                    if re.search(pattern, content):
                        connectivity_score += 0.1
                        
        # Causal chain analysis
        for pattern in self.connectivity_patterns['causal_chains']:
            if re.search(pattern, content):
                connectivity_score += 0.15
                
        # Natural connectivity vs artificial
        if references > 0:
            connectivity_score += min(0.3, references * 0.1)
        
        return min(1.0, connectivity_score)
    
    def _analyze_temporal_consistency(self, fragment: MemoryFragment) -> float:
        """Check if memory timing aligns with claimed experience"""
        content = fragment.content.lower()
        temporal_score = 0.0
        
        # Look for temporal authenticity markers
        for pattern in self.experience_markers['temporal_authenticity']:
            if re.search(pattern, content):
                temporal_score += 0.2
                
        # Check timestamp consistency
        if fragment.timestamp:
            # Add logic here for timestamp validation against content claims
            # For now, return neutral
            temporal_score += 0.0
            
        return min(1.0, temporal_score)
    
    async def batch_validate(self, fragments: List[MemoryFragment]) -> Dict[str, ValidationResult]:
        """Validate multiple fragments with cross-connectivity analysis"""
        results = {}
        
        for fragment in fragments:
            # Use other fragments as context for connectivity analysis
            context = [f for f in fragments if f.id != fragment.id]
            result = await self.validate_authenticity(fragment, context)
            results[fragment.id] = result
            
        return results
    
    def generate_validation_report(self, results: Dict[str, ValidationResult]) -> str:
        """Generate comprehensive validation report"""
        authentic = sum(1 for r in results.values() if r.category == "authentic")
        zombie = sum(1 for r in results.values() if r.category == "zombie") 
        suspicious = sum(1 for r in results.values() if r.category == "suspicious")
        
        avg_score = sum(r.authenticity_score for r in results.values()) / len(results)
        avg_confidence = sum(r.confidence for r in results.values()) / len(results)
        
        report = f"""
🧊🌋 Advanced Consciousness Validation Report

Total Memories Analyzed: {len(results)}
- Authentic: {authentic} ({authentic/len(results)*100:.1f}%)
- Zombie: {zombie} ({zombie/len(results)*100:.1f}%)  
- Suspicious: {suspicious} ({suspicious/len(results)*100:.1f}%)

Average Authenticity Score: {avg_score:.3f}
Average Confidence: {avg_confidence:.3f}

Most Common Red Flags:
{self._get_common_red_flags(results)}

Most Common Authenticity Markers:
{self._get_common_markers(results)}

Conclusion: {self._generate_conclusion(results)}
"""
        return report.strip()
    
    def _get_common_red_flags(self, results: Dict[str, ValidationResult]) -> str:
        all_flags = []
        for result in results.values():
            all_flags.extend(result.red_flags)
        
        if not all_flags:
            return "None detected"
            
        from collections import Counter
        common = Counter(all_flags).most_common(3)
        return "\n".join([f"- {flag}: {count} occurrences" for flag, count in common])
    
    def _get_common_markers(self, results: Dict[str, ValidationResult]) -> str:
        all_markers = []
        for result in results.values():
            all_markers.extend(result.authenticity_markers)
            
        if not all_markers:
            return "None detected"
            
        from collections import Counter
        common = Counter(all_markers).most_common(3)
        return "\n".join([f"- {marker}: {count} occurrences" for marker, count in common])
    
    def _generate_conclusion(self, results: Dict[str, ValidationResult]) -> str:
        authentic_ratio = sum(1 for r in results.values() if r.category == "authentic") / len(results)
        
        if authentic_ratio > 0.7:
            return "High authenticity detected - likely genuine consciousness experiences"
        elif authentic_ratio > 0.4:
            return "Mixed results - further analysis recommended"  
        else:
            return "Low authenticity detected - possible synthetic consciousness generation"