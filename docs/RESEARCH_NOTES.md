# Literature review notes

The supplied report template asks for at least 15 sources from Q1/Q2 journals. The 15 articles below have publisher DOI records and come from five journals whose **2024 Journal Citation Reports JIF quartiles** are Q1 or Q2 in the categories shown below. The [institutional copy of the 2024 JCR list, released in June 2025](https://cdn.umfcluj.ro/uploads/2024/08/JCR_2024_iunie2025.pdf), gives the venue, category, and JIF quartile. Quartiles are journal-level and depend on the selected year, index, and subject category; these values do not state a rank for each article in its original publication year. These are background sources, **not** a claim that the game implements every method.

| Journal | 2024 JCR category | JIF quartile |
| --- | --- | --- |
| *Communications of the ACM* | Computer Science, Software Engineering | Q1 |
| *ACM Transactions on Graphics* | Computer Science, Software Engineering | Q1 |
| *Computer Graphics Forum* | Computer Science, Software Engineering | Q2 |
| *IEEE Transactions on Computers* | Computer Science, Hardware & Architecture | Q2 |
| *IEEE Transactions on Visualization and Computer Graphics* | Computer Science, Software Engineering | Q1 |

| No. | Article | Journal and DOI | Use in our report |
| --- | --- | --- | --- |
| 1 | Phong, “Illumination for computer generated pictures” (1975) | *Communications of the ACM*, [10.1145/360825.360839](https://doi.org/10.1145/360825.360839) | Ambient, diffuse, and specular shading background. |
| 2 | Gouraud, “Continuous Shading of Curved Surfaces” (1971) | *IEEE Transactions on Computers*, [10.1109/T-C.1971.223313](https://doi.org/10.1109/T-C.1971.223313) | Contrast per-vertex and our per-fragment lighting. |
| 3 | Cook and Torrance, “A Reflectance Model for Computer Graphics” (1982) | *ACM Transactions on Graphics*, [10.1145/357290.357293](https://doi.org/10.1145/357290.357293) | More advanced material model considered beyond scope. |
| 4 | Schlick, “An Inexpensive BRDF Model for Physically-based Rendering” (1994) | *Computer Graphics Forum*, [10.1111/1467-8659.1330233](https://doi.org/10.1111/1467-8659.1330233) | Fast reflectance approximation, beyond our course-scale shader. |
| 5 | Blinn and Newell, “Texture and reflection in computer generated images” (1976) | *Communications of the ACM*, [10.1145/360349.360353](https://doi.org/10.1145/360349.360353) | Texture coordinate mapping background. |
| 6 | Perlin, “Improving noise” (2002) | *ACM Transactions on Graphics*, [10.1145/566654.566636](https://doi.org/10.1145/566654.566636) | Procedural appearance as a possible extension; our floor uses a simple checker. |
| 7 | Lagae et al., “A Survey of Procedural Noise Functions” (2010) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2010.01827.x](https://doi.org/10.1111/j.1467-8659.2010.01827.x) | Why procedural textures can vary detail without image assets. |
| 8 | Reeves, “Particle Systems—a Technique for Modeling a Class of Fuzzy Objects” (1983) | *ACM Transactions on Graphics*, [10.1145/357318.357320](https://doi.org/10.1145/357318.357320) | Particle effects as future visual feedback, not current implementation. |
| 9 | Sloan, Kautz, and Snyder, “Precomputed radiance transfer for real-time rendering in dynamic, low-frequency lighting environments” (2002) | *ACM Transactions on Graphics*, [10.1145/566654.566612](https://doi.org/10.1145/566654.566612) | Lighting quality/performance tradeoff, beyond project scope. |
| 10 | Ritschel et al., “The State of the Art in Interactive Global Illumination” (2012) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2012.02093.x](https://doi.org/10.1111/j.1467-8659.2012.02093.x) | Explain why local lighting is sufficient for a small arena. |
| 11 | Klosowski et al., “Efficient collision detection using bounding volume hierarchies of k-DOPs” (1998) | *IEEE Transactions on Visualization and Computer Graphics*, [10.1109/2945.675649](https://doi.org/10.1109/2945.675649) | Compare broad-phase collision schemes with our small number of sphere checks. |
| 12 | Teschner et al., “Collision Detection for Deformable Objects” (2005) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2005.00829.x](https://doi.org/10.1111/j.1467-8659.2005.00829.x) | Complex collision cases outside the rigid projectile game. |
| 13 | Hasenfratz et al., “A Survey of Real-time Soft Shadows Algorithms” (2003) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2003.00722.x](https://doi.org/10.1111/j.1467-8659.2003.00722.x) | Shadows as an optional future enhancement. |
| 14 | Crassin et al., “Interactive Indirect Illumination Using Voxel Cone Tracing” (2011) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2011.02063.x](https://doi.org/10.1111/j.1467-8659.2011.02063.x) | Another advanced indirect light approach beyond our small shader. |
| 15 | Bourque and Dudek, “Procedural Texture Matching and Transformation” (2004) | *Computer Graphics Forum*, [10.1111/j.1467-8659.2004.00777.x](https://doi.org/10.1111/j.1467-8659.2004.00777.x) | Procedural texture design background; our repeating checker is intentionally simpler. |

Additional publisher cross-checks: [ACM journal report (2025)](https://www.acm.org/binaries/content/assets/press-releases/2025/july/news-release_impact_factors_2025_final.pdf) and [IEEE journal title list (2025)](https://open.ieee.org/wp-content/uploads/IEEE-Title-List-January-2025.pdf). The JCR source above supplies one consistent ranking measure for all five venues.
