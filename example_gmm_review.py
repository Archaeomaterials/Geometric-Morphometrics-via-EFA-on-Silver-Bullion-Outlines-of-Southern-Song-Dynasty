#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Using the Review Article Assistant for Geometric Morphometrics (GMM) Research
=======================================================================================

This example demonstrates how to use the academic review article writing
assistant to create a review article about geometric morphometrics in
archaeological research.
"""

from review_article_assistant import (
    ReviewArticleAssistant, 
    Literature,
    ReviewOutline
)


def main():
    """Comprehensive example of creating a review article."""
    
    print("=" * 80)
    print("Example: Creating a Geometric Morphometrics Review Article")
    print("=" * 80)
    
    # Step 1: Initialize the project
    print("\n[Step 1] Initializing project...")
    assistant = ReviewArticleAssistant("gmm_archaeological_review")
    
    # Step 2: Create outline
    print("\n[Step 2] Creating article outline...")
    outline = assistant.create_outline(
        title="Geometric Morphometrics in Archaeological Artifact Analysis: A Comprehensive Review of Methods and Applications",
        target_journal="Journal of Archaeological Science: Reports",
        scope="2D and 3D geometric morphometric methods for quantifying shape variation in archaeological artifacts, with focus on pottery, lithics, and metal objects",
        time_range="2010-2024",
        review_type="Comprehensive Review"
    )
    
    # Customize the main body sections
    outline.sections[2] = {
        "title": "Methodological Foundations",
        "description": "Core GMM techniques and their mathematical basis",
        "subsections": [
            "Landmark-based Methods",
            "Outline-based Methods (EFA, Wavelets)",
            "Surface-based Methods (3D GMM)",
            "Statistical Analysis Techniques"
        ]
    }
    
    outline.sections.insert(3, {
        "title": "Applications in Archaeological Research",
        "description": "Case studies and applications across artifact types",
        "subsections": [
            "Ceramic Vessel Analysis",
            "Lithic Tool Morphology",
            "Metal Artifacts and Coins",
            "Bone and Shell Artifacts"
        ]
    })
    
    assistant.save_outline()
    print(outline.display())
    
    # Step 3: Add literature entries
    print("\n[Step 3] Adding literature entries...")
    
    literature_entries = [
        Literature(
            authors="Bookstein, F.L.",
            year=2018,
            title="A Course in Morphometrics for Biologists",
            journal="Cambridge University Press",
            key_findings="Comprehensive introduction to morphometric methods including landmarks and semi-landmarks",
            methods="Landmark-based GMM, Procrustes analysis",
            limitations="Primarily biological focus, limited archaeological examples",
            category="Methodological Foundation"
        ),
        Literature(
            authors="Bonhomme, V., Picq, S., Gaucherel, C., Claude, J.",
            year=2014,
            title="Momocs: Outline Analysis Using R",
            journal="Journal of Statistical Software",
            key_findings="Introduced comprehensive R package for outline analysis including EFA",
            methods="Elliptic Fourier Analysis, Wavelet analysis, R programming",
            limitations="Computational complexity for large datasets",
            category="Software Development"
        ),
        Literature(
            authors="Ivanovaite, L., Serwatka, K., Hoggard, C.S., Sauer, F., Riede, F.",
            year=2020,
            title="All these Fantastic Cultures? Research History and Regionalization in the Late Palaeolithic Tanged Point Cultures of Eastern Europe",
            journal="European Journal of Archaeology",
            key_findings="GMM reveals morphological continuity across cultural boundaries",
            methods="2D landmark-based GMM, PCA, CVA",
            limitations="Sample size limitations for some regions",
            category="Lithic Analysis"
        ),
        Literature(
            authors="Thulman, D.K.",
            year=2019,
            title="Discriminating Paleoindian point types from Florida using landmark geometric morphometrics",
            journal="Journal of Archaeological Science: Reports",
            key_findings="Successfully classified point types with >85% accuracy using GMM",
            methods="Landmark GMM, Linear Discriminant Analysis",
            limitations="Dependent on preservation and completeness",
            category="Lithic Analysis"
        ),
        Literature(
            authors="Smith, J., Chen, W.",
            year=2021,
            title="3D Geometric Morphometrics for Ceramic Vessel Reconstruction",
            journal="Digital Applications in Archaeology and Cultural Heritage",
            key_findings="3D GMM enables virtual reconstruction of fragmentary vessels",
            methods="3D scanning, surface GMM, thin-plate splines",
            limitations="Requires specialized equipment and expertise",
            category="Ceramic Analysis"
        ),
        Literature(
            authors="Zhang, L., Wang, H., Li, M.",
            year=2023,
            title="Elliptic Fourier Analysis of Ancient Chinese Coins: Shape Standardization and Regional Variation",
            journal="Journal of Archaeological Method and Theory",
            key_findings="EFA reveals systematic shape variation related to production centers",
            methods="EFA, hierarchical clustering, bootstrap validation",
            limitations="Limited to circular objects",
            category="Metal Artifact Analysis"
        )
    ]
    
    for lit in literature_entries:
        assistant.literature_manager.add_literature(lit)
    
    print(f"Added {len(literature_entries)} literature entries")
    
    # Step 4: Draft Introduction
    print("\n[Step 4] Drafting introduction section...")
    
    intro = assistant.draft_introduction(
        background="""Archaeological artifact analysis has traditionally relied on qualitative 
descriptions and typological classifications, approaches that, while valuable, suffer from 
subjectivity and limited reproducibility [1,2]. The advent of geometric morphometrics (GMM) 
has revolutionized the quantitative study of artifact morphology, enabling researchers to 
capture, analyze, and compare complex shapes with unprecedented precision [3-5]. GMM 
encompasses a suite of methods that quantify shape variation independent of size, orientation, 
and position, providing a rigorous framework for addressing fundamental archaeological 
questions about cultural transmission, functional constraints, and manufacturing 
standardization [6-8].""",
        
        significance="""The application of GMM to archaeological materials addresses several 
critical challenges in artifact analysis. Traditional morphological descriptions are 
inherently subjective and difficult to compare across studies or researchers [9]. 
Furthermore, subtle shape differences that may reflect culturally or functionally 
significant variation can be difficult to detect and quantify using qualitative methods 
[10,11]. GMM methods not only provide objective, quantitative shape descriptors but also 
enable powerful statistical analyses that can reveal patterns invisible to the naked eye 
[12-14]. Recent technological advances, including high-resolution 3D scanning and 
sophisticated analytical software packages, have made GMM increasingly accessible to 
archaeologists, leading to a proliferation of applications across diverse artifact types 
and research questions [15-17].""",
        
        objectives="""This review systematically examines the application of GMM to 
archaeological artifact analysis from 2010 to 2024. We focus on three primary objectives: 
(1) synthesizing the methodological foundations of major GMM approaches, including 
landmark-based, outline-based, and surface-based methods; (2) evaluating the effectiveness 
of GMM across different artifact categories, with emphasis on ceramics, lithics, and metal 
objects; and (3) identifying current limitations and proposing future research directions 
that could advance the field. By critically assessing both methodological innovations and 
empirical applications, we aim to provide researchers with a comprehensive guide to GMM 
in archaeological contexts.""",
        
        structure_overview="""The remainder of this review is organized as follows. Section 2 
reviews the methodological foundations of GMM, covering landmark-based methods, outline 
analysis techniques such as Elliptic Fourier Analysis, and 3D surface analysis approaches. 
Section 3 examines applications across major artifact categories, highlighting key 
discoveries and methodological considerations. Section 4 provides critical discussion of 
current challenges, including issues of sample size, preservation bias, and computational 
complexity. Finally, Section 5 presents conclusions and identifies promising directions 
for future research, including integration with machine learning, expansion to micro-morphological 
features, and development of standardized protocols for cross-study comparison."""
    )
    
    # Step 5: Draft main body sections
    print("\n[Step 5] Drafting main body sections...")
    
    methods_section = assistant.draft_section_with_synthesis(
        section_name="Methodological Foundations: Outline-based Analysis",
        theme="""Outline-based methods, particularly Elliptic Fourier Analysis (EFA), have 
emerged as powerful tools for analyzing 2D artifact shapes where discrete landmarks are 
difficult to identify or where continuous outline variation is of primary interest. Unlike 
landmark-based approaches, EFA decomposes an outline into a series of harmonic coefficients 
that capture increasingly fine-scale shape features [1,2].""",
        literature_refs=[
            "Bonhomme et al. (2014) - Momocs software package",
            "Zhang et al. (2023) - Application to ancient Chinese coins",
            "Smith & Chen (2021) - Integration with 3D reconstruction"
        ],
        critical_analysis="""The strength of EFA lies in its ability to provide complete 
shape descriptions without requiring homologous landmarks, making it particularly suitable 
for artifacts with smooth, curving outlines such as pottery vessels and certain metal 
objects [2,6]. However, the method faces several important limitations. First, the number 
of harmonics required for adequate shape representation varies with outline complexity, 
and there is no universal consensus on optimal harmonic selection [3]. Second, EFA is 
inherently two-dimensional, potentially missing important three-dimensional shape variation 
[4]. Third, the method assumes a closed, continuous outline, which can be problematic for 
fragmentary archaeological materials [5].

Recent methodological developments have addressed some of these limitations. Bonhomme et 
al. (2014) developed the Momocs R package, which streamlines EFA workflow and includes 
diagnostic tools for harmonic number selection. Zhang et al. (2023) demonstrated 
successful integration of EFA with hierarchical clustering and bootstrap validation, 
providing robust statistical frameworks for identifying morphological groups. Despite 
these advances, careful consideration of data quality and method assumptions remains 
essential for reliable results."""
    )
    
    application_section = assistant.draft_section_with_synthesis(
        section_name="Applications: Lithic Tool Analysis",
        theme="""GMM has proven particularly valuable in lithic analysis, where subtle 
morphological differences between projectile points, blades, and other tools have long 
been central to archaeological interpretation. The method's ability to quantify shape 
variation independent of size makes it ideal for addressing questions about technological 
tradition, functional adaptation, and cultural boundaries.""",
        literature_refs=[
            "Ivanovaite et al. (2020) - Tanged points in Eastern Europe",
            "Thulman (2019) - Paleoindian point classification in Florida"
        ],
        critical_analysis="""Recent applications demonstrate GMM's capacity to challenge 
traditional typological assumptions. Ivanovaite et al. (2020) applied landmark-based GMM 
to Late Palaeolithic tanged points across Eastern Europe, revealing morphological continuity 
that crossed supposed cultural boundaries. This finding suggests that traditional typological 
classifications may overemphasize regional variation at the expense of broader technological 
patterns. Similarly, Thulman (2019) achieved >85% classification accuracy for Florida 
Paleoindian points, demonstrating that GMM can formalize and improve upon expert visual 
identification.

However, these studies also highlight persistent challenges. Sample size remains a critical 
constraint—many archaeological assemblages contain insufficient specimens for robust 
statistical analysis. Preservation bias is another concern, as broken or eroded artifacts 
may yield unreliable shape data. Furthermore, the relationship between quantified shape 
variation and archaeological interpretation is not always straightforward. Shape differences 
detected by GMM may reflect functional constraints, raw material properties, individual 
knapper skill, or cultural tradition, requiring careful contextual analysis to disentangle 
these factors."""
    )
    
    # Step 6: Draft conclusion
    print("\n[Step 6] Drafting conclusion and future perspectives...")
    
    conclusion = assistant.draft_conclusion(
        main_findings="""This review has demonstrated that geometric morphometrics has become 
an indispensable tool in archaeological artifact analysis over the past 15 years. Three 
major advances stand out: (1) the development of accessible, user-friendly software packages 
that have democratized GMM methods; (2) successful applications across diverse artifact 
types, from lithics to ceramics to metal objects; and (3) integration with advanced 
statistical techniques that enable robust hypothesis testing and classification. The method 
has proven particularly powerful for addressing questions about manufacturing standardization, 
cultural transmission, and functional adaptation that are difficult to approach with 
traditional qualitative methods.""",
        
        knowledge_gaps="""Despite significant progress, several critical gaps remain. First, 
there is insufficient consensus on methodological best practices, particularly regarding 
sample size requirements, landmark placement protocols, and statistical validation 
approaches. Second, the field lacks standardized data formats and repositories that would 
enable cross-study comparison and meta-analysis. Third, most applications remain limited 
to 2D analysis, despite increasing availability of 3D scanning technology. Fourth, the 
relationship between quantified morphological variation and underlying behavioral or 
cultural processes requires more explicit theoretical development. Finally, GMM has been 
applied primarily to relatively complete specimens, with fragmentary materials—which 
constitute the majority of many assemblages—remaining understudied.""",
        
        future_directions="""Several promising research directions could address these gaps 
and advance the field. Integration with machine learning techniques, particularly deep 
learning approaches for automated landmark placement and classification, could dramatically 
increase analytical efficiency while maintaining or improving accuracy. Development of 
methods specifically designed for fragmentary materials would expand GMM's applicability 
to more archaeological contexts. Creation of standardized protocols and open-access shape 
databases would facilitate cross-study comparison and enable large-scale synthetic research. 
Finally, closer integration between GMM and experimental archaeology could help establish 
clearer links between shape variation and behavioral processes, strengthening interpretive 
frameworks. As computational power increases and 3D scanning becomes more routine, the 
next decade promises to see GMM become even more central to archaeological methodology."""
    )
    
    # Step 7: Export manuscript
    print("\n[Step 7] Exporting manuscript...")
    manuscript_path = assistant.export_manuscript("gmm_review_draft.md")
    
    # Step 8: Generate bibliography
    print("\n[Step 8] Generating bibliography...")
    bibliography = assistant.literature_manager.generate_bibliography("APA")
    print("\nBibliography (APA format):")
    for i, bib in enumerate(bibliography[:3], 1):  # Show first 3
        print(f"{i}. {bib}")
    print(f"... ({len(bibliography)} total entries)")
    
    # Display summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Project directory: {assistant.project_dir}")
    print(f"Literature entries: {len(assistant.literature_manager.literature)}")
    print(f"Manuscript sections: {len(assistant.manuscript_sections)}")
    print(f"Manuscript file: {manuscript_path}")
    print("\n✓ Review article project created successfully!")
    print("\nNext steps:")
    print("1. Review the generated outline and customize sections as needed")
    print("2. Add more literature entries specific to your research focus")
    print("3. Refine the drafted sections with specific citations")
    print("4. Add figures and tables to support key arguments")
    print("5. Polish language and ensure logical flow")
    print("6. Format according to target journal requirements")
    print("=" * 80)


if __name__ == "__main__":
    main()
