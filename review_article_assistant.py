#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Review Article Writing Assistant
==========================================

A comprehensive tool for writing high-quality academic review articles for top-tier journals.

This tool helps researchers:
1. Define scope and develop outline
2. Manage and categorize literature
3. Draft sections with critical analysis
4. Format according to journal requirements
5. Polish and finalize manuscripts

Author: Archaeological Research Team
Version: 1.0.0
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict


@dataclass
class Literature:
    """Represents a single literature entry."""
    authors: str
    year: int
    title: str
    journal: str
    key_findings: str
    methods: str
    limitations: str
    category: str = ""
    notes: str = ""
    citation_key: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Literature':
        return cls(**data)


@dataclass
class ReviewOutline:
    """Represents the structure of a review article."""
    title: str
    sections: List[Dict[str, str]] = field(default_factory=list)
    target_journal: str = ""
    scope: str = ""
    time_range: str = ""
    review_type: str = "Comprehensive Review"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReviewOutline':
        return cls(**data)
    
    def add_section(self, section_title: str, description: str, subsections: List[str] = None):
        """Add a section to the outline."""
        section = {
            "title": section_title,
            "description": description,
            "subsections": subsections or []
        }
        self.sections.append(section)
    
    def display(self) -> str:
        """Display the outline in a formatted way."""
        output = [
            f"Review Article Outline",
            f"=" * 80,
            f"Title: {self.title}",
            f"Target Journal: {self.target_journal}",
            f"Review Type: {self.review_type}",
            f"Scope: {self.scope}",
            f"Time Range: {self.time_range}",
            f"\nStructure:",
            f"-" * 80
        ]
        
        for i, section in enumerate(self.sections, 1):
            output.append(f"\n{i}. {section['title']}")
            output.append(f"   Description: {section['description']}")
            if section.get('subsections'):
                for j, subsec in enumerate(section['subsections'], 1):
                    output.append(f"   {i}.{j} {subsec}")
        
        return "\n".join(output)


@dataclass
class ManuscriptSection:
    """Represents a drafted section of the manuscript."""
    section_name: str
    content: str
    references: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ManuscriptSection':
        return cls(**data)


class LiteratureManager:
    """Manages literature database and categorization."""
    
    def __init__(self, library_path: str = "literature_library.json"):
        self.library_path = library_path
        self.literature: List[Literature] = []
        self.load_library()
    
    def load_library(self):
        """Load existing literature library."""
        if os.path.exists(self.library_path):
            with open(self.library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.literature = [Literature.from_dict(lit) for lit in data]
    
    def save_library(self):
        """Save literature library to file."""
        with open(self.library_path, 'w', encoding='utf-8') as f:
            json.dump([lit.to_dict() for lit in self.literature], f, indent=2, ensure_ascii=False)
    
    def add_literature(self, lit: Literature):
        """Add a literature entry."""
        if not lit.citation_key:
            lit.citation_key = f"{lit.authors.split(',')[0].strip()}_{lit.year}"
        self.literature.append(lit)
        self.save_library()
    
    def categorize_by_theme(self) -> Dict[str, List[Literature]]:
        """Categorize literature by theme/category."""
        categories = {}
        for lit in self.literature:
            if lit.category not in categories:
                categories[lit.category] = []
            categories[lit.category].append(lit)
        return categories
    
    def filter_by_year_range(self, start_year: int, end_year: int) -> List[Literature]:
        """Filter literature by year range."""
        return [lit for lit in self.literature if start_year <= lit.year <= end_year]
    
    def search_literature(self, keyword: str) -> List[Literature]:
        """Search literature by keyword in title or key findings."""
        keyword_lower = keyword.lower()
        return [lit for lit in self.literature 
                if keyword_lower in lit.title.lower() or keyword_lower in lit.key_findings.lower()]
    
    def generate_bibliography(self, citation_format: str = "APA") -> List[str]:
        """Generate bibliography in specified format."""
        bibliography = []
        for lit in sorted(self.literature, key=lambda x: (x.authors, x.year)):
            if citation_format == "APA":
                bib_entry = f"{lit.authors} ({lit.year}). {lit.title}. {lit.journal}."
            elif citation_format == "IEEE":
                bib_entry = f"{lit.authors}, \"{lit.title},\" {lit.journal}, {lit.year}."
            else:  # Default
                bib_entry = f"{lit.authors}, {lit.year}. {lit.title}. {lit.journal}."
            bibliography.append(bib_entry)
        return bibliography


class ReviewArticleAssistant:
    """Main class for the review article writing assistant."""
    
    def __init__(self, project_name: str = "review_project"):
        self.project_name = project_name
        self.project_dir = f"review_projects/{project_name}"
        self.outline: Optional[ReviewOutline] = None
        self.literature_manager = LiteratureManager(
            os.path.join(self.project_dir, "literature_library.json")
        )
        self.manuscript_sections: List[ManuscriptSection] = []
        self._initialize_project()
    
    def _initialize_project(self):
        """Initialize project directory structure."""
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "drafts"), exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "figures"), exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "references"), exist_ok=True)
    
    def create_outline(self, title: str, target_journal: str, scope: str, 
                      time_range: str, review_type: str = "Comprehensive Review") -> ReviewOutline:
        """Create a new review article outline."""
        self.outline = ReviewOutline(
            title=title,
            target_journal=target_journal,
            scope=scope,
            time_range=time_range,
            review_type=review_type
        )
        
        # Add standard sections for a review article
        self.outline.add_section(
            "Abstract",
            "Concise summary of background, purpose, main findings, and conclusions (150-250 words)",
            []
        )
        
        self.outline.add_section(
            "Introduction",
            "Define research background, establish importance, state objectives, and outline structure",
            [
                "Research Background and Context",
                "Significance of the Problem",
                "Objectives and Scope of this Review",
                "Article Structure Overview"
            ]
        )
        
        self.outline.add_section(
            "Main Body",
            "Thematic organization of literature with critical analysis",
            [
                "Theme 1: [To be defined based on specific topic]",
                "Theme 2: [To be defined based on specific topic]",
                "Theme 3: [To be defined based on specific topic]"
            ]
        )
        
        self.outline.add_section(
            "Discussion and Critical Analysis",
            "Synthesize findings, identify patterns, evaluate methodologies, and discuss implications",
            [
                "Major Progress and Consensus",
                "Contradictions and Debates",
                "Methodological Evaluation",
                "Knowledge Gaps and Limitations"
            ]
        )
        
        self.outline.add_section(
            "Conclusion and Future Perspectives",
            "Summarize key insights and propose forward-looking research directions",
            [
                "Summary of Main Findings",
                "Unresolved Questions",
                "Future Research Directions",
                "Broader Implications"
            ]
        )
        
        self.outline.add_section(
            "References",
            "Complete bibliography in journal-required format",
            []
        )
        
        self.save_outline()
        return self.outline
    
    def save_outline(self):
        """Save outline to file."""
        if self.outline:
            outline_path = os.path.join(self.project_dir, "outline.json")
            with open(outline_path, 'w', encoding='utf-8') as f:
                json.dump(self.outline.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_outline(self):
        """Load outline from file."""
        outline_path = os.path.join(self.project_dir, "outline.json")
        if os.path.exists(outline_path):
            with open(outline_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.outline = ReviewOutline.from_dict(data)
    
    def draft_introduction(self, background: str, significance: str, 
                          objectives: str, structure_overview: str) -> ManuscriptSection:
        """
        Draft the introduction section with proper academic style.
        
        This method generates a well-structured introduction that:
        1. Establishes context and background
        2. Demonstrates significance
        3. States clear objectives
        4. Previews the article structure
        """
        content = f"""# Introduction

{background}

{significance}

{objectives}

{structure_overview}
"""
        section = ManuscriptSection(
            section_name="Introduction",
            content=content,
            notes="Generated introduction draft - requires refinement with specific citations"
        )
        self.manuscript_sections.append(section)
        return section
    
    def draft_section_with_synthesis(self, section_name: str, theme: str, 
                                     literature_refs: List[str], 
                                     critical_analysis: str) -> ManuscriptSection:
        """
        Draft a main body section with literature synthesis and critical analysis.
        
        This method avoids simple literature listing and instead:
        1. Presents a central argument or theme
        2. Synthesizes multiple sources
        3. Provides critical evaluation
        4. Identifies patterns and contradictions
        """
        content = f"""# {section_name}

{theme}

{critical_analysis}

**Key Literature:**
{'\n'.join([f"- {ref}" for ref in literature_refs])}
"""
        section = ManuscriptSection(
            section_name=section_name,
            content=content,
            references=literature_refs
        )
        self.manuscript_sections.append(section)
        return section
    
    def draft_conclusion(self, main_findings: str, knowledge_gaps: str, 
                        future_directions: str) -> ManuscriptSection:
        """
        Draft the conclusion and future perspectives section.
        
        This section:
        1. Summarizes major progress
        2. Highlights current consensus
        3. Identifies unresolved questions
        4. Proposes forward-looking research directions
        """
        content = f"""# Conclusion and Future Perspectives

## Summary of Main Findings

{main_findings}

## Knowledge Gaps and Unresolved Questions

{knowledge_gaps}

## Future Research Directions

{future_directions}

## Broader Implications

This review synthesizes current understanding and charts a path forward for advancing this field. 
The identified gaps and future directions provide a roadmap for researchers to address critical 
challenges and push the boundaries of knowledge.
"""
        section = ManuscriptSection(
            section_name="Conclusion and Future Perspectives",
            content=content
        )
        self.manuscript_sections.append(section)
        return section
    
    def generate_abstract(self, word_limit: int = 250) -> str:
        """
        Generate an abstract based on the drafted sections.
        
        The abstract includes:
        1. Background (1-2 sentences)
        2. Purpose and scope (1 sentence)
        3. Main findings/synthesis (2-3 sentences)
        4. Conclusions and implications (1-2 sentences)
        """
        abstract_template = f"""**Abstract**

[Background: 1-2 sentences establishing context and importance]

[Purpose: State the objectives and scope of this review]

[Main Findings: 2-3 sentences summarizing key insights and synthesis]

[Conclusions: 1-2 sentences on implications and future directions]

**Note:** This abstract should be refined to approximately {word_limit} words.
"""
        return abstract_template
    
    def export_manuscript(self, filename: str = None, format: str = "markdown"):
        """Export the complete manuscript."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"manuscript_{timestamp}.md"
        
        output_path = os.path.join(self.project_dir, "drafts", filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Title
            if self.outline:
                f.write(f"# {self.outline.title}\n\n")
                f.write(f"**Target Journal:** {self.outline.target_journal}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("---\n\n")
            
            # Abstract
            f.write(self.generate_abstract())
            f.write("\n\n---\n\n")
            
            # Main sections
            for section in self.manuscript_sections:
                f.write(section.content)
                f.write("\n\n")
                if section.references:
                    f.write("**References for this section:**\n")
                    for ref in section.references:
                        f.write(f"- {ref}\n")
                f.write("\n---\n\n")
            
            # Bibliography
            f.write("# References\n\n")
            bibliography = self.literature_manager.generate_bibliography()
            for i, bib in enumerate(bibliography, 1):
                f.write(f"{i}. {bib}\n")
        
        print(f"Manuscript exported to: {output_path}")
        return output_path
    
    def generate_writing_guidelines(self) -> str:
        """Generate comprehensive writing guidelines for top-tier review articles."""
        guidelines = """
# Academic Review Article Writing Guidelines
============================================

## Core Principles for Top-Tier Review Articles

### 1. Authoritative Voice
- Demonstrate comprehensive and deep understanding of the field
- Speak with confidence based on thorough literature analysis
- Position yourself as an expert guide through the literature

### 2. Critical Analysis (NOT Just Literature Listing)
**AVOID:**
- "Study A found X"
- "Study B found Y"  
- "Study C found Z"

**INSTEAD:**
- Present a theme or argument
- Use multiple studies to support, contrast, or debate the theme
- Evaluate methodological strengths and limitations
- Identify patterns and contradictions
- Explain discrepancies between conflicting findings

### 3. Synthesis Over Summary
- Integrate scattered findings into a coherent narrative
- Identify overarching themes and trends
- Build a "story" that connects past, present, and future
- Create new insights through synthesis

### 4. Structure and Organization
**Thematic Organization** (Recommended):
- Organize by key concepts or themes
- Allows deep exploration of each topic
- Facilitates critical comparison

**Chronological Organization**:
- Useful for historical development
- Shows evolution of ideas
- Best combined with thematic elements

**Methodological Organization**:
- Group by research approaches
- Compare different methodologies
- Evaluate technique strengths/limitations

### 5. Clear and Precise Academic Language
- Use concise, professional language
- Avoid unnecessary jargon
- Define technical terms when first introduced
- Maintain logical flow between paragraphs and sections
- Use transition sentences effectively

### 6. Introduction Best Practices
A strong introduction should:
1. Establish broad context (why does this field matter?)
2. Narrow to specific focus (what gap does this review fill?)
3. State clear objectives (what will this review accomplish?)
4. Preview structure (how is this review organized?)

**Example Framework:**
"Field X is undergoing fundamental transformation driven by Y [1,2]. Traditional approaches 
relied on Z, which had limitations A and B [3]. Recent advances in method M have shown 
potential to overcome these challenges [4-7]. However, widespread adoption faces obstacles 
including I, J, and K [8-10]. Therefore, this review aims to systematically examine... 
We focus on (1)..., (2)..., and (3)... The article is structured as follows: Section 2..."

### 7. Main Body Best Practices
For each thematic section:
1. **State the central question or theme**
2. **Present supporting evidence from literature**
   - Synthesize findings from multiple sources
   - Compare and contrast different approaches
3. **Provide critical evaluation**
   - What are the contributions?
   - What are the limitations?
   - How do studies relate to each other?
4. **Summarize current state of knowledge on this theme**

### 8. Conclusion and Future Perspectives
Should include:
1. **Synthesis of main progress** - What have we learned?
2. **Current consensus** - What do researchers agree on?
3. **Unresolved questions** - What remains unknown?
4. **Knowledge gaps** - Where are the blind spots?
5. **Future directions** - What should researchers do next?
6. **Broader implications** - Why does this matter?

**Make future directions:**
- Specific and actionable
- Forward-looking and innovative
- Grounded in identified gaps
- Potentially transformative

### 9. Citation and Reference Management
- Ensure all citations are accurate
- Use appropriate citation style (APA, IEEE, Vancouver, etc.)
- Cite seminal works and recent advances
- Balance citation distribution (avoid over-citing own work)
- Use citation management software

### 10. Quality Checks Before Submission
- [ ] Logical flow between all sections
- [ ] No unsupported claims
- [ ] All citations verified
- [ ] Consistent terminology throughout
- [ ] Meets journal word count requirements
- [ ] Figures and tables properly formatted
- [ ] Abstract accurately reflects content
- [ ] No grammatical or spelling errors
- [ ] Complies with journal formatting guidelines

## Common Pitfalls to Avoid

1. **Literature listing without synthesis**
2. **Lack of critical analysis**
3. **Insufficient coverage of recent literature**
4. **Ignoring contradictory findings**
5. **Poor logical organization**
6. **Vague or generic conclusions**
7. **Missing future perspectives**
8. **Inadequate citation of key works**

## Target Journal Considerations

**Nature Reviews, Science Reviews:**
- Extremely broad readership - minimize jargon
- Strong emphasis on future impact
- Exceptional figure quality required
- ~3000-5000 words typical

**Specialized Review Journals:**
- Can use more technical language
- Deeper methodological detail
- ~5000-8000 words typical

**Always check specific journal guidelines!**
"""
        return guidelines


def interactive_assistant():
    """Interactive command-line interface for the review article assistant."""
    print("=" * 80)
    print("Academic Review Article Writing Assistant")
    print("=" * 80)
    print("\nWelcome! This tool will help you write a high-quality review article")
    print("for top-tier academic journals.\n")
    
    project_name = input("Enter project name: ").strip() or "my_review"
    assistant = ReviewArticleAssistant(project_name)
    
    print(f"\nProject '{project_name}' initialized at: {assistant.project_dir}")
    print("\nWhat would you like to do?")
    print("1. Create new outline")
    print("2. View writing guidelines")
    print("3. Add literature entry")
    print("4. Draft introduction")
    print("5. Export manuscript")
    print("6. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n--- Create Review Article Outline ---")
            title = input("Review title: ").strip()
            target_journal = input("Target journal (e.g., Nature Reviews): ").strip()
            scope = input("Scope of review: ").strip()
            time_range = input("Time range (e.g., 2018-2024): ").strip()
            review_type = input("Review type (Comprehensive/Systematic/Meta-Analysis) [Comprehensive]: ").strip() or "Comprehensive Review"
            
            outline = assistant.create_outline(title, target_journal, scope, time_range, review_type)
            print("\n" + outline.display())
            
        elif choice == "2":
            print("\n" + assistant.generate_writing_guidelines())
            
        elif choice == "3":
            print("\n--- Add Literature Entry ---")
            authors = input("Authors: ").strip()
            try:
                year = int(input("Year: ").strip())
            except ValueError:
                print("Error: Year must be a number. Entry not added.")
                continue
            title = input("Title: ").strip()
            journal = input("Journal: ").strip()
            key_findings = input("Key findings: ").strip()
            methods = input("Methods: ").strip()
            limitations = input("Limitations: ").strip()
            category = input("Category/Theme: ").strip()
            
            lit = Literature(authors, year, title, journal, key_findings, methods, limitations, category)
            assistant.literature_manager.add_literature(lit)
            print(f"Literature added: {lit.citation_key}")
            
        elif choice == "4":
            print("\n--- Draft Introduction ---")
            print("Provide content for each subsection:\n")
            background = input("Background and context: ").strip()
            significance = input("Significance of the problem: ").strip()
            objectives = input("Objectives and scope: ").strip()
            structure = input("Structure overview: ").strip()
            
            section = assistant.draft_introduction(background, significance, objectives, structure)
            print("\nIntroduction drafted successfully!")
            
        elif choice == "5":
            filename = input("Output filename (press Enter for auto-generated): ").strip() or None
            path = assistant.export_manuscript(filename)
            print(f"Manuscript exported to: {path}")
            
        elif choice == "6":
            print("\nThank you for using the Academic Review Article Writing Assistant!")
            print("Good luck with your review article!")
            break
        
        else:
            print("Invalid choice. Please enter 1-6.")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_assistant()
    else:
        # Demonstration mode
        print("Academic Review Article Writing Assistant - Demonstration Mode")
        print("=" * 80)
        print("\nFor interactive mode, run: python review_article_assistant.py --interactive")
        print("\nThis tool provides comprehensive support for writing review articles,")
        print("including outline generation, literature management, section drafting,")
        print("and manuscript export.\n")
        
        # Create demo project
        demo = ReviewArticleAssistant("demo_project")
        
        # Create outline
        outline = demo.create_outline(
            title="Geometric Morphometrics in Archaeological Research: Methods, Applications, and Future Directions",
            target_journal="Journal of Archaeological Science",
            scope="Review of 2D and 3D geometric morphometric methods applied to archaeological artifacts",
            time_range="2010-2024",
            review_type="Comprehensive Review"
        )
        
        print("\nDemo outline created:")
        print(outline.display())
        
        # Add sample literature
        sample_lit = Literature(
            authors="Smith, J., Jones, A.",
            year=2020,
            title="Advances in Elliptic Fourier Analysis for Artifact Classification",
            journal="Journal of Archaeological Method and Theory",
            key_findings="EFA provides robust quantification of shape variation in ceramic vessels",
            methods="2D-GMM, EFA, PCA",
            limitations="Limited to 2D outlines, requires high-quality images",
            category="Methodological Development"
        )
        demo.literature_manager.add_literature(sample_lit)
        
        print("\nSample literature entry added.")
        print(f"\nProject files created in: {demo.project_dir}")
        print("\nRun with --interactive flag for full functionality.")


if __name__ == "__main__":
    main()
