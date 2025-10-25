===========================================================
📂 ESTRUTURA DE PASTAS CRIADA:
📁 dwarf_fortress_data/
  📁 metadata/
    📄 session_info.json - Session metadata and statistics
    📄 layout_info.json - Memory layout information
    📄 decoder_info.json - Decoder version and settings
  📁 dwarfs/
    📁 demographics/
      📁 by_profession/
        📄 fish_dissector_115/ - 43 dwarfs with profession 115
        📄 profession_103/ - 26 dwarfs with profession 103
        📄 profession_50/ - 25 dwarfs with profession 50
        📄 other_professions/ - 65 other profession types
      📁 by_age/
        📄 young_0_20/ - 61 dwarfs aged 0-20
        📄 adult_21_50/ - 51 dwarfs aged 21-50
        📄 mature_51_100/ - 109 dwarfs aged 51-100
        📄 elder_100plus/ - 19 dwarfs over 100
      📁 by_gender/
        📄 female/ - 105 female dwarfs
        📄 male/ - 138 male dwarfs
        📄 unknown/ - 8 unknown gender
      📁 by_civilization/
        📄 main_civ_287/ - 234 dwarfs from main civilization
        📄 other_civs/ - 17 dwarfs from other civilizations
    📁 skills/
      📁 by_category/
        📁 social_skills/
          📄 teaching/ - 211 dwarfs with Teaching skill
          📄 speaking/ - 211 dwarfs with Speaking skill
          📄 flattery/ - 211 dwarfs with Flattery skill
          📄 leadership/ - 206 dwarfs with Leadership skill
        📁 combat_skills/
          📄 weapon_skills/ - Various weapon proficiencies
          📄 armor_skills/ - Armor user skills
          📄 tactics/ - Military tactical skills
        📁 craft_skills/
          📄 mining/ - Mining and excavation
          📄 smithing/ - Metalworking skills
          📄 carpentry/ - Woodworking skills
      📁 by_level/
        📄 novice_0_1/ - 4839 skills at novice level
        📄 adequate_2_5/ - 1359 skills at adequate level
        📄 professional_6plus/ - 302 skills at professional+ level
      📁 skill_combinations/
        📄 specialists/ - Dwarfs with 1-3 high skills
        📄 generalists/ - Dwarfs with many low skills
        📄 masters/ - Dwarfs with level 15+ skills
    📁 attributes/
      📁 physical/
        📁 strength/
          📄 very_low_0_20/ - 880 attributes (58.4%)
          📄 low_21_40/ - 37 attributes (2.5%)
          📄 medium_41_60/ - 223 attributes (14.8%)
          📄 high_61_80/ - 8 attributes (0.5%)
          📄 very_high_81_100/ - 22 attributes (1.5%)
        📄 agility/ - 251 agility measurements
        📄 toughness/ - 251 toughness measurements
        📄 endurance/ - 251 endurance measurements
        📄 recuperation/ - 251 recuperation measurements
        📄 disease_resistance/ - 251 disease resistance measurements
      📁 mental/
        📄 analytical_ability/ - 251 analytical measurements
        📄 creativity/ - Mental creativity scores
        📄 intuition/ - Intuitive thinking scores
        📄 patience/ - Patience measurements
        📄 memory/ - Memory capacity scores
        📄 focus/ - Focus ability scores
        📄 willpower/ - Willpower measurements
    📁 labors/
      📁 enabled/
        📄 hunt/ - 166 dwarfs (66.1%) enabled
        📄 mine/ - 10 dwarfs (4.0%) enabled
        📄 other_labors/ - 10 other labor types with low enablement
      📁 disabled/
        📄 all_others/ - Most labors disabled for most dwarfs
      📁 by_type/
        📄 outdoor/ - Hunt, Fish, Cut Wood
        📄 workshop/ - Carpentry, Stonework, Engraving
        📄 animal/ - Animal Care, Animal Training
        📄 food/ - Butcher, related food labors
    📁 health/
      📁 wounds/
        📁 by_severity/
          📄 extreme_pain_100plus/ - 132 wounds (74.6%)
          📄 severe_pain_51_100/ - 7 wounds (4.0%)
          📄 moderate_pain_26_50/ - 2 wounds (1.1%)
          📄 light_pain_1_25/ - 22 wounds (12.4%)
        📁 by_body_part/
          📄 part_0/ - 9 wounds
          📄 part_2126345456/ - 1 wound
          📄 other_parts/ - Various body part IDs
        📄 wounded_dwarfs/ - 59 dwarfs with wounds (23.5%)
        📄 healthy_dwarfs/ - 192 dwarfs without wounds (76.5%)
      📁 status_flags/
        📄 dead/ - 35 dwarfs (13.9%)
        📄 caged/ - 0 dwarfs
        📄 butcher_marked/ - 0 dwarfs
        📄 in_mood/ - 0 dwarfs
        📄 normal/ - 216 dwarfs in normal state
    📁 equipment/
      📁 by_type/
        📄 none_type/ - 1877 items marked as 'None'
        📄 weapons/ - Weapon category items
        📄 armor/ - Armor and protection
        📄 tools/ - Workshop and utility tools
      📁 by_quality/
        📄 quality_4294901760/ - 513 items (27.3%)
        📄 basic/ - 187 items (10.0%)
        📄 well_crafted/ - 2 items
        📄 superior/ - 1 item
        📄 masterwork/ - 1 item
        📄 unknown_qualities/ - 1173 items with undefined quality
      📁 by_material/
        📄 no_material/ - 4 items
        📄 unknown_materials/ - 1873 items with unknown material IDs
      📄 equipped_dwarfs/ - 200 dwarfs with equipment (79.7%)
      📄 unequipped_dwarfs/ - 51 dwarfs without equipment (20.3%)
    📁 personality/
      📁 traits/
        📁 dominant_traits/
          📄 gluttony/ - 177 dwarfs
          📄 laziness/ - 177 dwarfs
          📄 curiosity/ - 159 dwarfs
          📄 immoderation/ - 159 dwarfs
          📄 chastity/ - 139 dwarfs
          📄 modesty/ - 139 dwarfs
        📁 rare_traits/
          📄 mercy/ - 27 dwarfs
          📄 temperance/ - 27 dwarfs
          📄 justice/ - 111 dwarfs
        📁 trait_tendencies/
          📄 high_tendency/ - 1255 trait instances
          📄 other_tendencies/ - Other tendency levels
      📁 stress_levels/
        📄 no_stress_0_100/ - 0 dwarfs
        📄 low_stress_101_1000/ - 1 dwarf (0.4%)
        📄 medium_stress_1001_5000/ - 250 dwarfs (99.6%)
        📄 high_stress_5000plus/ - 0 dwarfs
      📁 focus_levels/
        📄 normal_focus/ - Most dwarfs
        📄 other_focus/ - Varying focus levels
    📁 organization/
      📁 squads/
        📄 civilians/ - 237 dwarfs not in squads
        📄 squad_149/ - 10 dwarfs in squad 149
        📄 squad_125/ - 4 dwarfs in squad 125
      📁 pets/
        📄 pet_owners/ - 19 dwarfs own pets
        📄 non_owners/ - 232 dwarfs don't own pets
  📁 analysis/
    📁 grouping_strategies/
      📁 functional_groups/
        📄 warriors/ - Squad members + combat skills
        📄 workers/ - Multiple enabled labors
        📄 specialists/ - Single high-level skill focus
        📄 managers/ - Leadership + social skills
      📁 experience_groups/
        📄 veterans/ - Age 50+ + multiple high skills
        📄 skilled_workers/ - Age 30-50 + specialized skills
        📄 apprentices/ - Age 20-30 + developing skills
        📄 children/ - Age <20 + basic skills
      📁 status_groups/
        📄 elite/ - High attributes + good equipment + no wounds
        📄 standard/ - Average stats + some equipment
        📄 struggling/ - Low stats + minimal equipment + wounds
        📄 disabled/ - Severe wounds or negative flags
    📁 correlations/
      📄 skill_age_correlation/ - Analysis of skills vs age
      📄 attribute_performance/ - Physical vs mental attributes
      📄 wound_recovery/ - Health tracking over time
    📁 anomalies/
      📄 negative_ages/ - Dwarfs with age -4 billion
      📄 unknown_equipment/ - Items with undefined types
      📄 strange_qualities/ - Equipment with odd quality values
  📁 exports/
    📁 raw_data/
      📄 complete_dwarves_data_20251025_135840.json - Full dataset
      📄 metadata_export.json - Metadata only
      📄 skills_export.json - Skills data only
    📁 processed_data/
      📄 dwarf_demographics.csv - Demographics in CSV
      📄 skills_matrix.csv - Skills cross-reference
      📄 health_status.csv - Health and wounds data
    📁 reports/
      📄 structure_analysis.md - This structure documentation
      📄 statistical_summary.pdf - Statistical analysis report
      📄 grouping_recommendations.md - Grouping strategy recommendations

