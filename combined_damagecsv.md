# ActionPriorityLists\rogue_subtlety.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=apply_poison
actions.precombat+=/flask
actions.precombat+=/augmentation
actions.precombat+=/food
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/stealth
actions.precombat+=/variable,name=algethar_puzzle_box_precombat_cast,value=3
actions.precombat+=/use_item,name=algethar_puzzle_box
actions.precombat+=/slice_and_dice,precombat_seconds=1

# Executed every time the actor is available.
# Restealth if possible (no vulnerable enemies in combat)
actions=stealth
# Interrupt on cooldown to allow simming interactions with that
actions+=/kick
# Used to determine whether cooldowns wait for SnD based on targets.
actions+=/variable,name=snd_condition,value=buff.slice_and_dice.up|spell_targets.shuriken_storm>=cp_max_spend
# Check CDs at first
actions+=/call_action_list,name=cds
# Apply Slice and Dice at 4+ CP if it expires within the next GCD or is not up
actions+=/slice_and_dice,if=spell_targets.shuriken_storm<cp_max_spend&buff.slice_and_dice.remains<gcd.max&fight_remains>6&combo_points>=4
# Run fully switches to the Stealthed Rotation (by doing so, it forces pooling if nothing is available).
actions+=/run_action_list,name=stealthed,if=stealthed.all
# Only change rotation if we have priority_rotation set.
actions+=/variable,name=priority_rotation,value=priority_rotation
# Used to define when to use stealth CDs or builders
actions+=/variable,name=stealth_threshold,value=20+talent.vigor.rank*25+talent.thistle_tea*20+talent.shadowcraft*20
actions+=/variable,name=stealth_helper,value=energy>=variable.stealth_threshold
actions+=/variable,name=stealth_helper,value=energy.deficit<=variable.stealth_threshold,if=!talent.vigor|talent.shadowcraft
# Consider using a Stealth CD when reaching the energy threshold
actions+=/call_action_list,name=stealth_cds,if=variable.stealth_helper|talent.invigorating_shadowdust
actions+=/call_action_list,name=finish,if=effective_combo_points>=cp_max_spend
# Finish at maximum or close to maximum combo point value
actions+=/call_action_list,name=finish,if=combo_points.deficit<=1|fight_remains<=1&effective_combo_points>=3
actions+=/call_action_list,name=finish,if=spell_targets.shuriken_storm>=4&effective_combo_points>=4
# Use a builder when reaching the energy threshold
actions+=/call_action_list,name=build,if=energy.deficit<=variable.stealth_threshold
# Lowest priority in all of the APL because it causes a GCD
actions+=/arcane_torrent,if=energy.deficit>=15+energy.regen
actions+=/arcane_pulse
actions+=/lights_judgment
actions+=/bag_of_tricks

# Builders  Keep using Shuriken Storm for Lingering Shadows on high stacks.
actions.build=shuriken_storm,if=spell_targets>=2+(talent.gloomblade&buff.lingering_shadow.remains>=6|buff.perforated_veins.up)
actions.build+=/gloomblade
actions.build+=/backstab

# Cooldowns  Helper Variable for Flagellation for trinket synchronisation
actions.cds=variable,name=trinket_conditions,value=(!equipped.witherbarks_branch|equipped.witherbarks_branch&trinket.witherbarks_branch.cooldown.remains<=8|equipped.bandolier_of_twisted_blades|talent.invigorating_shadowdust)
# Cold Blood on 5 combo points when not playing Secret Technique
actions.cds+=/cold_blood,if=!talent.secret_technique&combo_points>=5
actions.cds+=/sepsis,if=variable.snd_condition&target.time_to_die>=16&(buff.perforated_veins.up|!talent.perforated_veins)
# Defines Flagellation use in a stacked manner with trinkets and Shadow Blades
actions.cds+=/flagellation,target_if=max:target.time_to_die,if=variable.snd_condition&combo_points>=5&target.time_to_die>10&(variable.trinket_conditions&cooldown.shadow_blades.remains<=3|fight_remains<=28|cooldown.shadow_blades.remains>=14&talent.invigorating_shadowdust&talent.double_dance)&(!talent.invigorating_shadowdust|talent.sepsis|!talent.double_dance|talent.invigorating_shadowdust.rank=2&spell_targets.shuriken_storm>=2|cooldown.symbols_of_death.remains<=3|buff.symbols_of_death.remains>3)
# Align Symbols of Death to Flagellation.
actions.cds+=/symbols_of_death,if=variable.snd_condition&(!buff.the_rotten.up|!set_bonus.tier30_2pc)&buff.symbols_of_death.remains<=3&(!talent.flagellation|cooldown.flagellation.remains>10|buff.shadow_dance.remains>=2&talent.invigorating_shadowdust|cooldown.flagellation.up&combo_points>=5&!talent.invigorating_shadowdust)
# Align Shadow Blades to Flagellation.
actions.cds+=/shadow_blades,if=variable.snd_condition&(combo_points<=1|set_bonus.tier31_4pc)&(buff.flagellation_buff.up|buff.flagellation_persist.up|!talent.flagellation)
# ER during Shadow Dance.
actions.cds+=/echoing_reprimand,if=variable.snd_condition&combo_points.deficit>=3
# Shuriken Tornado with Symbols of Death on 3 and more targets
actions.cds+=/shuriken_tornado,if=variable.snd_condition&buff.symbols_of_death.up&combo_points<=2&!buff.premeditation.up&(!talent.flagellation|cooldown.flagellation.remains>20)&spell_targets.shuriken_storm>=3
# Shuriken Tornado only outside of cooldowns
actions.cds+=/shuriken_tornado,if=variable.snd_condition&!buff.shadow_dance.up&!buff.flagellation_buff.up&!buff.flagellation_persist.up&!buff.shadow_blades.up&spell_targets.shuriken_storm<=2&!raid_event.adds.up
actions.cds+=/shadow_dance,if=!buff.shadow_dance.up&fight_remains<=8+talent.subterfuge.enabled
# Goremaws Bite during Shadow Dance if possible.
actions.cds+=/goremaws_bite,if=variable.snd_condition&combo_points.deficit>=3&(!cooldown.shadow_dance.up|talent.double_dance&buff.shadow_dance.up&!talent.invigorating_shadowdust|spell_targets.shuriken_storm<4&!talent.invigorating_shadowdust|talent.the_rotten|raid_event.adds.up)
# Thistle Tea during Shadow Dance when close to max stacks.
actions.cds+=/thistle_tea,if=!buff.thistle_tea.up&cooldown.thistle_tea.charges_fractional>=2.5&buff.shadow_dance.remains>=4
# Thistle Tea during Shadow Dance when Secret Techniques is up.
actions.cds+=/thistle_tea,if=!buff.thistle_tea.up&buff.shadow_dance.remains>=4&cooldown.secret_technique.remains<=10
# Thistle Tea for energy
actions.cds+=/thistle_tea,if=!buff.thistle_tea.up&(energy.deficit>=(100)|!buff.thistle_tea.up&fight_remains<=(6*cooldown.thistle_tea.charges))&(cooldown.symbols_of_death.remains>=3|buff.symbols_of_death.up)&combo_points.deficit>=2
actions.cds+=/potion,if=buff.bloodlust.react|fight_remains<30|buff.symbols_of_death.up&(buff.shadow_blades.up|cooldown.shadow_blades.remains<=10)
actions.cds+=/variable,name=racial_sync,value=buff.shadow_blades.up|!talent.shadow_blades&buff.symbols_of_death.up|fight_remains<20
actions.cds+=/blood_fury,if=variable.racial_sync
actions.cds+=/berserking,if=variable.racial_sync
actions.cds+=/fireblood,if=variable.racial_sync
actions.cds+=/ancestral_call,if=variable.racial_sync
# Sync specific trinkets to Flagellation or Shadow Dance.
actions.cds+=/use_item,name=ashes_of_the_embersoul,if=(buff.cold_blood.up|(!talent.danse_macabre&buff.shadow_dance.up|buff.danse_macabre.stack>=3)&!talent.cold_blood)|fight_remains<10
actions.cds+=/use_item,name=witherbarks_branch,if=buff.flagellation_buff.up&talent.invigorating_shadowdust|buff.shadow_blades.up|equipped.bandolier_of_twisted_blades&raid_event.adds.up
actions.cds+=/use_item,name=mirror_of_fractured_tomorrows,if=buff.shadow_dance.up&(target.time_to_die>=15|equipped.ashes_of_the_embersoul)
actions.cds+=/use_item,name=beacon_to_the_beyond,use_off_gcd=1,if=!stealthed.all&(buff.deeper_daggers.up|!talent.deeper_daggers)&(!raid_event.adds.up|!equipped.stormeaters_boon|trinket.stormeaters_boon.cooldown.remains>20)
actions.cds+=/use_item,name=manic_grieftorch,use_off_gcd=1,if=!stealthed.all&(!raid_event.adds.up|!equipped.stormeaters_boon|trinket.stormeaters_boon.cooldown.remains>20)
# PI
actions.cds+=/invoke_external_buff,name=power_infusion,if=buff.shadow_dance.up
# Default fallback for usable items: Use outside of Stealth/Shadow Dance.
actions.cds+=/use_items,if=!stealthed.all&(!trinket.mirror_of_fractured_tomorrows.cooldown.ready|!equipped.mirror_of_fractured_tomorrows)&(!trinket.ashes_of_the_embersoul.cooldown.ready|!equipped.ashes_of_the_embersoul)|fight_remains<10

# Finisher  Defines what abilities need to be used for DM stacks before casting Secret Technique.
actions.finish=variable,name=secret_condition,value=(action.gloomblade.used_for_danse|action.shadowstrike.used_for_danse|action.backstab.used_for_danse|action.shuriken_storm.used_for_danse)&(action.eviscerate.used_for_danse|action.black_powder.used_for_danse|action.rupture.used_for_danse)|!talent.danse_macabre
# Apply Rupture if its not up.
actions.finish+=/rupture,if=!dot.rupture.ticking&target.time_to_die-remains>6
actions.finish+=/variable,name=premed_snd_condition,value=talent.premeditation.enabled&spell_targets.shuriken_storm<5
# Refresh Slice and Dice outside of Shadow Dance.
actions.finish+=/slice_and_dice,if=!stealthed.all&!variable.premed_snd_condition&spell_targets.shuriken_storm<6&!buff.shadow_dance.up&buff.slice_and_dice.remains<fight_remains&refreshable
# Variable to decide when not to use Rupture.
actions.finish+=/variable,name=skip_rupture,value=buff.thistle_tea.up&spell_targets.shuriken_storm=1|buff.shadow_dance.up&(spell_targets.shuriken_storm=1|dot.rupture.ticking&spell_targets.shuriken_storm>=2)
actions.finish+=/rupture,if=(!variable.skip_rupture|variable.priority_rotation)&target.time_to_die-remains>6&refreshable
# Refresh Rupture during Shadow Dance with Finality.
actions.finish+=/rupture,if=buff.finality_rupture.up&buff.shadow_dance.up&spell_targets.shuriken_storm<=4&!action.rupture.used_for_danse
actions.finish+=/cold_blood,if=variable.secret_condition&cooldown.secret_technique.ready
# Synchronizes Secret to Cold Blood if possible. Defaults to use once a builder and finisher is used.
actions.finish+=/secret_technique,if=variable.secret_condition&(!talent.cold_blood|cooldown.cold_blood.remains>buff.shadow_dance.remains-2|!talent.improved_shadow_dance)
# Multidotting targets that will live long enough, refresh during pandemic.
actions.finish+=/rupture,cycle_targets=1,if=!variable.skip_rupture&!variable.priority_rotation&spell_targets.shuriken_storm>=2&target.time_to_die>=(2*combo_points)&refreshable
# Refresh Rupture early if it will expire during Symbols. Do that refresh if SoD gets ready in the next 5s.
actions.finish+=/rupture,if=!variable.skip_rupture&remains<cooldown.symbols_of_death.remains+10&cooldown.symbols_of_death.remains<=5&target.time_to_die-remains>cooldown.symbols_of_death.remains+5
actions.finish+=/black_powder,if=!variable.priority_rotation&spell_targets>=3
actions.finish+=/coup_de_grace
actions.finish+=/eviscerate

# Stealth Cooldowns  Helper Variable for Shadow Dance.
actions.stealth_cds=variable,name=shd_threshold,value=cooldown.shadow_dance.charges_fractional>=0.75+talent.double_dance
# Helper variable to check for Cold Blood and The Rotten buff.
actions.stealth_cds+=/variable,name=rotten_cb,value=(!buff.the_rotten.up|!set_bonus.tier30_2pc)&(!talent.cold_blood|cooldown.cold_blood.remains<4|cooldown.cold_blood.remains>10)
# Consider Flagellation, Symbols and Secret Technique cooldown when using Vanish with Shadow Dust.
actions.stealth_cds+=/vanish,if=(combo_points.deficit>1|buff.shadow_blades.up&talent.invigorating_shadowdust)&!variable.shd_threshold&(cooldown.flagellation.remains>=60|!talent.flagellation|fight_remains<=(30*cooldown.vanish.charges))&(cooldown.symbols_of_death.remains>3|!set_bonus.tier30_2pc)&(cooldown.secret_technique.remains>=10|!talent.secret_technique|cooldown.vanish.charges>=2&talent.invigorating_shadowdust&(buff.the_rotten.up|!talent.the_rotten)&!raid_event.adds.up)
# Pool for Shadowmeld unless we are about to cap on Dance charges.
actions.stealth_cds+=/pool_resource,for_next=1,extra_amount=40,if=race.night_elf
actions.stealth_cds+=/shadowmeld,if=energy>=40&energy.deficit>=10&!variable.shd_threshold&combo_points.deficit>4
actions.stealth_cds+=/variable,name=shd_combo_points,value=combo_points.deficit>=3
# Shadow dance when Rupture is up and synchronize depending on talent choice.
actions.stealth_cds+=/shadow_dance,if=(dot.rupture.ticking|talent.invigorating_shadowdust)&variable.rotten_cb&(!talent.the_first_dance|combo_points.deficit>=4|buff.shadow_blades.up)&(variable.shd_combo_points&variable.shd_threshold|(buff.shadow_blades.up|cooldown.symbols_of_death.up&!talent.sepsis|buff.symbols_of_death.remains>=4&!set_bonus.tier30_2pc|!buff.symbols_of_death.remains&set_bonus.tier30_2pc)&cooldown.secret_technique.remains<10+12*(!talent.invigorating_shadowdust|set_bonus.tier30_2pc))

# Stealthed Rotation  Always Strike from Stealth
actions.stealthed=shadowstrike,if=buff.stealth.up&(spell_targets.shuriken_storm<4|variable.priority_rotation)
# Finish when on Animacharged combo points or max combo points.
actions.stealthed+=/call_action_list,name=finish,if=effective_combo_points>=cp_max_spend
actions.stealthed+=/call_action_list,name=finish,if=buff.shuriken_tornado.up&combo_points.deficit<=2
actions.stealthed+=/call_action_list,name=finish,if=combo_points.deficit<=1+(talent.deeper_stratagem|talent.secret_stratagem)
# Backstab for Danse Macabre stack generation during Shadowblades.
actions.stealthed+=/backstab,if=!buff.premeditation.up&buff.shadow_dance.remains>=3&buff.shadow_blades.up&!used_for_danse&talent.danse_macabre&spell_targets.shuriken_storm<=3&!buff.the_rotten.up
# Gloomblade for Danse Macabre stack generation during Shadowblades.
actions.stealthed+=/gloomblade,if=!buff.premeditation.up&buff.shadow_dance.remains>=3&buff.shadow_blades.up&!used_for_danse&talent.danse_macabre&spell_targets.shuriken_storm<=4
# Shadow Strike for Danse Macabre stack generation during Shadowblades.
actions.stealthed+=/shadowstrike,if=!used_for_danse&buff.shadow_blades.up
actions.stealthed+=/shuriken_storm,if=!buff.premeditation.up&spell_targets>=4
actions.stealthed+=/shadowstrike

```

# ActionPriorityLists\rogue_outlaw.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=apply_poison
actions.precombat+=/flask
actions.precombat+=/augmentation
actions.precombat+=/food
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/use_item,name=imperfect_ascendancy_serum
actions.precombat+=/stealth,precombat_seconds=2
# Cancel Stealth to activate Double Jeopardy
actions.precombat+=/cancel_buff,name=stealth,if=talent.double_jeopardy
actions.precombat+=/roll_the_bones,precombat_seconds=2
actions.precombat+=/adrenaline_rush,precombat_seconds=1,if=talent.improved_adrenaline_rush
actions.precombat+=/slice_and_dice,precombat_seconds=1
actions.precombat+=/stealth

# Executed every time the actor is available.
# Restealth if possible (no vulnerable enemies in combat)
actions=stealth
# Interrupt on cooldown to allow simming interactions with that
actions+=/kick
# Default Roll the Bones reroll rule: reroll for any buffs that aren't Buried Treasure, excluding Grand Melee in single target
actions+=/variable,name=rtb_reroll,value=rtb_buffs.will_lose=(rtb_buffs.will_lose.buried_treasure+rtb_buffs.will_lose.grand_melee&spell_targets.blade_flurry<2&raid_event.adds.in>10)
# Crackshot builds without T31 should reroll for True Bearing (or Broadside without Hidden Opportunity) if we won't lose over 1 buff
actions+=/variable,name=rtb_reroll,if=talent.crackshot&!set_bonus.tier31_4pc,value=(!rtb_buffs.will_lose.true_bearing&talent.hidden_opportunity|!rtb_buffs.will_lose.broadside&!talent.hidden_opportunity)&rtb_buffs.will_lose<=1
# Crackshot builds with T31 should reroll if we won't lose over 1 buff (2 with Loaded Dice)
actions+=/variable,name=rtb_reroll,if=talent.crackshot&set_bonus.tier31_4pc,value=(rtb_buffs.will_lose<=1+buff.loaded_dice.up)
# Hidden Opportunity builds without Crackshot should reroll for Skull and Crossbones or any 2 buffs excluding Grand Melee in single target
actions+=/variable,name=rtb_reroll,if=!talent.crackshot&talent.hidden_opportunity,value=!rtb_buffs.will_lose.skull_and_crossbones&(rtb_buffs.will_lose<2+rtb_buffs.will_lose.grand_melee&spell_targets.blade_flurry<2&raid_event.adds.in>10)
# Additional reroll rules if all active buffs will not be rolled away, not in stealth, Loaded Dice is active, and we have less than 6 buffs
actions+=/variable,name=rtb_reroll,value=variable.rtb_reroll&rtb_buffs.longer=0|rtb_buffs.normal=0&rtb_buffs.longer>=1&rtb_buffs<6&rtb_buffs.max_remains<=39&!stealthed.all&buff.loaded_dice.up
# Avoid rerolls when we will not have time remaining on the fight or add wave to recoup the opportunity cost of the global
actions+=/variable,name=rtb_reroll,op=reset,if=!(raid_event.adds.remains>12|raid_event.adds.up&(raid_event.adds.in-raid_event.adds.remains)<6|target.time_to_die>12)|fight_remains<12
actions+=/variable,name=ambush_condition,value=(talent.hidden_opportunity|combo_points.deficit>=2+talent.improved_ambush+buff.broadside.up)&energy>=50
# Use finishers if at -1 from max combo points, or -2 in Stealth with Crackshot
actions+=/variable,name=finish_condition,value=effective_combo_points>=cp_max_spend-1-(stealthed.all&talent.crackshot)
# With multiple targets, this variable is checked to decide whether some CDs should be synced with Blade Flurry
actions+=/variable,name=blade_flurry_sync,value=spell_targets.blade_flurry<2&raid_event.adds.in>20|buff.blade_flurry.remains>gcd
actions+=/call_action_list,name=cds
# High priority stealth list, will fall through if no conditions are met
actions+=/call_action_list,name=stealth,if=stealthed.all
actions+=/run_action_list,name=finish,if=variable.finish_condition
actions+=/call_action_list,name=build
actions+=/arcane_torrent,if=energy.base_deficit>=15+energy.regen
actions+=/arcane_pulse
actions+=/lights_judgment
actions+=/bag_of_tricks

# Builders
actions.build=echoing_reprimand
# High priority Ambush for Hidden Opportunity builds
actions.build+=/ambush,if=talent.hidden_opportunity&buff.audacity.up
# With Audacity + Hidden Opportunity + Fan the Hammer, consume Opportunity to proc Audacity any time Ambush is not available
actions.build+=/pistol_shot,if=talent.fan_the_hammer&talent.audacity&talent.hidden_opportunity&buff.opportunity.up&!buff.audacity.up
# With Fan the Hammer, consume Opportunity as a higher priority if at max stacks or if it will expire
actions.build+=/pistol_shot,if=talent.fan_the_hammer&buff.opportunity.up&(buff.opportunity.stack>=buff.opportunity.max_stack|buff.opportunity.remains<2)
# With Fan the Hammer, consume Opportunity if it will not overcap CPs, or with 1 CP at minimum
actions.build+=/pistol_shot,if=talent.fan_the_hammer&buff.opportunity.up&(combo_points.deficit>=(1+(talent.quick_draw+buff.broadside.up)*(talent.fan_the_hammer.rank+1))|combo_points<=talent.ruthlessness)
# If not using Fan the Hammer, then consume Opportunity based on energy, when it will exactly cap CPs, or when using Quick Draw
actions.build+=/pistol_shot,if=!talent.fan_the_hammer&buff.opportunity.up&(energy.base_deficit>energy.regen*1.5|combo_points.deficit<=1+buff.broadside.up|talent.quick_draw.enabled|talent.audacity.enabled&!buff.audacity.up)
# Fallback pooling just so Sinister Strike is never casted if Ambush is available for Hidden Opportunity builds
actions.build+=/pool_resource,for_next=1
actions.build+=/ambush,if=talent.hidden_opportunity
actions.build+=/sinister_strike

# Cooldowns  Use Adrenaline Rush if it is not active and the finisher condition is not met, but Crackshot builds can refresh it with 2cp or lower inside stealth
actions.cds=adrenaline_rush,if=!buff.adrenaline_rush.up&(!variable.finish_condition|!talent.improved_adrenaline_rush)|stealthed.all&talent.crackshot&talent.improved_adrenaline_rush&combo_points<=2
# Maintain Blade Flurry on 2+ targets
actions.cds+=/blade_flurry,if=spell_targets>=2&buff.blade_flurry.remains<gcd
# With Deft Maneuvers, use Blade Flurry on cooldown at 5+ targets, or at 3-4 targets if missing combo points equal to the amount given
actions.cds+=/blade_flurry,if=talent.deft_maneuvers&!variable.finish_condition&(spell_targets>=3&combo_points.deficit=spell_targets+buff.broadside.up|spell_targets>=5)
# Use Roll the Bones if reroll conditions are met, or with no buffs, or 2s before buffs expire with T31, or 7s before buffs expire with Vanish ready
actions.cds+=/roll_the_bones,if=variable.rtb_reroll|rtb_buffs=0|rtb_buffs.max_remains<=2&set_bonus.tier31_4pc|rtb_buffs.max_remains<=7&cooldown.vanish.ready&talent.crackshot
# Use Keep it Rolling with at least 3 buffs that are not Buried Treasure. If Broadside is not active, then wait until just before the lowest buff expires.
actions.cds+=/keep_it_rolling,if=rtb_buffs>=3+(buff.buried_treasure.up|set_bonus.tier31_4pc)&(rtb_buffs.min_remains<2|buff.broadside.up)
actions.cds+=/ghostly_strike,if=combo_points<cp_max_spend
# Trinkets that should not be used during stealth and have higher priority than entering stealth
actions.cds+=/use_item,name=manic_grieftorch,if=!stealthed.all&buff.between_the_eyes.up|fight_remains<=5
actions.cds+=/use_item,name=beacon_to_the_beyond,if=!stealthed.all&buff.between_the_eyes.up|fight_remains<=5
actions.cds+=/use_item,name=imperfect_ascendancy_serum,if=!stealthed.all|fight_remains<=22
# Killing Spree has higher priority than stealth cooldowns
actions.cds+=/killing_spree,if=variable.finish_condition&!stealthed.all
# Crackshot builds use stealth cooldowns if Between the Eyes is ready
actions.cds+=/call_action_list,name=stealth_cds,if=!stealthed.all&(!talent.crackshot|cooldown.between_the_eyes.ready)
actions.cds+=/thistle_tea,if=!buff.thistle_tea.up&(energy.base_deficit>=150|fight_remains<charges*6)
# Use Blade Rush at minimal energy outside of stealth
actions.cds+=/blade_rush,if=energy.base_time_to_max>4&!stealthed.all
actions.cds+=/potion,if=buff.bloodlust.react|fight_remains<30|buff.adrenaline_rush.up
actions.cds+=/blood_fury
actions.cds+=/berserking
actions.cds+=/fireblood
actions.cds+=/ancestral_call
# Default conditions for usable items.
actions.cds+=/use_item,name=elementium_pocket_anvil,use_off_gcd=1,if=gcd.remains<=action.sinister_strike.gcd%2
# Use Bomb Dispenser on cooldown, but hold if 2nd trinket is nearly off cooldown, unless at max charges or sim duration ends soon
actions.cds+=/use_item,name=dragonfire_bomb_dispenser,use_off_gcd=1,if=gcd.remains<=action.sinister_strike.gcd%2&((!trinket.1.is.dragonfire_bomb_dispenser&trinket.1.cooldown.remains>10|trinket.2.cooldown.remains>10)|cooldown.dragonfire_bomb_dispenser.charges>2|fight_remains<20|!trinket.2.has_cooldown|!trinket.1.has_cooldown)
actions.cds+=/use_item,name=stormeaters_boon,if=spell_targets.blade_flurry>desired_targets|raid_event.adds.in>60|raid_event.adds.count<2|fight_remains<10
actions.cds+=/use_item,name=enduring_dreadplate,if=spell_targets.blade_flurry>desired_targets|raid_event.adds.in>60|raid_event.adds.count<2|fight_remains<16
actions.cds+=/use_item,name=windscar_whetstone,if=spell_targets.blade_flurry>desired_targets|raid_event.adds.in>60|raid_event.adds.count<2|fight_remains<7
actions.cds+=/use_items,slots=trinket1,if=buff.between_the_eyes.up|trinket.1.has_stat.any_dps|fight_remains<=20
actions.cds+=/use_items,slots=trinket2,if=buff.between_the_eyes.up|trinket.2.has_stat.any_dps|fight_remains<=20

# Finishers  Use Between the Eyes to keep the crit buff up, but on cooldown if Improved/Greenskins, and avoid overriding Greenskins
actions.finish=between_the_eyes,if=!talent.crackshot&(buff.between_the_eyes.remains<4|talent.improved_between_the_eyes|talent.greenskins_wickers)&!buff.greenskins_wickers.up
# Crackshot builds use Between the Eyes outside of Stealth if we will not enter a Stealth window before the next cast
actions.finish+=/between_the_eyes,if=talent.crackshot&cooldown.vanish.remains>45&(raid_event.adds.remains>8|raid_event.adds.in<raid_event.adds.remains|!raid_event.adds.up)
actions.finish+=/slice_and_dice,if=buff.slice_and_dice.remains<fight_remains&refreshable
actions.finish+=/cold_blood
actions.finish+=/coup_de_grace
actions.finish+=/dispatch

# Stealth
actions.stealth=blade_flurry,if=talent.subterfuge&talent.hidden_opportunity&spell_targets>=2&buff.blade_flurry.remains<gcd
actions.stealth+=/cold_blood,if=variable.finish_condition
# Ensure Crackshot BtE is not skipped because of low energy
actions.stealth+=/pool_resource,for_next=1
# High priority Between the Eyes for Crackshot, except not directly out of Shadowmeld
actions.stealth+=/between_the_eyes,if=variable.finish_condition&talent.crackshot&(!buff.shadowmeld.up|stealthed.rogue)
actions.stealth+=/dispatch,if=variable.finish_condition
# 2 Fan the Hammer Crackshot builds can consume Opportunity in stealth with max stacks, Broadside, and low CPs, or with Greenskins active
actions.stealth+=/pistol_shot,if=talent.crackshot&talent.fan_the_hammer.rank>=2&buff.opportunity.stack>=6&(buff.broadside.up&combo_points<=1|buff.greenskins_wickers.up)
actions.stealth+=/ambush,if=talent.hidden_opportunity

# Stealth Cooldowns  Builds with Underhanded Upper Hand and Subterfuge (and Without a Trace for Crackshot) must use Vanish while Adrenaline Rush is active
actions.stealth_cds=vanish,if=talent.underhanded_upper_hand&talent.subterfuge&(buff.adrenaline_rush.up|!talent.without_a_trace&talent.crackshot)&(variable.finish_condition|!talent.crackshot&(variable.ambush_condition|!talent.hidden_opportunity))
# Builds without Underhanded Upper Hand but with Crackshot must still use Vanish into Between the Eyes on cooldown
actions.stealth_cds+=/vanish,if=!talent.underhanded_upper_hand&talent.crackshot&variable.finish_condition
# Builds without Underhanded Upper Hand and Crackshot but still Hidden Opportunity use Vanish into Ambush when Audacity is not active and under max Opportunity stacks
actions.stealth_cds+=/vanish,if=!talent.underhanded_upper_hand&!talent.crackshot&talent.hidden_opportunity&!buff.audacity.up&buff.opportunity.stack<buff.opportunity.max_stack&variable.ambush_condition
# Builds without Underhanded Upper Hand, Crackshot, and Hidden Opportunity use Vanish into a builder to activate Double Jeopardy without breaking the current coin streak, or to activate Take 'em by Surprise
actions.stealth_cds+=/vanish,if=!talent.underhanded_upper_hand&!talent.crackshot&!talent.hidden_opportunity&(!variable.finish_condition&talent.double_jeopardy|!buff.take_em_by_surprise.up&talent.take_em_by_surprise)
actions.stealth_cds+=/shadowmeld,if=variable.finish_condition&!cooldown.vanish.ready

```

# ActionPriorityLists\rogue_assassination.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=apply_poison
actions.precombat+=/flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/snapshot_stats
# Check which trinket slots have Stat Values
actions.precombat+=/variable,name=trinket_sync_slot,value=1,if=trinket.1.has_stat.any_dps&(!trinket.2.has_stat.any_dps|trinket.1.cooldown.duration>=trinket.2.cooldown.duration)&!trinket.2.is.witherbarks_branch|trinket.1.is.witherbarks_branch
actions.precombat+=/variable,name=trinket_sync_slot,value=2,if=trinket.2.has_stat.any_dps&(!trinket.1.has_stat.any_dps|trinket.2.cooldown.duration>trinket.1.cooldown.duration)&!trinket.1.is.witherbarks_branch|trinket.2.is.witherbarks_branch
# Determine combo point finish condition
actions.precombat+=/variable,name=effective_spend_cp,value=cp_max_spend-2<?5*talent.hand_of_fate
# Pre-cast Slice and Dice if possible
actions.precombat+=/stealth
actions.precombat+=/slice_and_dice,precombat_seconds=1

# Executed every time the actor is available.
# Restealth if possible (no vulnerable enemies in combat)
actions=stealth
# Interrupt on cooldown to allow simming interactions with that
actions+=/kick
# Conditional to check if there is only one enemy
actions+=/variable,name=single_target,value=spell_targets.fan_of_knives<2
# Combined Energy Regen needed to saturate
actions+=/variable,name=regen_saturated,value=energy.regen_combined>35
# Check if we should be using our energy
actions+=/variable,name=not_pooling,value=(dot.deathmark.ticking|dot.kingsbane.ticking|debuff.shiv.up)|(buff.envenom.up&buff.envenom.remains<=1&energy.pct>=40)|energy.pct>=50|fight_remains<=20
actions+=/call_action_list,name=stealthed,if=stealthed.rogue|stealthed.improved_garrote|master_assassin_remains>0
actions+=/call_action_list,name=cds
# Put SnD up initially for Cut to the Chase, refresh with Envenom if at low duration
actions+=/slice_and_dice,if=!buff.slice_and_dice.up&dot.rupture.ticking&combo_points>=1
actions+=/envenom,if=buff.slice_and_dice.up&buff.slice_and_dice.remains<5&combo_points>=5
actions+=/call_action_list,name=dot
actions+=/call_action_list,name=direct
actions+=/arcane_torrent,if=energy.deficit>=15+energy.regen_combined
actions+=/arcane_pulse
actions+=/lights_judgment
actions+=/bag_of_tricks

# Cooldowns  Wait on Deathmark for Garrote with MA and check for Kingsbane
actions.cds=variable,name=deathmark_ma_condition,value=!talent.master_assassin.enabled|dot.garrote.ticking
actions.cds+=/variable,name=deathmark_kingsbane_condition,value=!talent.kingsbane|cooldown.kingsbane.remains<=2
# Deathmark to be used if not stealthed, Rupture is up, and all other talent conditions are satisfied
actions.cds+=/variable,name=deathmark_condition,value=!stealthed.rogue&dot.rupture.ticking&buff.envenom.up&!debuff.deathmark.up&variable.deathmark_ma_condition&variable.deathmark_kingsbane_condition
# Usages for various special-case Trinkets and other Cantrips if applicable
actions.cds+=/call_action_list,name=items
# Invoke Externals to Deathmark
actions.cds+=/invoke_external_buff,name=power_infusion,if=dot.deathmark.ticking
actions.cds+=/deathmark,if=variable.deathmark_condition|fight_remains<=20
# Check for Applicable Shiv usage
actions.cds+=/call_action_list,name=shiv
actions.cds+=/kingsbane,if=(debuff.shiv.up|cooldown.shiv.remains<6)&buff.envenom.up&(cooldown.deathmark.remains>=50|dot.deathmark.ticking)|fight_remains<=15
# Avoid overcapped energy, use with shiv, or dump charges at the end of a fight
actions.cds+=/thistle_tea,if=!buff.thistle_tea.up&(((energy.deficit>=100+energy.regen_combined|charges>=3)&debuff.shiv.remains>=4))|fight_remains<charges*6
# Potion/Racials/Other misc cooldowns
actions.cds+=/call_action_list,name=misc_cds
actions.cds+=/call_action_list,name=vanish,if=!stealthed.all&master_assassin_remains=0
actions.cds+=/cold_blood,if=combo_points>=4

# Direct Damage Abilities   Envenom at applicable cp if not pooling, capped on amplifying poison stacks, on an animacharged CP, or in aoe.
actions.direct=envenom,if=!buff.darkest_night.up&effective_combo_points>=variable.effective_spend_cp&(variable.not_pooling|debuff.amplifying_poison.stack>=20|effective_combo_points>cp_max_spend|!variable.single_target)&!buff.vanish.up
# Special Envenom handling for Darkest Night
actions.direct+=/envenom,if=buff.darkest_night.up&effective_combo_points>=cp_max_spend
# Check if we should be using a filler
actions.direct+=/variable,name=use_filler,value=combo_points.deficit>1|variable.not_pooling|!variable.single_target
# Maintain Caustic Spatter
actions.direct+=/mutilate,if=talent.caustic_spatter&dot.rupture.ticking&(!debuff.caustic_spatter.up|debuff.caustic_spatter.remains<=2)&variable.use_filler&!variable.single_target
actions.direct+=/ambush,if=talent.caustic_spatter&dot.rupture.ticking&(!debuff.caustic_spatter.up|debuff.caustic_spatter.remains<=2)&variable.use_filler&!variable.single_target
actions.direct+=/echoing_reprimand,if=variable.use_filler|fight_remains<20
# Fan of Knives at 2+ targets or 3+ with DTB
actions.direct+=/fan_of_knives,if=variable.use_filler&(!priority_rotation&spell_targets.fan_of_knives>=2+stealthed.rogue+talent.dragontempered_blades)
# Fan of Knives to apply poisons if inactive on any target (or any bleeding targets with priority rotation) at 3T
actions.direct+=/fan_of_knives,target_if=!dot.deadly_poison_dot.ticking&(!priority_rotation|dot.garrote.ticking|dot.rupture.ticking),if=variable.use_filler&spell_targets.fan_of_knives>=3
# Ambush on Blindside/Subterfuge. Do not use Ambush from stealth during Kingsbane & Deathmark.
actions.direct+=/ambush,if=variable.use_filler&(buff.blindside.up|stealthed.rogue)&(!dot.kingsbane.ticking|debuff.deathmark.down|buff.blindside.up)
# Tab-Mutilate to apply Deadly Poison at 2 targets
actions.direct+=/mutilate,target_if=!dot.deadly_poison_dot.ticking&!debuff.amplifying_poison.up,if=variable.use_filler&spell_targets.fan_of_knives=2
# Fallback Mutilate
actions.direct+=/mutilate,if=variable.use_filler

# Damage over time abilities   Check what the maximum Scent of Blood stacks is currently
actions.dot=variable,name=scent_effective_max_stacks,value=(spell_targets.fan_of_knives*talent.scent_of_blood.rank*2)>?20
# We are Scent Saturated when our stack count is hitting the maximum
actions.dot+=/variable,name=scent_saturation,value=buff.scent_of_blood.stack>=variable.scent_effective_max_stacks
# Crimson Tempest on 3+ Targets if we have enough energy regen
actions.dot+=/crimson_tempest,target_if=min:remains,if=spell_targets>=3&refreshable&pmultiplier<=1&effective_combo_points>=variable.effective_spend_cp&energy.regen_combined>25&!cooldown.deathmark.ready&target.time_to_die-remains>6
# Garrote upkeep, also uses it in AoE to reach energy saturation
actions.dot+=/garrote,if=combo_points.deficit>=1&(pmultiplier<=1)&refreshable&target.time_to_die-remains>12
actions.dot+=/garrote,cycle_targets=1,if=combo_points.deficit>=1&(pmultiplier<=1)&refreshable&!variable.regen_saturated&spell_targets.fan_of_knives>=2&target.time_to_die-remains>12
# Rupture upkeep, also uses it in AoE to reach energy saturation
actions.dot+=/rupture,if=effective_combo_points>=variable.effective_spend_cp&(pmultiplier<=1)&refreshable&target.time_to_die-remains>(4+(talent.dashing_scoundrel*5)+(variable.regen_saturated*6))&!buff.darkest_night.up
actions.dot+=/rupture,cycle_targets=1,if=effective_combo_points>=variable.effective_spend_cp&(pmultiplier<=1)&refreshable&(!variable.regen_saturated|!variable.scent_saturation)&target.time_to_die-remains>(4+(talent.dashing_scoundrel*5)+(variable.regen_saturated*6))&!buff.darkest_night.up
# Garrote as a special generator for the last CP before a finisher for edge case handling
actions.dot+=/garrote,if=refreshable&combo_points.deficit>=1&(pmultiplier<=1|remains<=tick_time&spell_targets.fan_of_knives>=3)&(remains<=tick_time*2&spell_targets.fan_of_knives>=3)&(target.time_to_die-remains)>4&master_assassin_remains=0

# Special Case Trinkets
actions.items=use_item,name=ashes_of_the_embersoul,use_off_gcd=1,if=(dot.kingsbane.ticking&dot.kingsbane.remains<=11)|fight_remains<=22
actions.items+=/use_item,name=algethar_puzzle_box,use_off_gcd=1,if=dot.rupture.ticking&cooldown.deathmark.remains<2|fight_remains<=22
# Fallback case for using stat trinkets
actions.items+=/use_items,slots=trinket1,if=(variable.trinket_sync_slot=1&(debuff.deathmark.up|fight_remains<=20)|(variable.trinket_sync_slot=2&(!trinket.2.cooldown.ready|!debuff.deathmark.up&cooldown.deathmark.remains>20))|!variable.trinket_sync_slot)
actions.items+=/use_items,slots=trinket2,if=(variable.trinket_sync_slot=2&(debuff.deathmark.up|fight_remains<=20)|(variable.trinket_sync_slot=1&(!trinket.1.cooldown.ready|!debuff.deathmark.up&cooldown.deathmark.remains>20))|!variable.trinket_sync_slot)

# Miscellaneous Cooldowns Potion
actions.misc_cds=potion,if=buff.bloodlust.react|fight_remains<30|debuff.deathmark.up
# Various special racials to be synced with cooldowns
actions.misc_cds+=/blood_fury,if=debuff.deathmark.up
actions.misc_cds+=/berserking,if=debuff.deathmark.up
actions.misc_cds+=/fireblood,if=debuff.deathmark.up
actions.misc_cds+=/ancestral_call,if=(!talent.kingsbane&debuff.deathmark.up&debuff.shiv.up)|(talent.kingsbane&debuff.deathmark.up&dot.kingsbane.ticking&dot.kingsbane.remains<8)

# Shiv Handling  Shiv if talented into Kingsbane; Always sync, or prioritize the last 8 seconds
actions.shiv=shiv,if=talent.kingsbane&!talent.lightweight_shiv.enabled&buff.envenom.up&!debuff.shiv.up&dot.garrote.ticking&dot.rupture.ticking&(dot.kingsbane.ticking&dot.kingsbane.remains<8|cooldown.kingsbane.remains>=24)&(!talent.crimson_tempest.enabled|variable.single_target|dot.crimson_tempest.ticking)|fight_remains<=charges*8
actions.shiv+=/shiv,if=talent.kingsbane&talent.lightweight_shiv.enabled&buff.envenom.up&!debuff.shiv.up&dot.garrote.ticking&dot.rupture.ticking&(dot.kingsbane.ticking|cooldown.kingsbane.remains<=1)|fight_remains<=charges*8
# Shiv cases for Arterial in special circumstances
actions.shiv+=/shiv,if=talent.arterial_precision&!debuff.shiv.up&dot.garrote.ticking&dot.rupture.ticking&debuff.deathmark.up|fight_remains<=charges*8
# Fallback if no special cases apply
actions.shiv+=/shiv,if=!talent.kingsbane&!talent.arterial_precision&!debuff.shiv.up&dot.garrote.ticking&dot.rupture.ticking&(!talent.crimson_tempest.enabled|variable.single_target|dot.crimson_tempest.ticking)|fight_remains<=charges*8

# Stealthed Actions
actions.stealthed=pool_resource,for_next=1
# Apply Deathstalkers Mark if it has fallen off and we have no way to reapply otherwise
actions.stealthed+=/ambush,if=!debuff.deathstalkers_mark.up&talent.deathstalkers_mark&!buff.darkest_night.up
# Make sure to have Shiv up during Kingsbane as a final check
actions.stealthed+=/shiv,if=talent.kingsbane&(dot.kingsbane.ticking|cooldown.kingsbane.up)&(!debuff.shiv.up&debuff.shiv.remains<1)&buff.envenom.up
# Envenom to maintain the buff during Subterfuge
actions.stealthed+=/envenom,if=effective_combo_points>=variable.effective_spend_cp&dot.kingsbane.ticking&buff.envenom.remains<=3
# Envenom during Master Assassin in single target
actions.stealthed+=/envenom,if=effective_combo_points>=variable.effective_spend_cp&buff.master_assassin_aura.up&variable.single_target
# Improved Garrote: Apply or Refresh with buffed Garrotes, accounting for Indiscriminate Carnage
actions.stealthed+=/garrote,target_if=min:remains,if=stealthed.improved_garrote&(remains<12|pmultiplier<=1|(buff.indiscriminate_carnage.up&active_dot.garrote<spell_targets.fan_of_knives))&!variable.single_target&target.time_to_die-remains>2
actions.stealthed+=/garrote,if=stealthed.improved_garrote&(pmultiplier<=1|remains<14|!variable.single_target&buff.master_assassin_aura.remains<3)&combo_points.deficit>=1+2*talent.shrouded_suffocation

# Stealth Cooldowns   Vanish Sync for Improved Garrote with Deathmark
actions.vanish=pool_resource,for_next=1,extra_amount=45
# Vanish to fish for Fateful Ending if possible
actions.vanish+=/vanish,if=!buff.fatebound_lucky_coin.up&(buff.fatebound_coin_tails.stack>=5|buff.fatebound_coin_heads.stack>=5)
# Vanish to spread Garrote during Deathmark without Indiscriminate Carnage
actions.vanish+=/vanish,if=!talent.master_assassin&!talent.indiscriminate_carnage&talent.improved_garrote&cooldown.garrote.up&(dot.garrote.pmultiplier<=1|dot.garrote.refreshable)&(debuff.deathmark.up|cooldown.deathmark.remains<4)&combo_points.deficit>=(spell_targets.fan_of_knives>?4)
actions.vanish+=/pool_resource,for_next=1,extra_amount=45
# Vanish for cleaving Garrotes with Indiscriminate Carnage
actions.vanish+=/vanish,if=!talent.master_assassin&talent.indiscriminate_carnage&talent.improved_garrote&cooldown.garrote.up&(dot.garrote.pmultiplier<=1|dot.garrote.refreshable)&spell_targets.fan_of_knives>2
# Vanish for Master Assassin during Kingsbane
actions.vanish+=/vanish,if=talent.master_assassin&talent.kingsbane&dot.kingsbane.remains<=3&dot.kingsbane.ticking&debuff.deathmark.remains<=3&dot.deathmark.ticking
# Vanish fallback for Master Assassin
actions.vanish+=/vanish,if=!talent.improved_garrote&talent.master_assassin&!dot.rupture.refreshable&dot.garrote.remains>3&debuff.deathmark.up&(debuff.shiv.up|debuff.deathmark.remains<4)

```

# ActionPriorityLists\README.md

```md
## Action Priority Lists

This folder contains automatically generated raw text Action Priority Lists in SimC APL format. 


The contents can be placed directly within any SimC input, such as a text input file for the `simc.exe` command line interface, or custom APL box/Advanced Sim in raidbots.com.


**These are only generated text;** APLs are generated from source files at `engine/class_modules` and `engine/class_modules/apl`.


For questions and contributions to the APL for a spec, you're encouraged to inquire in your Class/Spec discord, as SimC developers and other contributors can be found there. You can also submit a Pull Request with direct changes to the source files.

```

# ActionPriorityLists\priest_shadow.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/shadowform,if=!buff.shadowform.up
actions.precombat+=/variable,name=dr_force_prio,default=0,op=reset
actions.precombat+=/variable,name=me_force_prio,default=1,op=reset
actions.precombat+=/variable,name=max_vts,default=0,op=reset
actions.precombat+=/variable,name=is_vt_possible,default=0,op=reset
actions.precombat+=/variable,name=pooling_mindblasts,default=0,op=reset
actions.precombat+=/arcane_torrent
actions.precombat+=/use_item,name=aberrant_spellforge
actions.precombat+=/shadow_crash,if=raid_event.adds.in>=25&spell_targets.shadow_crash<=8&!fight_style.dungeonslice&(!set_bonus.tier31_4pc|spell_targets.shadow_crash>1)
actions.precombat+=/vampiric_touch,if=!talent.shadow_crash.enabled|raid_event.adds.in<25|spell_targets.shadow_crash>8|fight_style.dungeonslice|set_bonus.tier31_4pc&spell_targets.shadow_crash=1

# Executed every time the actor is available.
actions=variable,name=holding_crash,op=set,value=raid_event.adds.in<15
actions+=/variable,name=pool_for_cds,op=set,value=(cooldown.void_eruption.remains<=gcd.max*3&talent.void_eruption|cooldown.dark_ascension.up&talent.dark_ascension)|talent.void_torrent&talent.psychic_link&cooldown.void_torrent.remains<=4&(!raid_event.adds.exists&spell_targets.vampiric_touch>1|raid_event.adds.in<=5|raid_event.adds.remains>=6&!variable.holding_crash)&!buff.voidform.up
actions+=/call_action_list,name=aoe,if=active_enemies>2
actions+=/run_action_list,name=main

actions.aoe=call_action_list,name=aoe_variables
# High Priority action to put out Vampiric Touch on enemies that will live at least 18 seconds, up to 12 targets manually while prepping AoE
actions.aoe+=/vampiric_touch,target_if=refreshable&target.time_to_die>=18&(dot.vampiric_touch.ticking|!variable.dots_up),if=(variable.max_vts>0&!variable.manual_vts_applied&!action.shadow_crash.in_flight|!talent.whispering_shadows)&!buff.entropic_rift.up
# Use Shadow Crash to apply Vampiric Touch to as many adds as possible while being efficient with Vampiric Touch refresh windows
actions.aoe+=/shadow_crash,if=!variable.holding_crash,target_if=dot.vampiric_touch.refreshable|dot.vampiric_touch.remains<=target.time_to_die&!buff.voidform.up&(raid_event.adds.in-dot.vampiric_touch.remains)<15

actions.aoe_variables=variable,name=max_vts,op=set,default=12,value=spell_targets.vampiric_touch>?12
actions.aoe_variables+=/variable,name=is_vt_possible,op=set,value=0,default=1
actions.aoe_variables+=/variable,name=is_vt_possible,op=set,value=1,target_if=max:(target.time_to_die*dot.vampiric_touch.refreshable),if=target.time_to_die>=18
# TODO: Revamp to fix undesired behaviour with unstacked fights
actions.aoe_variables+=/variable,name=dots_up,op=set,value=(active_dot.vampiric_touch+8*(action.shadow_crash.in_flight&talent.whispering_shadows))>=variable.max_vts|!variable.is_vt_possible
actions.aoe_variables+=/variable,name=holding_crash,op=set,value=(variable.max_vts-active_dot.vampiric_touch)<4|raid_event.adds.in<10&raid_event.adds.count>(variable.max_vts-active_dot.vampiric_touch),if=variable.holding_crash&talent.whispering_shadows
actions.aoe_variables+=/variable,name=manual_vts_applied,op=set,value=(active_dot.vampiric_touch+8*!variable.holding_crash)>=variable.max_vts|!variable.is_vt_possible

# TODO: Check VE/DA enter conditions based on dots
actions.cds=potion,if=(buff.voidform.up|buff.power_infusion.up|buff.dark_ascension.up&(fight_remains<=cooldown.power_infusion.remains+15))&(fight_remains>=320|time_to_bloodlust>=320|buff.bloodlust.react)|fight_remains<=30
actions.cds+=/fireblood,if=buff.power_infusion.up|fight_remains<=8
actions.cds+=/berserking,if=buff.power_infusion.up|fight_remains<=12
actions.cds+=/blood_fury,if=buff.power_infusion.up|fight_remains<=15
actions.cds+=/ancestral_call,if=buff.power_infusion.up|fight_remains<=15
# Use Nymue's before we go into our cooldowns
actions.cds+=/use_item,name=nymues_unraveling_spindle,if=variable.dots_up&(fight_remains<30|target.time_to_die>15)&(!talent.dark_ascension|cooldown.dark_ascension.remains<3+gcd.max|fight_remains<15)
# Sync Power Infusion with Voidform or Dark Ascension
actions.cds+=/power_infusion,if=(buff.voidform.up|buff.dark_ascension.up&(fight_remains<=80|fight_remains>=140)|active_allied_augmentations)
# Use <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> while <a href='https://www.wowhead.com/spell=194249/voidform'>Voidform</a> or <a href='https://www.wowhead.com/spell=391109/dark-ascension'>Dark Ascension</a> is active. Chain directly after your own <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a>.
actions.cds+=/invoke_external_buff,name=power_infusion,if=(buff.voidform.up|buff.dark_ascension.up)&!buff.power_infusion.up
actions.cds+=/invoke_external_buff,name=bloodlust,if=buff.power_infusion.up&fight_remains<120|fight_remains<=40
# Make sure Mindbender is active before popping Dark Ascension unless you have insignificant talent points or too many targets
actions.cds+=/halo,if=talent.power_surge&(pet.fiend.active&cooldown.fiend.remains>=4&talent.mindbender|!talent.mindbender&!cooldown.fiend.up|active_enemies>2&!talent.inescapable_torment|!talent.dark_ascension)&(cooldown.mind_blast.charges=0|!talent.void_eruption|cooldown.void_eruption.remains>=gcd.max*4)
# Make sure Mindbender is active before popping Void Eruption and dump charges of Mind Blast before casting
actions.cds+=/void_eruption,if=!cooldown.fiend.up&(pet.fiend.active&cooldown.fiend.remains>=4|!talent.mindbender|active_enemies>2&!talent.inescapable_torment.rank)&(cooldown.mind_blast.charges=0|time>15)
actions.cds+=/dark_ascension,if=pet.fiend.active&cooldown.fiend.remains>=4|!talent.mindbender&!cooldown.fiend.up|active_enemies>2&!talent.inescapable_torment
actions.cds+=/call_action_list,name=trinkets
# Use Desperate Prayer to heal up should Shadow Word: Death or other damage bring you below 75%
actions.cds+=/desperate_prayer,if=health.pct<=75

actions.empowered_filler=mind_spike_insanity,target_if=max:dot.devouring_plague.remains
actions.empowered_filler+=/mind_flay,target_if=max:dot.devouring_plague.remains,if=buff.mind_flay_insanity.up

# Cast Vampiric Touch to consume Unfurling Darkness, prefering the target with the lowest DoT duration active
actions.filler=vampiric_touch,target_if=min:remains,if=buff.unfurling_darkness.up
actions.filler+=/call_action_list,name=heal_for_tof,if=!buff.twist_of_fate.up&buff.twist_of_fate_can_trigger_on_ally_heal.up&(talent.rhapsody|talent.divine_star|talent.halo)
# Use PWS with CR talented to trigger TOF if there are no better alternatives available to do this as we still get insanity for a PWS cast.
actions.filler+=/power_word_shield,if=!buff.twist_of_fate.up&buff.twist_of_fate_can_trigger_on_ally_heal.up&talent.crystalline_reflection
actions.filler+=/call_action_list,name=empowered_filler,if=dot.devouring_plague.remains>action.mind_spike.cast_time|!talent.mind_spike
actions.filler+=/shadow_word_death,target_if=target.health.pct<20|(buff.deathspeaker.up|set_bonus.tier31_2pc)&dot.devouring_plague.ticking
actions.filler+=/shadow_word_death,target_if=min:target.time_to_die,if=talent.inescapable_torment&pet.fiend.active
actions.filler+=/devouring_plague,if=buff.voidform.up|cooldown.dark_ascension.up|buff.mind_devourer.up
# Save up to 20s if adds are coming soon.
actions.filler+=/halo,if=spell_targets>1
# Using a heal with no damage kickbacks for TOF is damage neutral, so we will do it.
actions.filler+=/power_word_life,if=!buff.twist_of_fate.up&buff.twist_of_fate_can_trigger_on_ally_heal.up
actions.filler+=/call_action_list,name=empowered_filler
actions.filler+=/call_action_list,name=heal_for_tof,if=equipped.rashoks_molten_heart&(active_allies-(10-buff.molten_radiance.value))>=10&buff.molten_radiance.up,line_cd=5
actions.filler+=/mind_spike,target_if=max:dot.devouring_plague.remains
actions.filler+=/mind_flay,target_if=max:dot.devouring_plague.remains,chain=1,interrupt_immediate=1,interrupt_if=ticks>=2
actions.filler+=/divine_star
# Use Shadow Crash while moving as a low-priority action when adds will not come in 20 seconds.
actions.filler+=/shadow_crash,if=raid_event.adds.in>20&!set_bonus.tier31_4pc
# Use Shadow Word: Death while moving as a low-priority action in execute
actions.filler+=/shadow_word_death,target_if=target.health.pct<20
# Use Shadow Word: Death while moving as a low-priority action
actions.filler+=/shadow_word_death,target_if=max:dot.devouring_plague.remains
# Use Shadow Word: Pain while moving as a low-priority action with T31 4pc
actions.filler+=/shadow_word_pain,target_if=max:dot.devouring_plague.remains,if=set_bonus.tier31_4pc
# Use Shadow Word: Pain while moving as a low-priority action without T31 4pc
actions.filler+=/shadow_word_pain,target_if=min:remains,if=!set_bonus.tier31_4pc

# Use Halo to acquire Twist of Fate if an ally can be healed for it and it is not currently up.
actions.heal_for_tof=halo
# Use Divine Star to acquire Twist of Fate if an ally can be healed for it and it is not currently up.
actions.heal_for_tof+=/divine_star
# Use Holy Nova when Rhapsody is fully stacked to acquire Twist of Fate if an ally can be healed for it and it is not currently up.
actions.heal_for_tof+=/holy_nova,if=buff.rhapsody.stack=20&talent.rhapsody

actions.main=variable,name=dots_up,op=set,value=active_dot.vampiric_touch=active_enemies|action.shadow_crash.in_flight&talent.whispering_shadows,if=active_enemies<3
# Are we pooling mindblasts? Currently only used for Voidweaver.
actions.main+=/variable,name=pooling_mindblasts,op=setif,value=1,value_else=0,condition=(cooldown.void_torrent.remains<?(variable.holding_crash*raid_event.adds.in))<=gcd.max*(1+talent.mind_melt*3),if=talent.void_blast
actions.main+=/call_action_list,name=cds,if=fight_remains<30|target.time_to_die>15&(!variable.holding_crash|active_enemies>2)
# Use Shadowfiend and Mindbender on cooldown as long as Vampiric Touch and Shadow Word: Pain are active and sync with Dark Ascension
actions.main+=/mindbender,if=(dot.shadow_word_pain.ticking&variable.dots_up|action.shadow_crash.in_flight&talent.whispering_shadows)&(fight_remains<30|target.time_to_die>15)&(!talent.dark_ascension|cooldown.dark_ascension.remains<gcd.max|fight_remains<15)
# High Priority Shadow Word: Death when you are forcing the bonus from Devour Matter
actions.main+=/shadow_word_death,target_if=max:(target.health.pct<=20)*100+dot.devouring_plague.ticking,if=priest.force_devour_matter&talent.devour_matter
# Blast more burst :wicked:
actions.main+=/void_blast,target_if=max:(dot.devouring_plague.remains*1000+target.time_to_die),if=(dot.devouring_plague.remains>=execute_time|buff.entropic_rift.remains<=gcd.max|action.void_torrent.channeling&talent.void_empowerment)&(insanity.deficit>=16|cooldown.mind_blast.full_recharge_time<=gcd.max)&(!talent.mind_devourer|!buff.mind_devourer.up|buff.entropic_rift.remains<=gcd.max)
actions.main+=/wait,sec=cooldown.mind_blast.recharge_time,if=cooldown.mind_blast.recharge_time<buff.entropic_rift.remains&buff.entropic_rift.up&buff.entropic_rift.remains<gcd.max&cooldown.mind_blast.charges<1
# Complicated do not overcap mindblast and use it to protect against void bolt cd desync
actions.main+=/mind_blast,if=buff.voidform.up&full_recharge_time<=gcd.max&(!talent.insidious_ire|dot.devouring_plague.remains>=execute_time)&(cooldown.void_bolt.remains%gcd.max-cooldown.void_bolt.remains%%gcd.max)*gcd.max<=0.25&(cooldown.void_bolt.remains%gcd.max-cooldown.void_bolt.remains%%gcd.max)>=0.01
# Use Voidbolt on the enemy with the largest time to die. We do no care about dots because Voidbolt is only accessible inside voidform which guarantees maximum effect
actions.main+=/void_bolt,target_if=max:target.time_to_die,if=insanity.deficit>16&cooldown.void_bolt.remains<=0.1
# Do not overcap on insanity
actions.main+=/devouring_plague,target_if=max:target.time_to_die*(dot.devouring_plague.remains<=gcd.max|variable.dr_force_prio|!talent.distorted_reality&variable.me_force_prio),if=active_dot.devouring_plague<=1&dot.devouring_plague.remains<=gcd.max&(!talent.void_eruption|cooldown.void_eruption.remains>=gcd.max*3)|insanity.deficit<=16
# Cast Void Torrent at very high priority if Voidweaver
actions.main+=/void_torrent,target_if=max:(dot.devouring_plague.remains*1000+target.time_to_die),if=(dot.devouring_plague.ticking|talent.void_eruption&cooldown.void_eruption.up)&talent.entropic_rift&!variable.holding_crash
# Snipe SWDs with Depth of Shadows to spawn pets. Prefer targets with Devouring Plague on them.
actions.main+=/shadow_word_death,target_if=max:(target.health.pct<=20)*100+dot.devouring_plague.ticking,if=talent.depth_of_shadows
# Use Mind Blasts if using Inescapable Torment and you are capping charges or it will expire soon. Do not use if pooling Mindblast.
actions.main+=/mind_blast,target_if=max:dot.devouring_plague.remains,if=(cooldown.mind_blast.full_recharge_time<=gcd.max+execute_time|pet.fiend.remains<=execute_time+gcd.max)&pet.fiend.active&talent.inescapable_torment&pet.fiend.remains>=execute_time&active_enemies<=7&(!buff.mind_devourer.up|!talent.mind_devourer)&dot.devouring_plague.remains>execute_time&!variable.pooling_mindblasts
# High Priority Shadow Word: Death is Mindbender is expiring in less than a gcd plus wiggle room
actions.main+=/shadow_word_death,target_if=max:dot.devouring_plague.remains,if=pet.fiend.remains<=(gcd.max+1)&pet.fiend.active&talent.inescapable_torment&active_enemies<=7
# Use Voidbolt on the enemy with the largest time to die. Force a cooldown check here to make sure SimC doesn't wait too long (i.e. weird MF:I desync with GCD)
actions.main+=/void_bolt,target_if=max:target.time_to_die,if=cooldown.void_bolt.remains<=0.1
# Do not overcap MSI or MFI during Empowered Surges (Archon).
actions.main+=/call_action_list,name=empowered_filler,if=(buff.mind_spike_insanity.stack=1&talent.mind_spike|buff.mind_flay_insanity.stack=1&!talent.mind_spike|buff.power_surge.up)&talent.empowered_surges&!cooldown.void_eruption.up
# Hyper cringe optimisations that fish for TOF using heals. Set priest.twist_of_fate_heal_rppm=<rppm> to make this be used.
actions.main+=/call_action_list,name=heal_for_tof,if=!buff.twist_of_fate.up&buff.twist_of_fate_can_trigger_on_ally_heal.up&(talent.rhapsody|talent.divine_star|talent.halo)
# Spend your Insanity on Devouring Plague at will if the fight will end in less than 10s
actions.main+=/devouring_plague,if=fight_remains<=duration+4
# Use Devouring Plague to maximize uptime. Short circuit if you are capping on Insanity within 35 With Distorted Reality can maintain more than one at a time in multi-target.
actions.main+=/devouring_plague,target_if=max:target.time_to_die*(dot.devouring_plague.remains<=gcd.max|variable.dr_force_prio|!talent.distorted_reality&variable.me_force_prio),if=insanity.deficit<=35&talent.distorted_reality|buff.dark_ascension.up|buff.mind_devourer.up&cooldown.mind_blast.up&(cooldown.void_eruption.remains>=3*gcd.max|!talent.void_eruption)|buff.entropic_rift.up
# Use Void Torrent if it will get near full Mastery Value and you have Cthun and Void Eruption. Prune this action for Entropic Rift Builds.
actions.main+=/void_torrent,target_if=max:(dot.devouring_plague.remains*1000+target.time_to_die),if=!variable.holding_crash&!talent.entropic_rift,target_if=dot.devouring_plague.remains>=2.5
# Use Shadow Crash as long as you are not holding for adds and Vampiric Touch is within pandemic range
actions.main+=/shadow_crash,if=!variable.holding_crash&dot.vampiric_touch.refreshable
# Put out Vampiric Touch on enemies that will live at least 12s and Shadow Crash is not available soon
actions.main+=/vampiric_touch,target_if=max:(refreshable*10000+target.time_to_die)*(dot.vampiric_touch.ticking|!variable.dots_up),if=refreshable&target.time_to_die>12&(dot.vampiric_touch.ticking|!variable.dots_up)&(variable.max_vts>0|active_enemies=1)&(cooldown.shadow_crash.remains>=dot.vampiric_touch.remains|variable.holding_crash|!talent.whispering_shadows)&(!action.shadow_crash.in_flight|!talent.whispering_shadows)
# Spend Deathspeaker Procs
actions.main+=/shadow_word_death,target_if=max:dot.devouring_plague.remains,if=variable.dots_up&buff.deathspeaker.up
# Use all charges of Mind Blast if Vampiric Touch and Shadow Word: Pain are active and Mind Devourer is not active or you are prepping Void Eruption
actions.main+=/mind_blast,target_if=max:dot.devouring_plague.remains,if=(!buff.mind_devourer.up|!talent.mind_devourer|cooldown.void_eruption.up&talent.void_eruption)&!variable.pooling_mindblasts
actions.main+=/call_action_list,name=filler

actions.trinkets=use_item,name=darkmoon_deck_box_inferno,if=equipped.darkmoon_deck_box_inferno
actions.trinkets+=/use_item,name=darkmoon_deck_box_rime,if=equipped.darkmoon_deck_box_rime
actions.trinkets+=/use_item,name=darkmoon_deck_box_dance,if=equipped.darkmoon_deck_box_dance
actions.trinkets+=/use_item,name=dreambinder_loom_of_the_great_cycle,use_off_gcd=1,if=gcd.remains>0|fight_remains<20
actions.trinkets+=/use_item,name=conjured_chillglobe
actions.trinkets+=/use_item,name=iceblood_deathsnare,if=(!raid_event.adds.exists|raid_event.adds.up|spell_targets.iceblood_deathsnare>=5)|fight_remains<20
# Use Erupting Spear Fragment with cooldowns, adds are currently active, or the fight will end in less than 20 seconds
actions.trinkets+=/use_item,name=erupting_spear_fragment,if=(buff.power_infusion.up|raid_event.adds.up|fight_remains<20)&equipped.erupting_spear_fragment
# Use Belor'relos on cooldown except to hold for incoming adds or if already facing 5 or more targets
actions.trinkets+=/use_item,name=belorrelos_the_suncaller,if=(!raid_event.adds.exists|raid_event.adds.up|spell_targets.belorrelos_the_suncaller>=5|fight_remains<20)&equipped.belorrelos_the_suncaller
# Use Beacon to the Beyond on cooldown except to hold for incoming adds or if already facing 5 or more targets
actions.trinkets+=/use_item,name=beacon_to_the_beyond,if=(!raid_event.adds.exists|raid_event.adds.up|spell_targets.beacon_to_the_beyond>=5|fight_remains<20)&equipped.beacon_to_the_beyond
actions.trinkets+=/use_item,name=aberrant_spellforge
actions.trinkets+=/use_item,name=spymasters_web,if=buff.spymasters_report.stack=1&buff.power_infusion.up&!buff.spymasters_web.up|buff.power_infusion.up&(fight_remains<120)|(fight_remains<=20|buff.dark_ascension.up&fight_remains<=60|buff.entropic_rift.up&talent.entropic_rift&fight_remains<=30)&!buff.spymasters_web.up
actions.trinkets+=/use_items,if=(buff.voidform.up|buff.power_infusion.up|buff.dark_ascension.up|(cooldown.void_eruption.remains>10&trinket.cooldown.duration<=60))|fight_remains<20
actions.trinkets+=/use_item,name=desperate_invokers_codex,if=equipped.desperate_invokers_codex

```

# ActionPriorityLists\monk_windwalker.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats

# Executed every time the actor is available.
actions=auto_attack
# Move to target
actions+=/roll,if=movement.distance>5
actions+=/chi_torpedo,if=movement.distance>5
actions+=/flying_serpent_kick,if=movement.distance>5
actions+=/spear_hand_strike,if=target.debuff.casting.react
# Potion
actions+=/potion,if=buff.storm_earth_and_fire.up&pet.xuen_the_white_tiger.active|fight_remains<=30
# Use Trinkets
actions+=/call_action_list,name=trinkets
# Use Cooldowns
actions+=/call_action_list,name=cooldowns,if=talent.storm_earth_and_fire
# Default Priority
actions+=/call_action_list,name=default_aoe,if=active_enemies>=3
actions+=/call_action_list,name=default_st,if=active_enemies<3
actions+=/lights_judgment,if=buff.storm_earth_and_fire.down
actions+=/bag_of_tricks,if=buff.storm_earth_and_fire.down

# Use <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> while <a href='https://www.wowhead.com/spell=123904/invoke-xuen-the-white-tiger'>Invoke Xuen, the White Tiger</a> is active.
actions.cooldowns=invoke_external_buff,name=power_infusion,if=pet.xuen_the_white_tiger.active
actions.cooldowns+=/invoke_xuen_the_white_tiger,if=(active_enemies>2|debuff.acclamation.up)&(prev.tiger_palm|energy<60&!talent.inner_peace|energy<55&talent.inner_peace|chi>3)
actions.cooldowns+=/storm_earth_and_fire,if=(buff.invokers_delight.up|target.time_to_die>15&cooldown.storm_earth_and_fire.full_recharge_time<cooldown.invoke_xuen_the_white_tiger.remains&cooldown.strike_of_the_windlord.remains<2)|fight_remains<=30|buff.bloodlust.up&cooldown.invoke_xuen_the_white_tiger.remains
actions.cooldowns+=/touch_of_karma
actions.cooldowns+=/blood_fury,if=cooldown.invoke_xuen_the_white_tiger.remains>30|fight_remains<20
actions.cooldowns+=/berserking,if=cooldown.invoke_xuen_the_white_tiger.remains>60|fight_remains<15
actions.cooldowns+=/fireblood,if=cooldown.invoke_xuen_the_white_tiger.remains>30|fight_remains<10
actions.cooldowns+=/ancestral_call,if=cooldown.invoke_xuen_the_white_tiger.remains>30|fight_remains<20

# >=3 Targets
actions.default_aoe=tiger_palm,if=(energy>55&talent.inner_peace|energy>60&!talent.inner_peace)&combo_strike&chi.max-chi>=2&buff.teachings_of_the_monastery.stack<buff.teachings_of_the_monastery.max_stack&!buff.ordered_elements.up&(!set_bonus.tier30_2pc|set_bonus.tier30_2pc&buff.dance_of_chiji.up&!buff.blackout_reinforcement.up&talent.energy_burst)|buff.storm_earth_and_fire.remains>3&cooldown.fists_of_fury.remains<3&chi<2
actions.default_aoe+=/touch_of_death
actions.default_aoe+=/spinning_crane_kick,if=buff.dance_of_chiji.stack=2&combo_strike
actions.default_aoe+=/rising_sun_kick,target_if=min:debuff.mark_of_the_crane.remains,if=buff.ordered_elements.remains<2&buff.storm_earth_and_fire.up&talent.ordered_elements
actions.default_aoe+=/celestial_conduit,if=buff.storm_earth_and_fire.up&buff.ordered_elements.up&cooldown.strike_of_the_windlord.remains
actions.default_aoe+=/chi_burst,if=combo_strike
actions.default_aoe+=/spinning_crane_kick,if=buff.dance_of_chiji.stack=2|buff.dance_of_chiji.up&combo_strike&buff.storm_earth_and_fire.up
actions.default_aoe+=/whirling_dragon_punch
actions.default_aoe+=/strike_of_the_windlord
actions.default_aoe+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=buff.teachings_of_the_monastery.stack=8&talent.shadowboxing_treads
actions.default_aoe+=/fists_of_fury,target_if=max:debuff.acclamation.stack
actions.default_aoe+=/rising_sun_kick,target_if=min:debuff.mark_of_the_crane.remains,if=talent.xuens_battlegear|cooldown.whirling_dragon_punch.remains<3
actions.default_aoe+=/spinning_crane_kick,if=combo_strike
actions.default_aoe+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=!talent.knowledge_of_the_broken_temple&buff.teachings_of_the_monastery.stack=4&talent.shadowboxing_treads
actions.default_aoe+=/crackling_jade_lightning,if=buff.the_emperors_capacitor.stack>19&!buff.ordered_elements.up&combo_strike&talent.power_of_the_thunder_king
actions.default_aoe+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike&talent.shadowboxing_treads
actions.default_aoe+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike
actions.default_aoe+=/crackling_jade_lightning,if=buff.the_emperors_capacitor.stack>19&!buff.ordered_elements.up&combo_strike
actions.default_aoe+=/jadefire_stomp
actions.default_aoe+=/tiger_palm,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike&buff.ordered_elements.up&chi.deficit>=1

# <3 Targets
actions.default_st=tiger_palm,target_if=min:debuff.mark_of_the_crane.remains,if=(energy>55&talent.inner_peace|energy>60&!talent.inner_peace)&combo_strike&chi.max-chi>=2&buff.teachings_of_the_monastery.stack<buff.teachings_of_the_monastery.max_stack&!buff.ordered_elements.up&(!set_bonus.tier30_2pc|set_bonus.tier30_2pc&buff.dance_of_chiji.up&!buff.blackout_reinforcement.up&talent.energy_burst)
actions.default_st+=/touch_of_death
actions.default_st+=/celestial_conduit,if=buff.storm_earth_and_fire.up&buff.ordered_elements.up&cooldown.strike_of_the_windlord.remains
actions.default_st+=/rising_sun_kick,target_if=max:debuff.acclamation.stack,if=!pet.xuen_the_white_tiger.active&prev.tiger_palm|buff.storm_earth_and_fire.up&talent.ordered_elements
actions.default_st+=/strike_of_the_windlord,if=talent.gale_force&buff.invokers_delight.up
actions.default_st+=/fists_of_fury,target_if=max:debuff.acclamation.stack,if=buff.power_infusion.up&buff.bloodlust.up
actions.default_st+=/rising_sun_kick,target_if=max:debuff.acclamation.stack,if=buff.power_infusion.up&buff.bloodlust.up
actions.default_st+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=buff.teachings_of_the_monastery.stack=8
actions.default_st+=/whirling_dragon_punch
actions.default_st+=/strike_of_the_windlord,if=time>5
actions.default_st+=/spinning_crane_kick,if=combo_strike&buff.dance_of_chiji.up&set_bonus.tier30_2pc&!buff.blackout_reinforcement.up
actions.default_st+=/rising_sun_kick,target_if=max:debuff.acclamation.stack
actions.default_st+=/fists_of_fury,if=buff.ordered_elements.remains>execute_time|!buff.ordered_elements.up|buff.ordered_elements.remains<=gcd.max
actions.default_st+=/spinning_crane_kick,if=combo_strike&buff.dance_of_chiji.up&set_bonus.tier30_2pc&!buff.blackout_reinforcement.up&talent.energy_burst
actions.default_st+=/tiger_palm,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike&chi.deficit>=2&(!buff.ordered_elements.up|energy.time_to_max<=gcd.max*3)
actions.default_st+=/jadefire_stomp,if=talent.Singularly_Focused_Jade|talent.jadefire_harmony
actions.default_st+=/rising_sun_kick,target_if=max:debuff.acclamation.stack
actions.default_st+=/blackout_kick,if=combo_strike&buff.blackout_reinforcement.up
actions.default_st+=/chi_burst,if=!buff.ordered_elements.up
actions.default_st+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike&(buff.ordered_elements.up|buff.bok_proc.up&chi.deficit>=1&talent.energy_burst)
actions.default_st+=/spinning_crane_kick,if=combo_strike&buff.dance_of_chiji.up&(buff.ordered_elements.up|energy.time_to_max>=gcd.max*3&talent.sequenced_strikes&talent.energy_burst|!talent.sequenced_strikes|!talent.energy_burst|buff.dance_of_chiji.stack=2|buff.dance_of_chiji.remains<=gcd.max*3)
actions.default_st+=/crackling_jade_lightning,if=buff.the_emperors_capacitor.stack>19&!buff.ordered_elements.up&combo_strike
actions.default_st+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike
actions.default_st+=/jadefire_stomp
actions.default_st+=/tiger_palm,target_if=min:debuff.mark_of_the_crane.remains,if=combo_strike&buff.ordered_elements.up&chi.deficit>=1
actions.default_st+=/chi_burst
actions.default_st+=/spinning_crane_kick,if=combo_strike&buff.ordered_elements.up&talent.hit_combo
actions.default_st+=/blackout_kick,target_if=min:debuff.mark_of_the_crane.remains,if=buff.ordered_elements.up&!talent.hit_combo

actions.trinkets=use_item,name=epic_purple_shirt

```

# ActionPriorityLists\monk_brewmaster.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/snapshot_stats
actions.precombat+=/potion
actions.precombat+=/chi_burst

# Executed every time the actor is available.
actions=auto_attack
actions+=/expel_harm,if=buff.gift_of_the_ox.stack>4
actions+=/potion
actions+=/call_action_list,name=race_actions
actions+=/call_action_list,name=item_actions
actions+=/black_ox_brew,if=energy<40
actions+=/celestial_brew,if=buff.aspect_of_harmony_accumulator.value>0.98*health.max|(target.time_to_die<20&target.time_to_die>14&buff.aspect_of_harmony_accumulator.value>0.2*health.max)
actions+=/blackout_kick
actions+=/chi_burst
actions+=/weapons_of_order
actions+=/rising_sun_kick,if=!talent.fluidity_of_motion.enabled
actions+=/tiger_palm,if=buff.blackout_combo.up
actions+=/rising_sun_kick,if=talent.fluidity_of_motion.enabled
actions+=/purifying_brew,if=buff.blackout_combo.down
actions+=/breath_of_fire,if=buff.charred_passions.down
actions+=/exploding_keg
actions+=/keg_smash
actions+=/rushing_jade_wind
actions+=/invoke_niuzao
actions+=/tiger_palm
actions+=/spinning_crane_kick

actions.item_actions=use_item,slot=trinket1
actions.item_actions+=/use_item,slot=trinket2

actions.race_actions=blood_fury
actions.race_actions+=/berserking
actions.race_actions+=/arcane_torrent
actions.race_actions+=/lights_judgment
actions.race_actions+=/fireblood
actions.race_actions+=/ancestral_call
actions.race_actions+=/bag_of_tricks

```

# ActionPriorityLists\mage_frost.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/arcane_intellect
actions.precombat+=/snapshot_stats
actions.precombat+=/blizzard,if=active_enemies>=2&talent.ice_caller&!talent.fractured_frost|active_enemies>=3
actions.precombat+=/frostbolt,if=active_enemies<=2

# Executed every time the actor is available.
actions=counterspell
actions+=/call_action_list,name=cds
actions+=/run_action_list,name=aoe,if=active_enemies>=7&!set_bonus.tier30_2pc|active_enemies>=4&talent.ice_caller
actions+=/run_action_list,name=cleave,if=active_enemies>=2&active_enemies<=3
actions+=/run_action_list,name=st

actions.aoe=cone_of_cold,if=talent.coldest_snap&(prev_gcd.1.comet_storm|prev_gcd.1.frozen_orb&!talent.comet_storm)
actions.aoe+=/frozen_orb,if=!prev_gcd.1.glacial_spike|!freezable
actions.aoe+=/blizzard,if=!prev_gcd.1.glacial_spike|!freezable
actions.aoe+=/frostbolt,if=buff.icy_veins.up&(buff.deaths_chill.stack<9|buff.deaths_chill.stack=9&!action.frostbolt.in_flight)&buff.icy_veins.remains>8&talent.deaths_chill
actions.aoe+=/comet_storm,if=!prev_gcd.1.glacial_spike&(!talent.coldest_snap|cooldown.cone_of_cold.ready&cooldown.frozen_orb.remains>25|cooldown.cone_of_cold.remains>20)
actions.aoe+=/freeze,if=freezable&debuff.frozen.down&(!talent.glacial_spike|prev_gcd.1.glacial_spike)
actions.aoe+=/ice_nova,if=freezable&!prev_off_gcd.freeze&(prev_gcd.1.glacial_spike)
actions.aoe+=/frost_nova,if=freezable&!prev_off_gcd.freeze&(prev_gcd.1.glacial_spike&!remaining_winters_chill)
actions.aoe+=/shifting_power,if=cooldown.comet_storm.remains>10
actions.aoe+=/flurry,if=cooldown_react&!debuff.winters_chill.remains&buff.icicles.react=4&talent.glacial_spike&!freezable
actions.aoe+=/glacial_spike,if=buff.icicles.react=5&cooldown.blizzard.remains>gcd.max
actions.aoe+=/flurry,if=(freezable|!talent.glacial_spike)&cooldown_react&!debuff.winters_chill.remains&(buff.brain_freeze.react|!buff.fingers_of_frost.react)
actions.aoe+=/ice_lance,if=buff.fingers_of_frost.react|debuff.frozen.remains>travel_time|remaining_winters_chill
actions.aoe+=/ice_nova,if=active_enemies>=4&(!talent.glacial_spike|!freezable)
actions.aoe+=/dragons_breath,if=active_enemies>=7
actions.aoe+=/arcane_explosion,if=mana.pct>30&active_enemies>=7
actions.aoe+=/frostbolt
actions.aoe+=/call_action_list,name=movement

actions.cds=use_item,name=spoils_of_neltharus,if=buff.spoils_of_neltharus_mastery.up|buff.spoils_of_neltharus_haste.up&buff.bloodlust.down|buff.spoils_of_neltharus_vers.up&(buff.bloodlust.up)
actions.cds+=/potion,if=prev_off_gcd.icy_veins|fight_remains<60
actions.cds+=/use_item,name=dreambinder_loom_of_the_great_cycle,if=(equipped.nymues_unraveling_spindle&prev_gcd.1.nymues_unraveling_spindle)|fight_remains>2
actions.cds+=/use_item,name=belorrelos_the_suncaller,if=time>5&!prev_gcd.1.flurry
actions.cds+=/flurry,if=time=0&active_enemies<=2
actions.cds+=/icy_veins
actions.cds+=/invoke_external_buff,name=power_infusion,if=buff.power_infusion.down
actions.cds+=/invoke_external_buff,name=blessing_of_summer,if=buff.blessing_of_summer.down
actions.cds+=/blood_fury
actions.cds+=/berserking
actions.cds+=/lights_judgment
actions.cds+=/fireblood
actions.cds+=/ancestral_call

actions.cleave=comet_storm,if=prev_gcd.1.flurry|prev_gcd.1.cone_of_cold
actions.cleave+=/flurry,target_if=min:debuff.winters_chill.stack,if=cooldown_react&((prev_gcd.1.frostbolt&buff.icicles.react>=3)|prev_gcd.1.glacial_spike|(buff.icicles.react>=3&buff.icicles.react<5&charges_fractional=2))
actions.cleave+=/ice_lance,target_if=max:debuff.winters_chill.stack,if=talent.glacial_spike&debuff.winters_chill.down&buff.icicles.react=4&buff.fingers_of_frost.react
actions.cleave+=/ray_of_frost,target_if=max:debuff.winters_chill.stack,if=remaining_winters_chill=1
actions.cleave+=/glacial_spike,if=buff.icicles.react=5&(action.flurry.cooldown_react|remaining_winters_chill)
actions.cleave+=/frozen_orb,if=buff.fingers_of_frost.react<2&(!talent.ray_of_frost|cooldown.ray_of_frost.remains)
actions.cleave+=/cone_of_cold,if=talent.coldest_snap&cooldown.comet_storm.remains>10&cooldown.frozen_orb.remains>10&remaining_winters_chill=0&active_enemies>=3
actions.cleave+=/shifting_power,if=cooldown.frozen_orb.remains>10&(!talent.comet_storm|cooldown.comet_storm.remains>10)&(!talent.ray_of_frost|cooldown.ray_of_frost.remains>10)|cooldown.icy_veins.remains<20
actions.cleave+=/glacial_spike,if=buff.icicles.react=5
actions.cleave+=/ice_lance,target_if=max:debuff.winters_chill.stack,if=buff.fingers_of_frost.react&!prev_gcd.1.glacial_spike|remaining_winters_chill
actions.cleave+=/ice_nova,if=active_enemies>=4
actions.cleave+=/frostbolt
actions.cleave+=/call_action_list,name=movement

actions.movement=any_blink,if=movement.distance>10
actions.movement+=/ice_floes,if=buff.ice_floes.down
actions.movement+=/ice_nova
actions.movement+=/arcane_explosion,if=mana.pct>30&active_enemies>=2
actions.movement+=/fire_blast
actions.movement+=/ice_lance

actions.st=comet_storm,if=prev_gcd.1.flurry|prev_gcd.1.cone_of_cold
actions.st+=/flurry,if=cooldown_react&remaining_winters_chill=0&debuff.winters_chill.down&((prev_gcd.1.frostbolt&buff.icicles.react>=3|prev_gcd.1.frostbolt&buff.brain_freeze.react)|prev_gcd.1.glacial_spike|talent.glacial_spike&buff.icicles.react=4&!buff.fingers_of_frost.react)
actions.st+=/ice_lance,if=talent.glacial_spike&debuff.winters_chill.down&buff.icicles.react=4&buff.fingers_of_frost.react
actions.st+=/ray_of_frost,if=remaining_winters_chill=1
actions.st+=/glacial_spike,if=buff.icicles.react=5&(action.flurry.cooldown_react|remaining_winters_chill)
actions.st+=/frozen_orb,if=buff.fingers_of_frost.react<2&(!talent.ray_of_frost|cooldown.ray_of_frost.remains)
actions.st+=/cone_of_cold,if=talent.coldest_snap&cooldown.comet_storm.remains>10&cooldown.frozen_orb.remains>10&remaining_winters_chill=0&active_enemies>=3
actions.st+=/blizzard,if=active_enemies>=2&talent.ice_caller&talent.freezing_rain&(!talent.splintering_cold&!talent.ray_of_frost|buff.freezing_rain.up|active_enemies>=3)
actions.st+=/shifting_power,if=(buff.icy_veins.down|!talent.deaths_chill)&cooldown.frozen_orb.remains>10&(!talent.comet_storm|cooldown.comet_storm.remains>10)&(!talent.ray_of_frost|cooldown.ray_of_frost.remains>10)|cooldown.icy_veins.remains<20
actions.st+=/glacial_spike,if=buff.icicles.react=5
actions.st+=/ice_lance,if=buff.fingers_of_frost.react&!prev_gcd.1.glacial_spike|remaining_winters_chill
actions.st+=/ice_nova,if=active_enemies>=4
actions.st+=/frostbolt
actions.st+=/call_action_list,name=movement

```

# ActionPriorityLists\mage_fire.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/arcane_intellect
# APL Variable Option: This variable specifies whether Combustion should be used during Firestarter.
actions.precombat+=/variable,name=firestarter_combustion,default=-1,value=talent.sun_kings_blessing,if=variable.firestarter_combustion<0
# APL Variable Option: This variable specifies the number of targets at which Hot Streak Flamestrikes outside of Combustion should be used.
actions.precombat+=/variable,name=hot_streak_flamestrike,if=variable.hot_streak_flamestrike=0,value=4*(talent.quickflame|talent.flame_patch)+999*(!talent.flame_patch&!talent.quickflame)
# APL Variable Option: This variable specifies the number of targets at which Hard Cast Flamestrikes outside of Combustion should be used as filler.
actions.precombat+=/variable,name=hard_cast_flamestrike,if=variable.hard_cast_flamestrike=0,value=999
# APL Variable Option: This variable specifies the number of targets at which Hot Streak Flamestrikes are used during Combustion.
actions.precombat+=/variable,name=combustion_flamestrike,if=variable.combustion_flamestrike=0,value=4*(talent.quickflame|talent.flame_patch)+999*(!talent.flame_patch&!talent.quickflame)
# APL Variable Option: This variable specifies the number of targets at which Flamestrikes should be used to consume Fury of the Sun King.
actions.precombat+=/variable,name=skb_flamestrike,if=variable.skb_flamestrike=0,value=3*(talent.quickflame|talent.flame_patch)+999*(!talent.flame_patch&!talent.quickflame)
# APL Variable Option: This variable specifies the number of targets at which Arcane Explosion outside of Combustion should be used.
actions.precombat+=/variable,name=arcane_explosion,if=variable.arcane_explosion=0,value=999
# APL Variable Option: This variable specifies the percentage of mana below which Arcane Explosion will not be used.
actions.precombat+=/variable,name=arcane_explosion_mana,default=40,op=reset
# APL Variable Option: The number of targets at which Shifting Power can used during Combustion.
actions.precombat+=/variable,name=combustion_shifting_power,if=variable.combustion_shifting_power=0,value=999
# APL Variable Option: The time remaining on a cast when Combustion can be used in seconds.
actions.precombat+=/variable,name=combustion_cast_remains,default=0.3,op=reset
# APL Variable Option: This variable specifies the number of seconds of Fire Blast that should be pooled past the default amount.
actions.precombat+=/variable,name=overpool_fire_blasts,default=0,op=reset
# The duration of a Sun King's Blessing Combustion.
actions.precombat+=/variable,name=skb_duration,value=dbc.effect.1016075.base_value
# Whether a usable item used to buff Combustion is equipped.
actions.precombat+=/variable,name=combustion_on_use,value=equipped.gladiators_badge|equipped.moonlit_prism|equipped.irideus_fragment|equipped.spoils_of_neltharus|equipped.timebreaching_talon|equipped.horn_of_valor
# How long before Combustion should trinkets that trigger a shared category cooldown on other trinkets not be used?
actions.precombat+=/variable,name=on_use_cutoff,value=20,if=variable.combustion_on_use
actions.precombat+=/snapshot_stats
actions.precombat+=/mirror_image
actions.precombat+=/flamestrike,if=active_enemies>=variable.hot_streak_flamestrike
actions.precombat+=/pyroblast

# Executed every time the actor is available.
actions=counterspell
# The combustion_timing action list schedules the approximate time when Combustion should be used and stores the number of seconds until then in variable.time_to_combustion.
actions+=/call_action_list,name=combustion_timing
actions+=/potion,if=buff.potion.duration>variable.time_to_combustion+buff.combustion.duration
# Variable that estimates whether Shifting Power will be used before the next Combustion.
actions+=/variable,name=shifting_power_before_combustion,value=variable.time_to_combustion>cooldown.shifting_power.remains
actions+=/variable,name=item_cutoff_active,value=(variable.time_to_combustion<variable.on_use_cutoff|buff.combustion.remains>variable.skb_duration&!cooldown.item_cd_1141.remains)&((trinket.1.has_cooldown&trinket.1.cooldown.remains<variable.on_use_cutoff)+(trinket.2.has_cooldown&trinket.2.cooldown.remains<variable.on_use_cutoff)>1)
# The War Within S1 On-Use items with special use timings
actions+=/use_item,effect_name=treacherous_transmitter,if=buff.combustion.remains>10|fight_remains<25
actions+=/use_item,name=imperfect_ascendancy_serum,if=variable.time_to_combustion<3
actions+=/use_item,effect_name=spymasters_web,if=(buff.combustion.remains>10&fight_remains<60)|fight_remains<25
actions+=/use_item,effect_name=gladiators_badge,if=variable.time_to_combustion>cooldown-5
actions+=/use_items,if=!variable.item_cutoff_active
# Pool as many Fire Blasts as possible for Combustion.
actions+=/variable,use_off_gcd=1,use_while_casting=1,name=fire_blast_pooling,value=buff.combustion.down&action.fire_blast.charges_fractional+(variable.time_to_combustion+action.shifting_power.full_reduction*variable.shifting_power_before_combustion)%cooldown.fire_blast.duration-1<cooldown.fire_blast.max_charges+variable.overpool_fire_blasts%cooldown.fire_blast.duration-(buff.combustion.duration%cooldown.fire_blast.duration)%%1&variable.time_to_combustion<fight_remains
actions+=/call_action_list,name=combustion_phase,if=variable.time_to_combustion<=0|buff.combustion.up|variable.time_to_combustion<variable.combustion_precast_time&cooldown.combustion.remains<variable.combustion_precast_time
# Adjust the variable that controls Fire Blast usage to save Fire Blasts while Searing Touch is active with Sun King's Blessing.
actions+=/variable,use_off_gcd=1,use_while_casting=1,name=fire_blast_pooling,value=scorch_execute.active&action.fire_blast.full_recharge_time>3*gcd.max,if=!variable.fire_blast_pooling&talent.sun_kings_blessing
actions+=/shifting_power,if=buff.combustion.down&(!improved_scorch.active|debuff.improved_scorch.remains>cast_time+action.scorch.cast_time&!buff.fury_of_the_sun_king.up)&!buff.hot_streak.react&buff.hyperthermia.down&(talent.sun_kings_blessing&cooldown.phoenix_flames.charges<=1|!talent.sun_kings_blessing)
# Variable that controls Phoenix Flames usage to ensure its charges are pooled for Combustion when needed. Only use Phoenix Flames outside of Combustion when full charges can be obtained during the next Combustion.
actions+=/variable,name=phoenix_pooling,if=!talent.sun_kings_blessing,value=(variable.time_to_combustion+buff.combustion.duration-5<action.phoenix_flames.full_recharge_time+cooldown.phoenix_flames.duration-action.shifting_power.full_reduction*variable.shifting_power_before_combustion&variable.time_to_combustion<fight_remains|talent.sun_kings_blessing)&!talent.alexstraszas_fury
# When Hardcasting Flamestrike, Fire Blasts should be used to generate Hot Streaks and to extend Feel the Burn.
actions+=/fire_blast,use_off_gcd=1,use_while_casting=1,if=!variable.fire_blast_pooling&variable.time_to_combustion>0&active_enemies>=variable.hard_cast_flamestrike&!firestarter.active&!buff.hot_streak.react&(buff.heating_up.react&action.flamestrike.execute_remains<0.5|charges_fractional>=2)
actions+=/call_action_list,name=firestarter_fire_blasts,if=buff.combustion.down&firestarter.active&variable.time_to_combustion>0
# Avoid capping Fire Blast charges while channeling Shifting Power
actions+=/fire_blast,use_while_casting=1,if=action.shifting_power.executing&(full_recharge_time<action.shifting_power.tick_reduction|talent.sun_kings_blessing&buff.heating_up.react)
actions+=/call_action_list,name=standard_rotation,if=variable.time_to_combustion>0&buff.combustion.down
actions+=/ice_nova,if=!scorch_execute.active
actions+=/scorch

actions.active_talents=meteor,if=buff.combustion.up|(buff.sun_kings_blessing.max_stack-buff.sun_kings_blessing.stack>4|variable.time_to_combustion<=0|buff.combustion.remains>travel_time|!talent.sun_kings_blessing&(cooldown.meteor.duration<variable.time_to_combustion|fight_remains<variable.time_to_combustion))
# With Alexstrasza's Fury when Combustion is not active, Dragon's Breath should be used to convert Heating Up to a Hot Streak.
actions.active_talents+=/dragons_breath,if=talent.alexstraszas_fury&(buff.combustion.down&!buff.hot_streak.react)&(buff.feel_the_burn.up|time>15)&(!improved_scorch.active)

actions.combustion_cooldowns=potion
actions.combustion_cooldowns+=/blood_fury
actions.combustion_cooldowns+=/berserking,if=buff.combustion.up
actions.combustion_cooldowns+=/fireblood
actions.combustion_cooldowns+=/ancestral_call
actions.combustion_cooldowns+=/invoke_external_buff,name=power_infusion,if=buff.power_infusion.down
actions.combustion_cooldowns+=/invoke_external_buff,name=blessing_of_summer,if=buff.blessing_of_summer.down
actions.combustion_cooldowns+=/use_item,effect_name=gladiators_badge

# Other cooldowns that should be used with Combustion should only be used with an actual Combustion cast and not with a Sun King's Blessing proc.
actions.combustion_phase=call_action_list,name=combustion_cooldowns,if=buff.combustion.remains>variable.skb_duration|fight_remains<20
actions.combustion_phase+=/call_action_list,name=active_talents
# If Combustion is down, precast something before activating it.
actions.combustion_phase+=/flamestrike,if=buff.combustion.down&buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.remains>cast_time&buff.fury_of_the_sun_king.expiration_delay_remains=0&cooldown.combustion.remains<cast_time&active_enemies>=variable.skb_flamestrike
actions.combustion_phase+=/pyroblast,if=buff.combustion.down&buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.remains>cast_time&(buff.fury_of_the_sun_king.expiration_delay_remains=0|buff.flame_accelerant.up)
actions.combustion_phase+=/meteor,if=talent.isothermic_core&buff.combustion.down&cooldown.combustion.remains<cast_time
actions.combustion_phase+=/fireball,if=buff.combustion.down&cooldown.combustion.remains<cast_time&active_enemies<2&!improved_scorch.active&!(talent.sun_kings_blessing&talent.flame_accelerant)
actions.combustion_phase+=/scorch,if=buff.combustion.down&cooldown.combustion.remains<cast_time
# Combustion should be used when the precast is almost finished or when Meteor is about to land.
actions.combustion_phase+=/combustion,use_off_gcd=1,use_while_casting=1,if=hot_streak_spells_in_flight=0&buff.combustion.down&variable.time_to_combustion<=0&(action.scorch.executing&action.scorch.execute_remains<variable.combustion_cast_remains|action.fireball.executing&action.fireball.execute_remains<variable.combustion_cast_remains|action.pyroblast.executing&action.pyroblast.execute_remains<variable.combustion_cast_remains|action.flamestrike.executing&action.flamestrike.execute_remains<variable.combustion_cast_remains|action.meteor.in_flight&action.meteor.in_flight_remains<variable.combustion_cast_remains)
actions.combustion_phase+=/fire_blast,use_off_gcd=1,use_while_casting=1,if=!variable.fire_blast_pooling&(!improved_scorch.active|action.scorch.executing|debuff.improved_scorch.remains>4*gcd.max)&(buff.fury_of_the_sun_king.down|action.pyroblast.executing)&buff.combustion.up&!buff.hot_streak.react&hot_streak_spells_in_flight+buff.heating_up.react*(gcd.remains>0)<2
# Cancelaura HT if SKB is ready
actions.combustion_phase+=/cancel_buff,name=hyperthermia,if=buff.fury_of_the_sun_king.react
# Spend Hot Streaks during Combustion at high priority.
actions.combustion_phase+=/flamestrike,if=(buff.hot_streak.react&active_enemies>=variable.combustion_flamestrike)|(buff.hyperthermia.react&active_enemies>=variable.combustion_flamestrike-talent.hyperthermia)
actions.combustion_phase+=/pyroblast,if=buff.hyperthermia.react
actions.combustion_phase+=/pyroblast,if=buff.hot_streak.react&buff.combustion.up
actions.combustion_phase+=/pyroblast,if=prev_gcd.1.scorch&buff.heating_up.react&active_enemies<variable.combustion_flamestrike&buff.combustion.up
# Spend Fury of the Sun King procs inside of combustion.
actions.combustion_phase+=/flamestrike,if=buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.remains>cast_time&active_enemies>=variable.skb_flamestrike&buff.fury_of_the_sun_king.expiration_delay_remains=0
actions.combustion_phase+=/pyroblast,if=buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.remains>cast_time&buff.fury_of_the_sun_king.expiration_delay_remains=0
actions.combustion_phase+=/phoenix_flames,if=talent.phoenix_reborn&buff.heating_up.react+hot_streak_spells_in_flight<2&buff.flames_fury.up
actions.combustion_phase+=/fireball,if=buff.frostfire_empowerment.up&!buff.hot_streak.react&!buff.excess_frost.up
actions.combustion_phase+=/scorch,if=improved_scorch.active&(debuff.improved_scorch.remains<4*gcd.max)&active_enemies<variable.combustion_flamestrike
actions.combustion_phase+=/scorch,if=buff.heat_shimmer.react&(talent.scald|talent.improved_scorch)&active_enemies<variable.combustion_flamestrike
# Use Phoenix Flames and Scorch in Combustion to help generate Hot Streaks when Fire Blasts are not available or need to be conserved.
actions.combustion_phase+=/phoenix_flames,if=(!talent.call_of_the_sun_king&travel_time<buff.combustion.remains|(talent.call_of_the_sun_king&buff.combustion.remains<4|buff.sun_kings_blessing.stack<8))&buff.heating_up.react+hot_streak_spells_in_flight<2
actions.combustion_phase+=/fireball,if=buff.frostfire_empowerment.up&!buff.hot_streak.react
actions.combustion_phase+=/scorch,if=buff.combustion.remains>cast_time&cast_time>=gcd.max
actions.combustion_phase+=/fireball,if=buff.combustion.remains>cast_time

# Helper variable that contains the actual estimated time that the next Combustion will be ready.
actions.combustion_timing=variable,use_off_gcd=1,use_while_casting=1,name=combustion_ready_time,value=cooldown.combustion.remains*expected_kindling_reduction
# The cast time of the spell that will be precast into Combustion.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=combustion_precast_time,value=action.fireball.cast_time*(active_enemies<variable.combustion_flamestrike)+action.flamestrike.cast_time*(active_enemies>=variable.combustion_flamestrike)-variable.combustion_cast_remains
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,value=variable.combustion_ready_time
# Delay Combustion for after Firestarter unless variable.firestarter_combustion is set.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,op=max,value=firestarter.remains,if=talent.firestarter&!variable.firestarter_combustion
# Delay Combustion until SKB is ready during Firestarter
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,op=max,value=(buff.sun_kings_blessing.max_stack-buff.sun_kings_blessing.stack)*(3*gcd.max),if=talent.sun_kings_blessing&firestarter.active&buff.fury_of_the_sun_king.down
# Delay Combustion for Gladiators Badge, unless it would be delayed longer than 20 seconds.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,op=max,value=cooldown.gladiators_badge_345228.remains,if=equipped.gladiators_badge&cooldown.gladiators_badge_345228.remains-20<variable.time_to_combustion
# Delay Combustion until Combustion expires if it's up.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,op=max,value=buff.combustion.remains
# Raid Events: Delay Combustion for add spawns of 3 or more adds that will last longer than 15 seconds. These values aren't necessarily optimal in all cases.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,op=max,value=raid_event.adds.in,if=raid_event.adds.exists&raid_event.adds.count>=3&raid_event.adds.duration>15
# Raid Events: Always use Combustion with vulnerability raid events, override any delays listed above to make sure it gets used here.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,value=raid_event.vulnerable.in*!raid_event.vulnerable.up,if=raid_event.vulnerable.exists&variable.combustion_ready_time<raid_event.vulnerable.in
# Use the next Combustion on cooldown if it would not be expected to delay the scheduled one or the scheduled one would happen less than 20 seconds before the fight ends.
actions.combustion_timing+=/variable,use_off_gcd=1,use_while_casting=1,name=time_to_combustion,value=variable.combustion_ready_time,if=variable.combustion_ready_time+cooldown.combustion.duration*(1-(0.4+0.2*talent.firestarter)*talent.kindling)<=variable.time_to_combustion|variable.time_to_combustion>fight_remains-20

# While casting Fireball or Pyroblast, convert Heating Up to a Hot Streak!
actions.firestarter_fire_blasts=fire_blast,use_while_casting=1,if=!variable.fire_blast_pooling&!buff.hot_streak.react&(action.fireball.execute_remains>gcd.remains|action.pyroblast.executing)&buff.heating_up.react+hot_streak_spells_in_flight=1&(cooldown.shifting_power.ready|charges>1|buff.feel_the_burn.remains<2*gcd.max)
# If not casting anything, use Fire Blast to trigger Hot Streak! only if Feel the Burn is talented and would expire before the GCD ends or if Shifting Power is available.
actions.firestarter_fire_blasts+=/fire_blast,use_off_gcd=1,if=!variable.fire_blast_pooling&buff.heating_up.react+hot_streak_spells_in_flight=1&(talent.feel_the_burn&buff.feel_the_burn.remains<gcd.remains|cooldown.shifting_power.ready)&time>0

actions.standard_rotation=flamestrike,if=active_enemies>=variable.hot_streak_flamestrike&(buff.hot_streak.react|buff.hyperthermia.react)
actions.standard_rotation+=/pyroblast,if=(buff.hyperthermia.react|buff.hot_streak.react&(buff.hot_streak.remains<action.fireball.execute_time)|buff.hot_streak.react&(hot_streak_spells_in_flight|firestarter.active|talent.call_of_the_sun_king&action.phoenix_flames.charges)|buff.hot_streak.react&scorch_execute.active)
actions.standard_rotation+=/flamestrike,if=active_enemies>=variable.skb_flamestrike&buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.expiration_delay_remains=0
actions.standard_rotation+=/scorch,if=improved_scorch.active&debuff.improved_scorch.remains<action.pyroblast.cast_time+5*gcd.max&buff.fury_of_the_sun_king.up&!action.scorch.in_flight
actions.standard_rotation+=/pyroblast,if=buff.fury_of_the_sun_king.up&buff.fury_of_the_sun_king.expiration_delay_remains=0
# During the standard rotation, only use Fire Blasts when they are not being pooled for  Combustion. Use Fire Blast either during a Fireball/Pyroblast cast when Heating Up is active or during execute with Searing Touch.
actions.standard_rotation+=/fire_blast,use_off_gcd=1,use_while_casting=1,if=!firestarter.active&(!variable.fire_blast_pooling|talent.spontaneous_combustion)&buff.fury_of_the_sun_king.down&(((action.fireball.executing&(action.fireball.execute_remains<0.5|!talent.hyperthermia)|action.pyroblast.executing&(action.pyroblast.execute_remains<0.5))&buff.heating_up.react)|(scorch_execute.active&(!improved_scorch.active|debuff.improved_scorch.stack=debuff.improved_scorch.max_stack|full_recharge_time<3)&(buff.heating_up.react&!action.scorch.executing|!buff.hot_streak.react&!buff.heating_up.react&action.scorch.executing&!hot_streak_spells_in_flight)))
# We will munch Fireblasts during Hyperthermia
actions.standard_rotation+=/fire_blast,use_off_gcd=1,use_while_casting=1,if=buff.hyperthermia.up&charges>0&buff.heating_up.react
actions.standard_rotation+=/pyroblast,if=prev_gcd.1.scorch&buff.heating_up.react&scorch_execute.active&active_enemies<variable.hot_streak_flamestrike
actions.standard_rotation+=/scorch,if=improved_scorch.active&debuff.improved_scorch.remains<4*gcd.max
actions.standard_rotation+=/fireball,if=buff.frostfire_empowerment.up&!buff.hot_streak.react&!buff.excess_frost.up
actions.standard_rotation+=/scorch,if=improved_scorch.active&debuff.improved_scorch.stack<debuff.improved_scorch.max_stack
actions.standard_rotation+=/scorch,if=buff.heat_shimmer.react&(talent.scald|talent.improved_scorch)&active_enemies<variable.combustion_flamestrike
# SKB prefers to not pool Phoenix Flames.
actions.standard_rotation+=/phoenix_flames,if=talent.sun_kings_blessing&talent.call_of_the_sun_king&!buff.hot_streak.react&hot_streak_spells_in_flight<2
# UI and default fire will pool.
actions.standard_rotation+=/phoenix_flames,if=!talent.sun_kings_blessing&talent.call_of_the_sun_king&!buff.hot_streak.react&hot_streak_spells_in_flight<2&(!variable.phoenix_pooling&buff.flames_fury.up|charges_fractional>2.5|charges_fractional>1.5|buff.flames_fury.react)&(!talent.feel_the_burn|buff.feel_the_burn.remains<3*gcd.max|buff.flames_fury.react)
actions.standard_rotation+=/call_action_list,name=active_talents
actions.standard_rotation+=/dragons_breath,if=active_enemies>1&talent.alexstraszas_fury
actions.standard_rotation+=/scorch,if=(scorch_execute.active|buff.heat_shimmer.react)
actions.standard_rotation+=/arcane_explosion,if=active_enemies>=variable.arcane_explosion&mana.pct>=variable.arcane_explosion_mana
# With enough targets, it is a gain to cast Flamestrike as filler instead of Fireball. This is currently never true up to 10t.
actions.standard_rotation+=/flamestrike,if=active_enemies>=variable.hard_cast_flamestrike
actions.standard_rotation+=/fireball

```

# ActionPriorityLists\mage_arcane.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/arcane_intellect
actions.precombat+=/variable,name=aoe_target_count,op=reset,default=2
actions.precombat+=/variable,name=aoe_target_count,op=set,value=9,if=!talent.arcing_cleave
actions.precombat+=/variable,name=opener,op=set,value=1
actions.precombat+=/variable,name=steroid_trinket_equipped,op=set,value=equipped.gladiators_badge|equipped.irideus_fragment|equipped.spoils_of_neltharus|equipped.timebreaching_talon|equipped.ashes_of_the_embersoul|equipped.nymues_unraveling_spindle|equipped.signet_of_the_priory|equipped.high_speakers_accretion|equipped.spymasters_web|equipped.treacherous_transmitter
actions.precombat+=/snapshot_stats
actions.precombat+=/mirror_image
actions.precombat+=/arcane_blast,if=!talent.evocation
actions.precombat+=/evocation,if=talent.evocation

# Executed every time the actor is available.
actions=counterspell
actions+=/potion,if=buff.siphon_storm.up|(!talent.evocation&cooldown.arcane_surge.ready)
actions+=/lights_judgment,if=buff.arcane_surge.down&debuff.touch_of_the_magi.down&active_enemies>=2
actions+=/berserking,if=prev_gcd.1.arcane_surge
actions+=/blood_fury,if=prev_gcd.1.arcane_surge
actions+=/fireblood,if=prev_gcd.1.arcane_surge
actions+=/ancestral_call,if=prev_gcd.1.arcane_surge
# Invoke Externals with cooldowns except Autumn which should come just after cooldowns
actions+=/invoke_external_buff,name=power_infusion,if=prev_gcd.1.arcane_surge
actions+=/invoke_external_buff,name=blessing_of_summer,if=prev_gcd.1.arcane_surge
actions+=/invoke_external_buff,name=blessing_of_autumn,if=cooldown.touch_of_the_magi.remains>5
# Trinket specific use cases vary, default is just with cooldowns
actions+=/use_items,if=prev_gcd.1.arcane_surge|prev_gcd.1.evocation|fight_remains<20|!variable.steroid_trinket_equipped
actions+=/use_item,name=spymasters_web,if=(prev_gcd.1.arcane_surge|prev_gcd.1.evocation)&(fight_remains<80|target.health.pct<35|!talent.arcane_bombardment)|fight_remains<20
actions+=/use_item,name=high_speakers_accretion,if=(prev_gcd.1.arcane_surge|prev_gcd.1.evocation)|cooldown.evocation.remains<7|fight_remains<20
actions+=/use_item,name=treacherous_transmitter,if=((prev_gcd.1.arcane_surge|prev_gcd.1.evocation)&variable.opener)|cooldown.evocation.remains<6|fight_remains<20
actions+=/do_treacherous_transmitter_task,use_off_gcd=1,if=buff.siphon_storm.up|fight_remains<20
actions+=/use_item,name=aberrant_spellforge,if=!variable.steroid_trinket_equipped|buff.siphon_storm.down|(equipped.spymasters_web&target.health.pct>35)
actions+=/use_item,name=mad_queens_mandate,if=!variable.steroid_trinket_equipped|buff.siphon_storm.down
actions+=/use_item,name=mereldars_toll,if=!variable.steroid_trinket_equipped|buff.siphon_storm.down
actions+=/variable,name=opener,op=set,if=debuff.touch_of_the_magi.up&variable.opener,value=0
actions+=/arcane_barrage,if=fight_remains<2
# Enter cooldowns, then action list depending on your hero talent choices
actions+=/call_action_list,name=cd_opener
actions+=/call_action_list,name=sunfury_aoe,if=active_enemies>=(variable.aoe_target_count+talent.impetus-talent.reverberate)&talent.spellfire_spheres
actions+=/call_action_list,name=spellslinger_aoe,if=active_enemies>=(variable.aoe_target_count+talent.impetus)&talent.splintering_sorcery
actions+=/call_action_list,name=sunfury,if=talent.spellfire_spheres
actions+=/call_action_list,name=spellslinger,if=talent.splintering_sorcery
actions+=/arcane_barrage

# Touch of the Magi used when Arcane Barrage is mid-flight or if you just used Arcane Surge and you don't have 4 Arcane Charges
actions.cd_opener=touch_of_the_magi,use_off_gcd=1,if=prev_gcd.1.arcane_barrage&(action.arcane_barrage.in_flight_remains<=0.5|gcd.remains<=0.5)|prev_gcd.1.arcane_surge&buff.arcane_charge.stack<4
# In single target, use Presence of Mind at the very end of Touch of the Magi, then cancelaura the buff to start the cooldown, wait is to simulate the delay of hitting Presence of Mind after another spell cast
actions.cd_opener+=/cancel_buff,name=presence_of_mind,use_off_gcd=1,if=prev_gcd.1.arcane_blast&buff.presence_of_mind.stack=1
actions.cd_opener+=/presence_of_mind,if=debuff.touch_of_the_magi.remains<=gcd.max&buff.nether_precision.up&active_enemies<variable.aoe_target_count&!talent.unerring_proficiency
actions.cd_opener+=/wait,sec=0.05,if=buff.presence_of_mind.up&prev_gcd.1.arcane_blast,line_cd=15
actions.cd_opener+=/arcane_blast,if=buff.presence_of_mind.up
# Use Orb for charges if you have High Voltage, then evocation, then Missiles for Nether Precision, then Arcane Surge
actions.cd_opener+=/arcane_orb,if=talent.high_voltage&variable.opener,line_cd=10
actions.cd_opener+=/evocation,if=cooldown.arcane_surge.remains<gcd.max*4&cooldown.touch_of_the_magi.remains<gcd.max*7
actions.cd_opener+=/arcane_missiles,if=variable.opener,interrupt_if=!gcd.remains,interrupt_immediate=1,interrupt_global=1,line_cd=10
actions.cd_opener+=/arcane_surge,if=cooldown.touch_of_the_magi.remains<gcd.max*3

actions.spellslinger=shifting_power,if=((buff.arcane_surge.down&buff.siphon_storm.down&debuff.touch_of_the_magi.down&cooldown.evocation.remains>15&cooldown.touch_of_the_magi.remains>15)&(cooldown.arcane_orb.remains&action.arcane_orb.charges=0)&fight_remains>10)|(prev_gcd.1.arcane_barrage&(buff.arcane_surge.up|debuff.touch_of_the_magi.up|cooldown.evocation.remains<20)),interrupt_if=(cooldown.evocation.ready&cooldown.arcane_surge.remains<3),interrupt_immediate=1,interrupt_global=1
actions.spellslinger+=/supernova,if=debuff.touch_of_the_magi.remains<=gcd.max&buff.unerring_proficiency.stack=30
actions.spellslinger+=/arcane_orb,if=buff.arcane_charge.stack<2
# Always queue Arcane Barrage on the second stack of Nether Precision as Spellslinger
actions.spellslinger+=/arcane_barrage,if=(buff.nether_precision.stack=1&time-action.arcane_blast.last_used<0.015)|(cooldown.touch_of_the_magi.ready&buff.nether_precision.stack=2)
actions.spellslinger+=/arcane_missiles,if=(buff.clearcasting.react&buff.nether_precision.down)|(buff.clearcasting.react&buff.clearcasting.stack=3),interrupt_if=!gcd.remains&(!talent.high_voltage|buff.arcane_charge.stack=4),interrupt_immediate=1,interrupt_global=1,chain=1
actions.spellslinger+=/arcane_blast
actions.spellslinger+=/arcane_barrage

actions.spellslinger_aoe=supernova,if=buff.unerring_proficiency.stack=30
actions.spellslinger_aoe+=/cancel_buff,name=presence_of_mind,use_off_gcd=1,if=(debuff.magis_spark_arcane_blast.up&time-action.arcane_blast.last_used>0.015)
# Use Shifting Power whenever as long as you'll get some cooldown reduction on your cds, especially if you get a Time Anomaly proc, this usually works out to just using it off cooldown
actions.spellslinger_aoe+=/shifting_power,if=(prev_gcd.1.arcane_barrage&(buff.arcane_surge.up|debuff.touch_of_the_magi.up|cooldown.evocation.remains<20)&talent.shifting_shards),interrupt_if=(cooldown.evocation.ready&cooldown.arcane_surge.remains<3),interrupt_immediate=1,interrupt_global=1
actions.spellslinger_aoe+=/arcane_orb,if=buff.arcane_charge.stack<2
# Blast in AOE for Magi's Spark
actions.spellslinger_aoe+=/arcane_blast,if=(debuff.magis_spark_arcane_blast.up&time-action.arcane_blast.last_used>0.015)
actions.spellslinger_aoe+=/arcane_barrage,if=(talent.arcane_tempo&buff.arcane_tempo.remains<gcd.max)|((buff.intuition.up&(buff.arcane_charge.stack=buff.arcane_charge.max_stack|!talent.high_voltage))&buff.nether_precision.up)|(buff.nether_precision.up&action.arcane_blast.executing)
# Clearcasting is exclusively spent on Arcane Missiles in AOE and always interrupted after the global cooldown ends
actions.spellslinger_aoe+=/arcane_missiles,if=buff.clearcasting.react&((talent.high_voltage&buff.arcane_charge.stack<buff.arcane_charge.max_stack)|buff.aether_attunement.up|talent.arcane_harmony)&((talent.high_voltage&buff.arcane_charge.stack<buff.arcane_charge.max_stack)|!buff.nether_precision.up),interrupt_if=!gcd.remains,interrupt_immediate=1,interrupt_global=1,chain=1
# Only use Presence of Mind at low charges, use these to get to 4 Charges, but cancelaura the buff if you need to queue Arcane Barrage with Magi's Spark.
actions.spellslinger_aoe+=/presence_of_mind,if=buff.arcane_charge.stack=3|buff.arcane_charge.stack=2
actions.spellslinger_aoe+=/arcane_blast,if=buff.presence_of_mind.up
actions.spellslinger_aoe+=/arcane_barrage,if=(buff.arcane_charge.stack=buff.arcane_charge.max_stack)
actions.spellslinger_aoe+=/arcane_explosion

actions.sunfury=shifting_power,if=((buff.arcane_surge.down&buff.siphon_storm.down&debuff.touch_of_the_magi.down&cooldown.evocation.remains>15&cooldown.touch_of_the_magi.remains>15)&fight_remains>10)&buff.arcane_soul.down
actions.sunfury+=/arcane_orb,if=buff.arcane_charge.stack<2&buff.arcane_soul.down
# Always increment your Spellfire Spheres so that Nether Precision lines up better with Burden of Power
actions.sunfury+=/arcane_blast,if=((buff.spellfire_spheres.stack=3&time-action.arcane_blast.last_used<0.015)|(buff.spellfire_spheres.stack=4&time-action.arcane_blast.last_used>0.015))&buff.arcane_soul.down
actions.sunfury+=/arcane_missiles,if=buff.clearcasting.react&buff.glorious_incandescence.down&(buff.nether_precision.down|(buff.clearcasting.stack=3)|(buff.nether_precision.stack=1&time-action.arcane_blast.last_used<0.015)),interrupt_if=!gcd.remains,interrupt_immediate=1,interrupt_global=1,chain=1
actions.sunfury+=/arcane_barrage,if=buff.glorious_incandescence.up|(buff.burden_of_power.down&buff.intuition.up&time-action.arcane_blast.last_used<0.015)|buff.arcane_soul.up|(buff.arcane_charge.stack=4&cooldown.touch_of_the_magi.ready)
actions.sunfury+=/arcane_blast
actions.sunfury+=/arcane_barrage

# Spam Arcane Barrage during Arcane Soul, ensuring that you always get to maximum Clearcasting by the end.
actions.sunfury_aoe=arcane_barrage,if=buff.arcane_soul.up&buff.clearcasting.stack<3
actions.sunfury_aoe+=/arcane_missiles,if=buff.arcane_soul.up,interrupt_if=!gcd.remains,interrupt_immediate=1,interrupt_global=1,chain=1
actions.sunfury_aoe+=/cancel_buff,name=presence_of_mind,use_off_gcd=1,if=(debuff.magis_spark_arcane_blast.up&time-action.arcane_blast.last_used>0.015)|(buff.burden_of_power.up&time-action.arcane_blast.last_used>0.015&buff.arcane_charge.stack=4)
# For Sunfury, Shifting Power only when you're not under the effect of any cooldowns
actions.sunfury_aoe+=/shifting_power,if=((buff.arcane_surge.down&buff.siphon_storm.down&debuff.touch_of_the_magi.down&cooldown.evocation.remains>15&cooldown.touch_of_the_magi.remains>15)&(cooldown.arcane_orb.remains&action.arcane_orb.charges=0)&fight_remains>10)
actions.sunfury_aoe+=/arcane_orb,if=buff.arcane_charge.stack<2&cooldown.touch_of_the_magi.remains>18&(!talent.high_voltage|!buff.clearcasting.up)
# Always queue Arcane Barrage after Arcane Blast when you have Burden of Power
actions.sunfury_aoe+=/arcane_blast,if=(debuff.magis_spark_arcane_blast.up&time-action.arcane_blast.last_used>0.015)|(buff.burden_of_power.up&time-action.arcane_blast.last_used>0.015&buff.arcane_charge.stack=4)
actions.sunfury_aoe+=/arcane_barrage,if=(talent.arcane_tempo&buff.arcane_tempo.remains<gcd.max)|((buff.intuition.up&(buff.arcane_charge.stack=buff.arcane_charge.max_stack|!talent.high_voltage))&buff.nether_precision.up)|(buff.nether_precision.up&action.arcane_blast.executing)
actions.sunfury_aoe+=/arcane_missiles,if=buff.clearcasting.react&((talent.high_voltage&buff.arcane_charge.stack<buff.arcane_charge.max_stack)|buff.aether_attunement.up|talent.arcane_harmony)&((talent.high_voltage&buff.arcane_charge.stack<buff.arcane_charge.max_stack)|!buff.nether_precision.up),interrupt_if=!gcd.remains,interrupt_immediate=1,interrupt_global=1,chain=1
actions.sunfury_aoe+=/arcane_barrage,if=(buff.arcane_charge.stack=buff.arcane_charge.max_stack)
actions.sunfury_aoe+=/presence_of_mind,if=buff.arcane_charge.stack=3|buff.arcane_charge.stack=2
actions.sunfury_aoe+=/arcane_explosion,if=talent.reverberate
actions.sunfury_aoe+=/arcane_blast
actions.sunfury_aoe+=/arcane_barrage

```

# ActionPriorityLists\hunter_survival.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/summon_pet
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats

# Executed every time the actor is available.
actions=auto_attack
actions+=/call_action_list,name=cds
actions+=/call_action_list,name=plst,if=active_enemies<3&talent.vicious_hunt
actions+=/call_action_list,name=plcleave,if=active_enemies>2&talent.vicious_hunt
actions+=/call_action_list,name=sentst,if=active_enemies<3&!talent.vicious_hunt
actions+=/call_action_list,name=sentcleave,if=active_enemies>2&!talent.vicious_hunt
# simply fires off if there is absolutely nothing else to press.
actions+=/arcane_torrent
actions+=/bag_of_tricks
actions+=/lights_judgment

# COOLDOWNS ACTIONLIST
actions.cds=blood_fury,if=buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault
actions.cds+=/invoke_external_buff,name=power_infusion,if=buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault
actions.cds+=/harpoon,if=prev.kill_command
actions.cds+=/ancestral_call,if=buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault
actions.cds+=/fireblood,if=buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault
actions.cds+=/berserking,if=buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault|time_to_die<13
actions.cds+=/muzzle
actions.cds+=/potion,if=target.time_to_die<25|buff.coordinated_assault.up|!talent.coordinated_assault&cooldown.spearhead.remains|!talent.spearhead&!talent.coordinated_assault
actions.cds+=/use_item,name=algethar_puzzle_box,use_off_gcd=1
actions.cds+=/use_item,name=manic_grieftorch
actions.cds+=/use_item,name=beacon_to_the_beyond
actions.cds+=/use_items,if=cooldown.coordinated_assault.remains|cooldown.spearhead.remains
actions.cds+=/aspect_of_the_eagle,if=target.distance>=6

# PACK LEADER AOE ACTIONLIST
actions.plcleave=spearhead,if=cooldown.coordinated_assault.remains
actions.plcleave+=/kill_command,target_if=min:bloodseeker.remains,if=buff.relentless_primal_ferocity.up&buff.tip_of_the_spear.stack<1
actions.plcleave+=/explosive_shot,if=buff.bombardier.remains
actions.plcleave+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&cooldown.wildfire_bomb.charges_fractional>1.7|cooldown.wildfire_bomb.charges_fractional>1.9|cooldown.coordinated_assault.remains<2*gcd
actions.plcleave+=/coordinated_assault,if=!talent.bombardier|talent.bombardier&cooldown.wildfire_bomb.charges_fractional<1
actions.plcleave+=/flanking_strike,if=buff.tip_of_the_spear.stack<2
actions.plcleave+=/explosive_shot,if=(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.coordinated_assault.remains>20|cooldown.coordinated_assault.remains<2
actions.plcleave+=/fury_of_the_eagle,if=buff.tip_of_the_spear.stack>0
actions.plcleave+=/kill_shot,if=buff.sic_em.remains&active_enemies<4
actions.plcleave+=/kill_command,target_if=min:bloodseeker.remains,if=focus+cast_regen<focus.max
actions.plcleave+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0
actions.plcleave+=/raptor_bite,if=buff.merciless_blows.up
actions.plcleave+=/butchery
actions.plcleave+=/kill_shot
actions.plcleave+=/raptor_bite

# PL revisit fote in ST for mdt/ds sim purposes once we lose S4 set. (DPET dif will be dramatically higher) revisit the need for tipping KS once we lose S4 revisit High prio SS refresh if/when Outland Venom is fixed. revisit sending tipless bombardier ES after bombardier fix for both ST and AOE. revisit for AOE AS IT might outperform with either of the AoE PL nodes. - actions.cleave+=/butchery,if=charges_fractional>2.8&cooldown.wildfire_bomb.charges_fractional<1.5 revisit KS priority for AoE with Cull the Herd. standard performance does well, but not better than low prio KS, heavy falloff beyond 3t. ST is currently optimised for KCspam, if the playstyle ends up fixed it is likely better to entirely redo and take the sentactionlist as a baseline. PACK LEADER SINGLE TARGET ACTIONLIST.
actions.plst=kill_command,target_if=min:bloodseeker.remains,if=(buff.relentless_primal_ferocity.up&buff.tip_of_the_spear.stack<1)
actions.plst+=/spearhead,if=cooldown.coordinated_assault.remains
actions.plst+=/raptor_bite,target_if=min:dot.serpent_sting.remains,if=!dot.serpent_sting.ticking&target.time_to_die>12&(!talent.contagious_reagents|active_dot.serpent_sting=0)
actions.plst+=/raptor_bite,target_if=max:dot.serpent_sting.remains,if=talent.contagious_reagents&active_dot.serpent_sting<active_enemies&dot.serpent_sting.remains
actions.plst+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&cooldown.wildfire_bomb.charges_fractional>1.7|cooldown.wildfire_bomb.charges_fractional>1.9|cooldown.coordinated_assault.remains<2*gcd
actions.plst+=/coordinated_assault,if=!talent.bombardier|talent.bombardier&cooldown.wildfire_bomb.charges_fractional<1
actions.plst+=/kill_shot,if=(buff.tip_of_the_spear.stack>0|talent.sic_em)
actions.plst+=/flanking_strike,if=buff.tip_of_the_spear.stack<2
actions.plst+=/explosive_shot,if=(talent.spearhead&(!talent.symbiotic_adrenaline&(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.spearhead.remains>20|cooldown.spearhead.remains<2))|((talent.symbiotic_adrenaline|!talent.spearhead)&(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.coordinated_assault.remains>20|cooldown.coordinated_assault.remains<2)
actions.plst+=/raptor_bite,if=(buff.furious_assault.up&buff.tip_of_the_spear.stack>0)&(!talent.mongoose_bite|buff.mongoose_fury.stack>4)
actions.plst+=/kill_command,target_if=min:bloodseeker.remains
actions.plst+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.in>15)
actions.plst+=/fury_of_the_eagle,interrupt=1,if=(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.in>40)
actions.plst+=/butchery,if=active_enemies>1&(talent.merciless_blows&buff.merciless_blows.down|!talent.merciless_blows)
actions.plst+=/raptor_bite,target_if=min:dot.serpent_sting.remains,if=!talent.contagious_reagents
actions.plst+=/raptor_bite,target_if=max:dot.serpent_sting.remains

# SENTINEL | DEFAULT AOE ACTIONLIST
actions.sentcleave=spearhead,if=cooldown.coordinated_assault.remains
actions.sentcleave+=/kill_command,target_if=min:bloodseeker.remains,if=buff.relentless_primal_ferocity.up&buff.tip_of_the_spear.stack<1
actions.sentcleave+=/explosive_shot,if=buff.bombardier.remains
actions.sentcleave+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&cooldown.wildfire_bomb.charges_fractional>1.7|cooldown.wildfire_bomb.charges_fractional>1.9|cooldown.coordinated_assault.remains<2*gcd
actions.sentcleave+=/coordinated_assault,if=!talent.bombardier|talent.bombardier&cooldown.wildfire_bomb.charges_fractional<1
actions.sentcleave+=/flanking_strike,if=buff.tip_of_the_spear.stack<2
actions.sentcleave+=/explosive_shot,if=(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.coordinated_assault.remains>20|cooldown.coordinated_assault.remains<2
actions.sentcleave+=/fury_of_the_eagle,if=buff.tip_of_the_spear.stack>0
actions.sentcleave+=/kill_shot,if=buff.sic_em.remains&active_enemies<4
actions.sentcleave+=/kill_command,target_if=min:bloodseeker.remains,if=focus+cast_regen<focus.max
actions.sentcleave+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0
actions.sentcleave+=/raptor_bite,if=buff.merciless_blows.up
actions.sentcleave+=/butchery
actions.sentcleave+=/kill_shot
actions.sentcleave+=/raptor_bite

# SENT revisit fote in ST for mdt/ds sim purposes once we lose S4 set. (DPET dif will be dramatically higher) revisit the need for tipping KS once we lose S4. revisit High prio SS refresh if/when Outland Venom is fixed. revisit sending tipless bombardier ES after bombardier fix for both ST and AoE. T31 line currently exists since level 70 characters follow the sent/default actionlist. sentinel is currently nyi. SENTINEL | DEFAULT SINGLE TARGET ACTIONLIST.
actions.sentst=kill_command,target_if=min:bloodseeker.remains,if=(buff.relentless_primal_ferocity.up&buff.tip_of_the_spear.stack<1)
actions.sentst+=/spearhead,if=cooldown.coordinated_assault.remains
actions.sentst+=/raptor_bite,target_if=min:dot.serpent_sting.remains,if=!dot.serpent_sting.ticking&target.time_to_die>12&(!talent.contagious_reagents|active_dot.serpent_sting=0)
actions.sentst+=/raptor_bite,target_if=max:dot.serpent_sting.remains,if=talent.contagious_reagents&active_dot.serpent_sting<active_enemies&dot.serpent_sting.remains
actions.sentst+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&cooldown.wildfire_bomb.charges_fractional>1.7|cooldown.wildfire_bomb.charges_fractional>1.9|cooldown.coordinated_assault.remains<2*gcd
actions.sentst+=/coordinated_assault,if=!talent.bombardier|talent.bombardier&cooldown.wildfire_bomb.charges_fractional<1
actions.sentst+=/fury_of_the_eagle,interrupt=1,if=set_bonus.tier31_2pc
actions.sentst+=/flanking_strike,if=buff.tip_of_the_spear.stack<2
actions.sentst+=/explosive_shot,if=(talent.spearhead&(!talent.symbiotic_adrenaline&(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.spearhead.remains>20|cooldown.spearhead.remains<2))|((talent.symbiotic_adrenaline|!talent.spearhead)&(buff.tip_of_the_spear.stack>0|buff.bombardier.remains)&cooldown.coordinated_assault.remains>20|cooldown.coordinated_assault.remains<2)
actions.sentst+=/kill_shot,if=buff.tip_of_the_spear.stack>0|talent.sic_em
actions.sentst+=/kill_command,target_if=min:bloodseeker.remains,if=focus+cast_regen<focus.max&(!buff.relentless_primal_ferocity.up||(buff.relentless_primal_ferocity.up&buff.tip_of_the_spear.stack<2))
actions.sentst+=/wildfire_bomb,if=buff.tip_of_the_spear.stack>0&(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.in>15)
actions.sentst+=/fury_of_the_eagle,interrupt=1,if=(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.in>40)
actions.sentst+=/butchery,if=active_enemies>1&(talent.merciless_blows&buff.merciless_blows.down|!talent.merciless_blows)
actions.sentst+=/raptor_bite,target_if=min:dot.serpent_sting.remains,if=!talent.contagious_reagents
actions.sentst+=/raptor_bite,target_if=max:dot.serpent_sting.remains

```

# ActionPriorityLists\hunter_marksmanship.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/summon_pet,if=!talent.lone_wolf
actions.precombat+=/snapshot_stats
# Determine the stronger trinket to sync with cooldowns. In descending priority: buff effects > damage effects, longer > shorter cooldowns, longer > shorter cast times. Special case to consider Mirror of Fractured Tomorrows weaker than other buff effects since its power is split between the dmg effect and the buff effect.
actions.precombat+=/variable,name=trinket_1_stronger,value=!trinket.2.has_cooldown|trinket.1.has_use_buff&(!trinket.2.has_use_buff|!trinket.1.is.mirror_of_fractured_tomorrows&(trinket.2.is.mirror_of_fractured_tomorrows|trinket.2.cooldown.duration<trinket.1.cooldown.duration|trinket.2.cast_time<trinket.1.cast_time|trinket.2.cast_time=trinket.1.cast_time&trinket.2.cooldown.duration=trinket.1.cooldown.duration))|!trinket.1.has_use_buff&(!trinket.2.has_use_buff&(trinket.2.cooldown.duration<trinket.1.cooldown.duration|trinket.2.cast_time<trinket.1.cast_time|trinket.2.cast_time=trinket.1.cast_time&trinket.2.cooldown.duration=trinket.1.cooldown.duration))
actions.precombat+=/variable,name=trinket_2_stronger,value=!variable.trinket_1_stronger
actions.precombat+=/salvo,precast_time=10
actions.precombat+=/use_item,name=algethar_puzzle_box
# Precast Aimed Shot on one or two targets unless we could cleave it with Volley on two targets.
actions.precombat+=/aimed_shot,if=active_enemies<3&(!talent.volley|active_enemies<2)
# Precast Steady Shot on two targets if we are saving Aimed Shot to cleave with Volley, otherwise on three or more targets.
actions.precombat+=/steady_shot,if=active_enemies>2|talent.volley&active_enemies=2

# Executed every time the actor is available.
# Determine if it is a good time to use Trueshot. Raid event optimization takes priority so usage is saved for multiple targets as long as it won't delay over half its duration. Otherwise allow for small delays to line up buff effect trinkets, and when using Bullseye, delay the last usage of the fight for max stacks.
actions=variable,name=trueshot_ready,value=cooldown.trueshot.ready&(!raid_event.adds.exists&(!talent.bullseye|fight_remains>cooldown.trueshot.duration_guess+buff.trueshot.duration%2|buff.bullseye.stack=buff.bullseye.max_stack)&(!trinket.1.has_use_buff|trinket.1.cooldown.remains>30|trinket.1.cooldown.ready)&(!trinket.2.has_use_buff|trinket.2.cooldown.remains>30|trinket.2.cooldown.ready)|raid_event.adds.exists&(!raid_event.adds.up&(raid_event.adds.duration+raid_event.adds.in<25|raid_event.adds.in>60)|raid_event.adds.up&raid_event.adds.remains>10)|fight_remains<25)
actions+=/auto_shot
actions+=/call_action_list,name=cds
actions+=/call_action_list,name=trinkets
actions+=/call_action_list,name=st,if=active_enemies<3|!talent.trick_shots
actions+=/call_action_list,name=trickshots,if=active_enemies>2

# Call for Power Infusion when Trueshot is up.
actions.cds=invoke_external_buff,name=power_infusion,if=buff.trueshot.remains>12
actions.cds+=/berserking,if=buff.trueshot.up|fight_remains<13
actions.cds+=/blood_fury,if=buff.trueshot.up|cooldown.trueshot.remains>30|fight_remains<16
actions.cds+=/ancestral_call,if=buff.trueshot.up|cooldown.trueshot.remains>30|fight_remains<16
actions.cds+=/fireblood,if=buff.trueshot.up|cooldown.trueshot.remains>30|fight_remains<9
actions.cds+=/lights_judgment,if=buff.trueshot.down
actions.cds+=/potion,if=buff.trueshot.up&(buff.bloodlust.up|target.health.pct<20)|fight_remains<26
actions.cds+=/salvo,if=active_enemies>2|cooldown.volley.remains<10

actions.st=steady_shot,if=talent.steady_focus&steady_focus_count&buff.steady_focus.remains<8
actions.st+=/kill_shot,if=buff.razor_fragments.up
actions.st+=/rapid_fire,if=talent.surging_shots|action.aimed_shot.full_recharge_time>action.aimed_shot.cast_time+cast_time
actions.st+=/volley,if=buff.salvo.up|variable.trueshot_ready|cooldown.trueshot.remains>45|fight_remains<12
actions.st+=/explosive_shot,if=active_enemies>1
actions.st+=/trueshot,if=variable.trueshot_ready
# Trigger Salvo if Volley isn't being used to trigger it.
actions.st+=/multishot,if=buff.salvo.up&!talent.volley
# Don't overwrite Precise Shots unless Trueshot is active or it can cleave.
actions.st+=/wailing_arrow,if=buff.precise_shots.down|buff.trueshot.up|active_enemies>1
# With Serpentstalker's Trickery target the lowest remaining Serpent Sting. Don't overwrite Precise Shots unless either Trueshot is active or Aimed Shot would cap before its next cast. Overwrite freely if it can cleave.
actions.st+=/aimed_shot,target_if=min:dot.serpent_sting.remains+action.serpent_sting.in_flight_to_target*99,if=buff.precise_shots.down|(buff.trueshot.up|full_recharge_time<gcd+cast_time)|(buff.trick_shots.remains>execute_time&active_enemies>1)
actions.st+=/kill_shot
actions.st+=/explosive_shot
actions.st+=/chimaera_shot,if=buff.precise_shots.up
actions.st+=/arcane_shot,if=buff.precise_shots.up
actions.st+=/barrage,if=talent.rapid_fire_barrage
actions.st+=/arcane_shot,if=focus>cost+action.aimed_shot.cost
actions.st+=/bag_of_tricks,if=buff.trueshot.down
actions.st+=/steady_shot

actions.trickshots=steady_shot,if=talent.steady_focus&steady_focus_count&buff.steady_focus.remains<8
actions.trickshots+=/kill_shot,if=buff.razor_fragments.up
actions.trickshots+=/explosive_shot
actions.trickshots+=/volley
actions.trickshots+=/barrage,if=talent.rapid_fire_barrage
actions.trickshots+=/rapid_fire,if=buff.trick_shots.remains>=execute_time&talent.surging_shots
actions.trickshots+=/wailing_arrow,if=buff.precise_shots.down|buff.trueshot.up
actions.trickshots+=/trueshot,if=variable.trueshot_ready
# For Serpentstalker's Trickery, target the lowest remaining Serpent Sting. Generally only cast if it would cleave with Trick Shots. Don't overwrite Precise Shots unless Trueshot is up or Aimed Shot would cap otherwise.
actions.trickshots+=/aimed_shot,target_if=min:dot.serpent_sting.remains+action.serpent_sting.in_flight_to_target*99,if=(buff.trick_shots.remains>=execute_time&(buff.precise_shots.down|buff.trueshot.up|full_recharge_time<cast_time+gcd))
actions.trickshots+=/rapid_fire,if=buff.trick_shots.remains>=execute_time
actions.trickshots+=/chimaera_shot,if=buff.trick_shots.up&buff.precise_shots.up&focus>cost+action.aimed_shot.cost&active_enemies<4
actions.trickshots+=/multishot,if=buff.trick_shots.down|(buff.precise_shots.up|buff.bulletstorm.stack=10)&focus>cost+action.aimed_shot.cost
actions.trickshots+=/kill_shot,if=focus>cost+action.aimed_shot.cost
actions.trickshots+=/multishot,if=focus>cost+action.aimed_shot.cost
actions.trickshots+=/bag_of_tricks,if=buff.trueshot.down
actions.trickshots+=/steady_shot

# True if effects that are desirable to sync a trinket buff with are ready.
actions.trinkets=variable,name=sync_ready,value=variable.trueshot_ready
# True if effecs that are desirable to sync a trinket buff with are active.
actions.trinkets+=/variable,name=sync_active,value=buff.trueshot.up
# Time until the effects that are desirable to sync a trinket buff with will be ready.
actions.trinkets+=/variable,name=sync_remains,value=cooldown.trueshot.remains_guess
# Uses buff effect trinkets with cooldowns and is willing to delay usage up to half the trinket cooldown if it won't lose a usage in the fight. Fills in downtime with weaker buff effects if they won't also be saved for later cooldowns (happens if it won't delay over half the trinket cooldown and a stronger trinket won't be up in time) or damage effects if they won't inferfere with any buff effect usage. Intended to be slot-agnostic so that any order of the same trinket pair should result in the same usage.
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=trinket.1.has_use_buff&(variable.sync_ready&(variable.trinket_1_stronger|trinket.2.cooldown.remains)|!variable.sync_ready&(variable.trinket_1_stronger&(variable.sync_remains>trinket.1.cooldown.duration%3&fight_remains>trinket.1.cooldown.duration+20|trinket.2.has_use_buff&trinket.2.cooldown.remains>variable.sync_remains-15&trinket.2.cooldown.remains-5<variable.sync_remains&variable.sync_remains+45>fight_remains)|variable.trinket_2_stronger&(trinket.2.cooldown.remains&(trinket.2.cooldown.remains-5<variable.sync_remains&variable.sync_remains>=20|trinket.2.cooldown.remains-5>=variable.sync_remains&(variable.sync_remains>trinket.1.cooldown.duration%3|trinket.1.cooldown.duration<fight_remains&(variable.sync_remains+trinket.1.cooldown.duration>fight_remains)))|trinket.2.cooldown.ready&variable.sync_remains>20&variable.sync_remains<trinket.2.cooldown.duration%3)))|!trinket.1.has_use_buff&(trinket.1.cast_time=0|!variable.sync_active)&(!trinket.2.has_use_buff&(variable.trinket_1_stronger|trinket.2.cooldown.remains)|trinket.2.has_use_buff&(variable.sync_remains>20|trinket.2.cooldown.remains>20))|fight_remains<25&(variable.trinket_1_stronger|trinket.2.cooldown.remains)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=trinket.2.has_use_buff&(variable.sync_ready&(variable.trinket_2_stronger|trinket.1.cooldown.remains)|!variable.sync_ready&(variable.trinket_2_stronger&(variable.sync_remains>trinket.2.cooldown.duration%3&fight_remains>trinket.2.cooldown.duration+20|trinket.1.has_use_buff&trinket.1.cooldown.remains>variable.sync_remains-15&trinket.1.cooldown.remains-5<variable.sync_remains&variable.sync_remains+45>fight_remains)|variable.trinket_1_stronger&(trinket.1.cooldown.remains&(trinket.1.cooldown.remains-5<variable.sync_remains&variable.sync_remains>=20|trinket.1.cooldown.remains-5>=variable.sync_remains&(variable.sync_remains>trinket.2.cooldown.duration%3|trinket.2.cooldown.duration<fight_remains&(variable.sync_remains+trinket.2.cooldown.duration>fight_remains)))|trinket.1.cooldown.ready&variable.sync_remains>20&variable.sync_remains<trinket.1.cooldown.duration%3)))|!trinket.2.has_use_buff&(trinket.2.cast_time=0|!variable.sync_active)&(!trinket.1.has_use_buff&(variable.trinket_2_stronger|trinket.1.cooldown.remains)|trinket.1.has_use_buff&(variable.sync_remains>20|trinket.1.cooldown.remains>20))|fight_remains<25&(variable.trinket_2_stronger|trinket.1.cooldown.remains)

```

# ActionPriorityLists\hunter_beast_mastery.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/summon_pet
actions.precombat+=/snapshot_stats
# Determine the stronger trinket to sync with cooldowns. In descending priority: buff effects > damage effects, longer > shorter cooldowns, longer > shorter cast times. Special case to consider Mirror of Fractured Tomorrows weaker than other buff effects since its power is split between the dmg effect and the buff effect.
actions.precombat+=/variable,name=trinket_1_stronger,value=!trinket.2.has_cooldown|trinket.1.has_use_buff&(!trinket.2.has_use_buff|!trinket.1.is.mirror_of_fractured_tomorrows&(trinket.2.is.mirror_of_fractured_tomorrows|trinket.2.cooldown.duration<trinket.1.cooldown.duration|trinket.2.cast_time<trinket.1.cast_time|trinket.2.cast_time=trinket.1.cast_time&trinket.2.cooldown.duration=trinket.1.cooldown.duration))|!trinket.1.has_use_buff&(!trinket.2.has_use_buff&(trinket.2.cooldown.duration<trinket.1.cooldown.duration|trinket.2.cast_time<trinket.1.cast_time|trinket.2.cast_time=trinket.1.cast_time&trinket.2.cooldown.duration=trinket.1.cooldown.duration))
actions.precombat+=/variable,name=trinket_2_stronger,value=!variable.trinket_1_stronger

# Executed every time the actor is available.
actions=auto_shot
actions+=/call_action_list,name=cds
actions+=/call_action_list,name=trinkets
actions+=/call_action_list,name=st,if=active_enemies<2|!talent.beast_cleave&active_enemies<3
actions+=/call_action_list,name=cleave,if=active_enemies>2|talent.beast_cleave&active_enemies>1

actions.cds=invoke_external_buff,name=power_infusion,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&(buff.bestial_wrath.up|cooldown.bestial_wrath.remains<30)|fight_remains<16
actions.cds+=/berserking,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up|fight_remains<13
actions.cds+=/blood_fury,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up|fight_remains<16
actions.cds+=/ancestral_call,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up|fight_remains<16
actions.cds+=/fireblood,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up|fight_remains<9
actions.cds+=/potion,if=buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up|fight_remains<31

actions.cleave=barbed_shot,target_if=min:dot.barbed_shot.remains,if=pet.main.buff.frenzy.up&pet.main.buff.frenzy.remains<=gcd+0.25|talent.scent_of_blood&cooldown.bestial_wrath.remains<12+gcd|pet.main.buff.frenzy.stack<3&(cooldown.bestial_wrath.ready|cooldown.call_of_the_wild.ready)|full_recharge_time<gcd&cooldown.bestial_wrath.remains
actions.cleave+=/multishot,if=pet.main.buff.beast_cleave.remains<0.25+gcd&(!talent.bloody_frenzy|cooldown.call_of_the_wild.remains)
actions.cleave+=/bestial_wrath
actions.cleave+=/call_of_the_wild
actions.cleave+=/kill_command,if=talent.kill_cleave
actions.cleave+=/explosive_shot
actions.cleave+=/bloodshed
actions.cleave+=/kill_shot,target_if=min:dot.serpent_sting.remains,if=talent.venoms_bite&dot.serpent_sting.remains<gcd&target.time_to_die>10
actions.cleave+=/dire_beast
actions.cleave+=/barbed_shot,target_if=min:dot.barbed_shot.remains,if=buff.call_of_the_wild.up|fight_remains<9|talent.wild_call&charges_fractional>1.2|talent.savagery
actions.cleave+=/kill_command
actions.cleave+=/multishot,if=pet.main.buff.beast_cleave.remains<gcd*2
actions.cleave+=/lights_judgment,if=buff.bestial_wrath.down|target.time_to_die<5
actions.cleave+=/kill_shot
actions.cleave+=/cobra_shot,if=focus.time_to_max<gcd*2
actions.cleave+=/bag_of_tricks,if=buff.bestial_wrath.down|target.time_to_die<5
actions.cleave+=/arcane_torrent,if=(focus+focus.regen+30)<focus.max

actions.st=barbed_shot,target_if=min:dot.barbed_shot.remains,if=pet.main.buff.frenzy.up&pet.main.buff.frenzy.remains<=gcd+0.25|pet.main.buff.frenzy.stack<3&(talent.scent_of_blood&(cooldown.bestial_wrath.ready|cooldown.call_of_the_wild.ready)|!cooldown.bestial_wrath.ready)
actions.st+=/bestial_wrath
actions.st+=/kill_command,if=(full_recharge_time<gcd&talent.alpha_predator)|talent.call_of_the_wild
actions.st+=/dire_beast,if=talent.huntmasters_call&(!buff.bestial_wrath.up&talent.killer_cobra|cooldown.call_of_the_wild.ready)
actions.st+=/kill_shot,target_if=min:dot.serpent_sting.remains,if=talent.venoms_bite&dot.serpent_sting.refreshable
actions.st+=/call_of_the_wild
actions.st+=/bloodshed
actions.st+=/kill_command
actions.st+=/barbed_shot,target_if=min:dot.barbed_shot.remains,if=talent.wild_call&charges_fractional>1.4|buff.call_of_the_wild.up|full_recharge_time<gcd&cooldown.bestial_wrath.remains|talent.scent_of_blood&(cooldown.bestial_wrath.remains<12+gcd)|talent.savagery|fight_remains<9
actions.st+=/cobra_shot,if=buff.bestial_wrath.up&talent.killer_cobra
actions.st+=/dire_beast
actions.st+=/explosive_shot,if=!buff.bestial_wrath.up&talent.killer_cobra|!talent.killer_cobra
actions.st+=/kill_shot,if=buff.hunters_prey.remains<gcd*2&talent.venoms_bite|target.health.pct<20
actions.st+=/lights_judgment,if=buff.bestial_wrath.down|target.time_to_die<5
actions.st+=/cobra_shot
actions.st+=/bag_of_tricks,if=buff.bestial_wrath.down|target.time_to_die<5
actions.st+=/arcane_pulse,if=buff.bestial_wrath.down|target.time_to_die<5
actions.st+=/arcane_torrent,if=(focus+focus.regen+15)<focus.max

# True if effects that are desirable to sync a trinket buff with are ready.
actions.trinkets=variable,name=sync_ready,value=talent.call_of_the_wild&(prev_gcd.1.call_of_the_wild)|!talent.call_of_the_wild&(buff.bestial_wrath.up|cooldown.bestial_wrath.remains_guess<5)
# True if effecs that are desirable to sync a trinket buff with are active.
actions.trinkets+=/variable,name=sync_active,value=talent.call_of_the_wild&buff.call_of_the_wild.up|!talent.call_of_the_wild&buff.bestial_wrath.up
# Time until the effects that are desirable to sync a trinket buff with will be ready.
actions.trinkets+=/variable,name=sync_remains,op=setif,value=cooldown.bestial_wrath.remains_guess,value_else=cooldown.call_of_the_wild.remains,condition=!talent.call_of_the_wild
# Uses buff effect trinkets with cooldowns and is willing to delay usage up to half the trinket cooldown if it won't lose a usage in the fight. Fills in downtime with weaker buff effects if they won't also be saved for later cooldowns (happens if it won't delay over half the trinket cooldown and a stronger trinket won't be up in time) or damage effects if they won't inferfere with any buff effect usage. Intended to be slot-agnostic so that any order of the same trinket pair should result in the same usage.
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=trinket.1.has_use_buff&(variable.sync_ready&(variable.trinket_1_stronger|trinket.2.cooldown.remains)|!variable.sync_ready&(variable.trinket_1_stronger&(variable.sync_remains>trinket.1.cooldown.duration%3&fight_remains>trinket.1.cooldown.duration+20|trinket.2.has_use_buff&trinket.2.cooldown.remains>variable.sync_remains-15&trinket.2.cooldown.remains-5<variable.sync_remains&variable.sync_remains+45>fight_remains)|variable.trinket_2_stronger&(trinket.2.cooldown.remains&(trinket.2.cooldown.remains-5<variable.sync_remains&variable.sync_remains>=20|trinket.2.cooldown.remains-5>=variable.sync_remains&(variable.sync_remains>trinket.1.cooldown.duration%3|trinket.1.cooldown.duration<fight_remains&(variable.sync_remains+trinket.1.cooldown.duration>fight_remains)))|trinket.2.cooldown.ready&variable.sync_remains>20&variable.sync_remains<trinket.2.cooldown.duration%3)))|!trinket.1.has_use_buff&(trinket.1.cast_time=0|!variable.sync_active)&(!trinket.2.has_use_buff&(variable.trinket_1_stronger|trinket.2.cooldown.remains)|trinket.2.has_use_buff&(!variable.sync_active&variable.sync_remains>20|trinket.2.cooldown.remains>20))|fight_remains<25&(variable.trinket_1_stronger|trinket.2.cooldown.remains)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=trinket.2.has_use_buff&(variable.sync_ready&(variable.trinket_2_stronger|trinket.1.cooldown.remains)|!variable.sync_ready&(variable.trinket_2_stronger&(variable.sync_remains>trinket.2.cooldown.duration%3&fight_remains>trinket.2.cooldown.duration+20|trinket.1.has_use_buff&trinket.1.cooldown.remains>variable.sync_remains-15&trinket.1.cooldown.remains-5<variable.sync_remains&variable.sync_remains+45>fight_remains)|variable.trinket_1_stronger&(trinket.1.cooldown.remains&(trinket.1.cooldown.remains-5<variable.sync_remains&variable.sync_remains>=20|trinket.1.cooldown.remains-5>=variable.sync_remains&(variable.sync_remains>trinket.2.cooldown.duration%3|trinket.2.cooldown.duration<fight_remains&(variable.sync_remains+trinket.2.cooldown.duration>fight_remains)))|trinket.1.cooldown.ready&variable.sync_remains>20&variable.sync_remains<trinket.1.cooldown.duration%3)))|!trinket.2.has_use_buff&(trinket.2.cast_time=0|!variable.sync_active)&(!trinket.1.has_use_buff&(variable.trinket_2_stronger|trinket.1.cooldown.remains)|trinket.1.has_use_buff&(!variable.sync_active&variable.sync_remains>20|trinket.1.cooldown.remains>20))|fight_remains<25&(variable.trinket_2_stronger|trinket.1.cooldown.remains)

```

# ActionPriorityLists\druid_guardian.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Guardian APL can be found at https://www.dreamgrove.gg/sims/bear/guardian.txt

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/bear_form

# Executed every time the actor is available.
actions=use_items
actions+=/auto_attack
actions+=/incarnation
actions+=/berserk
actions+=/heart_of_the_wild
actions+=/natures_vigil
actions+=/convoke_the_spirits
actions+=/stampeding_roar
actions+=/growl
actions+=/frenzied_regeneration
actions+=/barkskin
actions+=/survival_instincts
actions+=/pulverize
actions+=/rage_of_the_sleeper
actions+=/lunar_beam
actions+=/bristling_fur
actions+=/ironfur,if=!buff.ironfur.up
actions+=/moonfire,target_if=refreshable
actions+=/maul
actions+=/mangle
actions+=/thrash_bear
actions+=/swipe_bear

```

# ActionPriorityLists\druid_feral.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Feral APL can be found at https://www.dreamgrove.gg/sims/cat/feral.txt

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/cat_form,if=!buff.cat_form.up
actions.precombat+=/prowl,if=!buff.prowl.up
# check if trinket slot contains a stat on use
actions.precombat+=/variable,name=trinket_1_buffs,value=trinket.1.has_buff.agility|trinket.1.has_buff.mastery|trinket.1.has_buff.versatility|trinket.1.has_buff.haste|trinket.1.has_buff.crit
actions.precombat+=/variable,name=trinket_2_buffs,value=trinket.2.has_buff.agility|trinket.2.has_buff.mastery|trinket.2.has_buff.versatility|trinket.2.has_buff.haste|trinket.2.has_buff.crit
# if we are playing 2 minute convoke, we prefer 2 minute on-use over 3 minute on-use even with berserk: heart of the lion
actions.precombat+=/variable,name=trinket_1_sync,op=setif,value=1,value_else=0.5,condition=talent.convoke_the_spirits&!talent.ashamanes_guidance&variable.trinket_1_buffs&(trinket.1.cooldown.duration%%120=0|120%%trinket.1.cooldown.duration=0)
actions.precombat+=/variable,name=trinket_2_sync,op=setif,value=1,value_else=0.5,condition=talent.convoke_the_spirits&!talent.ashamanes_guidance&variable.trinket_2_buffs&(trinket.1.cooldown.duration%%120=0|120%%trinket.1.cooldown.duration=0)
# if we aren't playing 2 minute convoke, then we can sync 3 minute cds with berserk sans hotl
actions.precombat+=/variable,name=trinket_1_sync,op=setif,value=1,value_else=0.5,condition=!(talent.convoke_the_spirits&!talent.ashamanes_guidance)&variable.trinket_1_buffs&(trinket.1.cooldown.duration%%cooldown.bs_inc.duration=0|cooldown.bs_inc.duration%%trinket.1.cooldown.duration=0|trinket.1.cooldown.duration%%cooldown.convoke_the_spirits.duration=0|cooldown.convoke_the_spirits.duration%%trinket.1.cooldown.duration=0)
actions.precombat+=/variable,name=trinket_2_sync,op=setif,value=1,value_else=0.5,condition=!(talent.convoke_the_spirits&!talent.ashamanes_guidance)&variable.trinket_2_buffs&(trinket.2.cooldown.duration%%cooldown.bs_inc.duration=0|cooldown.bs_inc.duration%%trinket.2.cooldown.duration=0|trinket.2.cooldown.duration%%cooldown.convoke_the_spirits.duration=0|cooldown.convoke_the_spirits.duration%%trinket.2.cooldown.duration=0)
# prioritize trinkets that line-up with cds -> main-stat on uses -> longer cd trinkets -> shorter duration trinkets
actions.precombat+=/variable,name=trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_1_buffs&variable.trinket_2_buffs|variable.trinket_2_buffs&((trinket.2.cooldown.duration%trinket.2.proc.any_dps.duration)*(1.5+trinket.2.has_buff.agility)*(1.2+trinket.2.has_buff.mastery)*(variable.trinket_2_sync))>((trinket.1.cooldown.duration%trinket.1.proc.any_dps.duration)*(1.5+trinket.1.has_buff.agility)*(1.2+trinket.1.has_buff.mastery)*(variable.trinket_1_sync))

# Executed every time the actor is available.
actions=prowl,if=buff.bs_inc.down&!buff.prowl.up
actions+=/cat_form,if=!buff.cat_form.up&!talent.fluid_form
# Line up <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> with Berserk.
actions+=/invoke_external_buff,name=power_infusion,if=buff.bs_inc.up|!talent.berserk_heart_of_the_lion
actions+=/call_action_list,name=variable
actions+=/auto_attack,if=!buff.prowl.up|!buff.shadowmeld.up
actions+=/tigers_fury,if=energy.deficit>35|combo_points=5
actions+=/rake,target_if=max:refreshable+persistent_multiplier>dot.rake.pmultiplier,if=buff.shadowmeld.up|buff.prowl.up
actions+=/natures_vigil,if=spell_targets.swipe_cat>0
actions+=/renewal,if=spell_targets.swipe_cat>0
actions+=/ferocious_bite,if=buff.apex_predators_craving.up&!(variable.need_bt&active_bt_triggers=2)
actions+=/adaptive_swarm,target_if=(!dot.adaptive_swarm_damage.ticking|dot.adaptive_swarm_damage.remains<2)&dot.adaptive_swarm_damage.stack<3&!action.adaptive_swarm_damage.in_flight&!action.adaptive_swarm.in_flight&target.time_to_die>5,if=buff.cat_form.up&!talent.unbridled_swarm.enabled|spell_targets.swipe_cat=1
actions+=/adaptive_swarm,target_if=max:(1+dot.adaptive_swarm_damage.stack)*dot.adaptive_swarm_damage.stack<3*time_to_die,if=buff.cat_form.up&dot.adaptive_swarm_damage.stack<3&talent.unbridled_swarm.enabled&spell_targets.swipe_cat>1
actions+=/call_action_list,name=cooldown,if=dot.rip.ticking
actions+=/call_action_list,name=berserk,if=buff.bs_inc.up
actions+=/call_action_list,name=finisher,if=combo_points=5
actions+=/call_action_list,name=builder,if=spell_targets.swipe_cat=1&combo_points<5&(variable.time_to_pool<=0|!variable.need_bt|variable.proccing_bt)
actions+=/call_action_list,name=aoe_builder,if=spell_targets.swipe_cat>=2&combo_points<5&(variable.time_to_pool<=0|!variable.need_bt|variable.proccing_bt)
actions+=/regrowth,if=buff.predatory_swiftness.up&variable.regrowth

# this variable tracks whether or not we've started our bt sequence
actions.aoe_builder=variable,name=proccing_bt,op=set,value=variable.need_bt
actions.aoe_builder+=/rake,target_if=!dot.rake.ticking,if=buff.sudden_ambush.up&!(variable.need_bt&buff.bt_rake.up)
actions.aoe_builder+=/brutal_slash,target_if=max:time_to_die,if=!(variable.need_bt&buff.bt_swipe.up)&(cooldown.brutal_slash.full_recharge_time<4|time_to_die<4|raid_event.adds.remains<4)
actions.aoe_builder+=/thrash_cat,if=refreshable&!talent.thrashing_claws
actions.aoe_builder+=/prowl,target_if=dot.rake.refreshable|dot.rake.pmultiplier<1.4,if=!(buff.bt_rake.up&active_bt_triggers=2)&action.rake.ready&gcd.remains=0&!buff.sudden_ambush.up
actions.aoe_builder+=/shadowmeld,target_if=dot.rake.refreshable|dot.rake.pmultiplier<1.4,if=!(buff.bt_rake.up&active_bt_triggers=2)&action.rake.ready&!buff.sudden_ambush.up&!buff.prowl.up
# maximize rake uptime while avoiding rake-downgrades
actions.aoe_builder+=/rake,target_if=min:dot.rake.remains-20*(dot.rake.pmultiplier<persistent_multiplier),if=refreshable&!(buff.bt_rake.up&active_bt_triggers=2)
actions.aoe_builder+=/brutal_slash,if=!(buff.bt_swipe.up&active_bt_triggers=2)
actions.aoe_builder+=/moonfire_cat,target_if=max:(3*refreshable)+dot.adaptive_swarm_damage.ticking,if=refreshable&(spell_targets.swipe_cat<4|talent.brutal_slash)&!(buff.bt_moonfire.up&active_bt_triggers=2)
actions.aoe_builder+=/swipe_cat,if=!(buff.bt_swipe.up&active_bt_triggers=2)
actions.aoe_builder+=/moonfire_cat,target_if=max:(3*refreshable)+dot.adaptive_swarm_damage.ticking,if=refreshable&!(buff.bt_moonfire.up&active_bt_triggers=2)
actions.aoe_builder+=/rake,target_if=min:dot.rake.remains-20*(dot.rake.pmultiplier<persistent_multiplier),if=refreshable&!(buff.bt_rake.up&active_bt_triggers=2)
# fill with shred if sudden ambush is not up. If easy swipe is enabled, skip this line. Thrashing instead is net-neutral up to at least 10t, but we prefer shred for priority damage.
actions.aoe_builder+=/shred,if=!(buff.bt_shred.up&active_bt_triggers=2)&!variable.easy_swipe&!buff.sudden_ambush.up
actions.aoe_builder+=/thrash_cat,if=!(buff.bt_thrash.up&active_bt_triggers=2)&!talent.thrashing_claws
# fallback bloodtalons actions below this point
actions.aoe_builder+=/moonfire_cat,target_if=max:dot.moonfire.ticks_gained_on_refresh,if=variable.need_bt&buff.bt_moonfire.down
actions.aoe_builder+=/shred,if=variable.need_bt&buff.bt_shred.down&!variable.easy_swipe
actions.aoe_builder+=/rake,target_if=dot.rake.pmultiplier<1.6,if=variable.need_bt&buff.bt_rake.down

actions.berserk=call_action_list,name=finisher,if=combo_points=5
actions.berserk+=/run_action_list,name=aoe_builder,if=spell_targets.swipe_cat>=2
actions.berserk+=/prowl,if=!(buff.bt_rake.up&active_bt_triggers=2)&action.rake.ready&gcd.remains=0&!buff.sudden_ambush.up&(dot.rake.refreshable|dot.rake.pmultiplier<1.4)&!buff.shadowmeld.up
actions.berserk+=/shadowmeld,if=!(buff.bt_rake.up&active_bt_triggers=2)&action.rake.ready&!buff.sudden_ambush.up&(dot.rake.refreshable|dot.rake.pmultiplier<1.4)&!buff.prowl.up
# rake if bt doesnt need proc and rake can be upgraded. Fish for sudden ambush procs unless rake will fall off otherwise.
actions.berserk+=/rake,if=!(buff.bt_rake.up&active_bt_triggers=2)&(dot.rake.remains<3|buff.sudden_ambush.up&persistent_multiplier>dot.rake.pmultiplier)
actions.berserk+=/moonfire_cat,if=refreshable
actions.berserk+=/thrash_cat,if=!talent.thrashing_claws&refreshable
# proc bt when an opportunity arises
actions.berserk+=/shred,if=active_bt_triggers=2&buff.bt_shred.down
actions.berserk+=/brutal_slash,if=active_bt_triggers=2&buff.bt_swipe.down
# alternate brs and shred to create bt opportunities
actions.berserk+=/brutal_slash,if=cooldown.brutal_slash.charges>1&buff.bt_swipe.down
actions.berserk+=/shred,if=buff.bt_shred.down
actions.berserk+=/brutal_slash,if=cooldown.brutal_slash.charges>1
actions.berserk+=/shred

# this variable tracks whether or not we've started our bt sequence
actions.builder=variable,name=proccing_bt,op=set,value=variable.need_bt
actions.builder+=/shadowmeld,if=gcd=0&energy>=35&!buff.sudden_ambush.up&(dot.rake.refreshable|dot.rake.pmultiplier<1.4)*!(variable.need_bt&buff.bt_rake.up)&buff.tigers_fury.up
# upgrade to stealth rakes, otherwise refresh in pandemic. Delay rake as long as possible if it would downgrade
actions.builder+=/rake,if=((refreshable&persistent_multiplier>=dot.rake.pmultiplier|dot.rake.remains<3)|buff.sudden_ambush.up&persistent_multiplier>dot.rake.pmultiplier)&!(variable.need_bt&buff.bt_rake.up)
actions.builder+=/brutal_slash,if=cooldown.brutal_slash.full_recharge_time<4&!(variable.need_bt&buff.bt_swipe.up)
actions.builder+=/thrash_cat,if=refreshable
actions.builder+=/moonfire_cat,if=refreshable&cooldown.convoke_the_spirits.remains>5
actions.builder+=/shred,if=buff.clearcasting.react
actions.builder+=/brutal_slash,if=!(variable.need_bt&buff.bt_swipe.up)
actions.builder+=/swipe_cat,if=talent.wild_slashes&!(variable.need_bt&buff.bt_swipe.up)
actions.builder+=/shred,if=!(variable.need_bt&buff.bt_shred.up)
actions.builder+=/swipe_cat,if=variable.need_bt&buff.bt_swipe.down
# clip rake for bt if it wont downgrade its snapshot
actions.builder+=/rake,if=variable.need_bt&buff.bt_rake.down&persistent_multiplier>=dot.rake.pmultiplier
actions.builder+=/moonfire_cat,if=variable.need_bt&buff.bt_moonfire.down
actions.builder+=/thrash_cat,if=variable.need_bt&buff.bt_thrash.down

actions.cooldown=incarnation
actions.cooldown+=/berserk
actions.cooldown+=/berserking,if=buff.bs_inc.up|cooldown.bs_inc.remains>50
actions.cooldown+=/potion,if=buff.bs_inc.up|fight_remains<32|(!variable.lastZerk&variable.lastConvoke&cooldown.convoke_the_spirits.remains<10)
actions.cooldown+=/feral_frenzy,if=combo_points<=1|buff.bs_inc.up&combo_points<=2
# stat on-use trinkets, prefers trinket with higher priority. reads like this: berserk is up OR if tigers fury up & convoke is either ready, wont be for the next tf, or the other trinket will be ready in time for convoke. If we dont have convoke, then we use if berserk wont be up for next tf or other trinket will be up for berserk.
actions.cooldown+=/use_item,slot=trinket1,if=(buff.bs_inc.up|((buff.tigers_fury.up&cooldown.tigers_fury.remains>20)&(cooldown.convoke_the_spirits.remains<4|cooldown.convoke_the_spirits.remains>45|cooldown.convoke_the_spirits.remains-trinket.2.cooldown.remains>0|!talent.convoke_the_spirits&(cooldown.bs_inc.remains>40|cooldown.bs_inc.remains-trinket.2.cooldown.remains>0))))&(!trinket.2.has_cooldown|trinket.2.cooldown.remains|variable.trinket_priority=1)|trinket.1.proc.any_dps.duration>=fight_remains
actions.cooldown+=/use_item,slot=trinket2,if=(buff.bs_inc.up|((buff.tigers_fury.up&cooldown.tigers_fury.remains>20)&(cooldown.convoke_the_spirits.remains<4|cooldown.convoke_the_spirits.remains>45|cooldown.convoke_the_spirits.remains-trinket.1.cooldown.remains>0|!talent.convoke_the_spirits&(cooldown.bs_inc.remains>40|cooldown.bs_inc.remains-trinket.1.cooldown.remains>0))))&(!trinket.1.has_cooldown|trinket.1.cooldown.remains|variable.trinket_priority=2)|trinket.2.proc.any_dps.duration>=fight_remains
# non-stat on use trinkets get used on cooldown, so long as it wont interfere with a stat on-use trinket
actions.cooldown+=/use_item,slot=trinket1,if=!variable.trinket_1_buffs&(trinket.2.cooldown.remains>20|!variable.trinket_2_buffs|trinket.2.cooldown.remains&cooldown.tigers_fury.remains>20)
actions.cooldown+=/use_item,slot=trinket2,if=!variable.trinket_2_buffs&(trinket.1.cooldown.remains>20|!variable.trinket_1_buffs|trinket.1.cooldown.remains&cooldown.tigers_fury.remains>20)
actions.cooldown+=/convoke_the_spirits,if=fight_remains<5|(buff.tigers_fury.up&(combo_points<=2|buff.bs_inc.up&combo_points<=3)&(target.time_to_die>5-talent.ashamanes_guidance.enabled|target.time_to_die=fight_remains))

# ravage prio over pw if pw won't upgrade, pw prio over regular bite (with DOTC)
actions.finisher=primal_wrath,if=spell_targets.primal_wrath>1&((dot.primal_wrath.remains<6.5&!buff.bs_inc.up|dot.primal_wrath.refreshable)|spell_targets.primal_wrath>3&!talent.rampant_ferocity.enabled|dot.primal_wrath.pmultiplier<persistent_multiplier)
# rip if single target or pw isnt up. Rip with bloodtalons if talented. If tigers fury will be up before rip falls off, then delay refresh
actions.finisher+=/rip,target_if=refreshable,if=(!talent.primal_wrath|spell_targets=1)&(buff.bloodtalons.up|!talent.bloodtalons)&(buff.tigers_fury.up|dot.rip.remains<cooldown.tigers_fury.remains)
actions.finisher+=/pool_resource,for_next=1
actions.finisher+=/ferocious_bite,max_energy=1,target_if=max:target.time_to_die,if=!buff.bs_inc.up|!talent.soul_of_the_forest.enabled
actions.finisher+=/ferocious_bite,target_if=max:target.time_to_die

# most expensive bt cycle is Shred + Thrash + Rake, 40+40+35 for 115 energy. During incarn it is 32+32+28 for 92energy
actions.variable=variable,name=effective_energy,op=set,value=energy+(40*buff.clearcasting.stack)+(3*energy.regen)+(50*cooldown.tigers_fury.remains<3.5)
# estimated time until we have enough energy to proc bloodtalons.
actions.variable+=/variable,name=time_to_pool,op=set,value=((115-variable.effective_energy-(23*buff.incarnation.up))%energy.regen)
# try to proc bt if we have 1 or 0 stacks of bloodtalons
actions.variable+=/variable,name=need_bt,value=talent.bloodtalons&buff.bloodtalons.stack<=1
# checks if theres exactly 1 convoke remaining in sim
actions.variable+=/variable,name=lastConvoke,value=(cooldown.convoke_the_spirits.remains+cooldown.convoke_the_spirits.duration)>remains&cooldown.convoke_the_spirits.remains<remains
# checks if theres exactly 1 berserk cast remaining in sim                 : at least 5s spare for now, TODO: check #s
actions.variable+=/variable,name=lastZerk,value=(cooldown.bs_inc.remains+cooldown.bs_inc.duration+5)>remains&cooldown.convoke_the_spirits.remains<remains
# 300-(time+318)%%300 roughly gives us potion cd remaining, pot cd=300, in other words this is the same cd_pot.remains+cd_pot.duration+15>fight_remains&cd_pot.remains+15<fight_remains
actions.variable+=/variable,name=lastPotion,value=(300-((time+300)%%300)+300+15)>remains&300-((time+300)%%300)+15<remains
# optional variable that alternates bite/pw during berserk regardless of talent setup. Off by default
actions.variable+=/variable,name=zerk_biteweave,op=reset
# optional variable that sends regrowth and renewal casts. Turned off by default
actions.variable+=/variable,name=regrowth,op=reset
# optional variable that forgoes shredding in AoE. Turned off by default
actions.variable+=/variable,name=easy_swipe,op=reset

```

# ActionPriorityLists\druid_balance.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Balance APL can be found at https://www.dreamgrove.gg/sims/owl/balance.txt

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/moonkin_form
actions.precombat+=/wrath
actions.precombat+=/wrath
actions.precombat+=/starfire,if=!talent.stellar_flare
actions.precombat+=/stellar_flare

# Executed every time the actor is available.
# Executed every time the actor is available.
actions=use_items
actions+=/auto_attack
actions+=/moonfire,target_if=refreshable
actions+=/sunfire,target_if=refreshable
actions+=/stellar_flare,target_if=refreshable
actions+=/force_of_nature
actions+=/fury_of_elune
actions+=/incarnation
actions+=/celestial_alignment
actions+=/warrior_of_elune,if=!talent.lunar_calling&buff.eclipse_solar.remains<7|talent.lunar_calling
actions+=/starfire,if=(!talent.lunar_calling&spell_targets.starfire=1)&(buff.eclipse_solar.up&buff.eclipse_solar.remains<action.starfire.cast_time|eclipse.in_none)
actions+=/wrath,if=(talent.lunar_calling|spell_targets.starfire>1)&(buff.eclipse_lunar.up&(buff.eclipse_lunar.remains<action.wrath.cast_time)|eclipse.in_none)
actions+=/starfall,if=buff.starweavers_warp.up
actions+=/starsurge,if=spell_targets.starfall<2
actions+=/starfall,if=spell_targets.starfall>1
actions+=/convoke_the_spirits
actions+=/new_moon
actions+=/half_moon
actions+=/full_moon
actions+=/warrior_of_elune
actions+=/wild_mushroom
actions+=/starfire,if=talent.lunar_calling|buff.eclipse_lunar.up&spell_targets.starfire>1
actions+=/wrath

```

# ActionPriorityLists\demonhunter_vengeance.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/snapshot_stats
actions.precombat+=/variable,name=single_target,value=spell_targets.spirit_bomb=1
actions.precombat+=/variable,name=small_aoe,value=spell_targets.spirit_bomb>=2&spell_targets.spirit_bomb<=5
actions.precombat+=/variable,name=big_aoe,value=spell_targets.spirit_bomb>=6
actions.precombat+=/arcane_torrent
actions.precombat+=/sigil_of_flame,if=hero_tree.aldrachi_reaver|(hero_tree.felscarred&talent.student_of_suffering)
actions.precombat+=/immolation_aura

# Executed every time the actor is available.
actions=variable,name=num_spawnable_souls,op=reset,default=0
actions+=/variable,name=num_spawnable_souls,op=max,value=2,if=talent.fracture&cooldown.fracture.charges_fractional>=1&!buff.metamorphosis.up
actions+=/variable,name=num_spawnable_souls,op=max,value=3,if=talent.fracture&cooldown.fracture.charges_fractional>=1&buff.metamorphosis.up
actions+=/variable,name=num_spawnable_souls,op=max,value=1,if=talent.soul_sigils&cooldown.sigil_of_flame.up
actions+=/variable,name=num_spawnable_souls,op=add,value=1,if=talent.soul_carver&(cooldown.soul_carver.remains>(cooldown.soul_carver.duration-3))
actions+=/auto_attack
actions+=/retarget_auto_attack,line_cd=1,target_if=min:debuff.reavers_mark.remains,if=hero_tree.aldrachi_reaver
actions+=/disrupt,if=target.debuff.casting.react
actions+=/infernal_strike,use_off_gcd=1
actions+=/demon_spikes,use_off_gcd=1,if=!buff.demon_spikes.up&!cooldown.pause_action.remains
actions+=/run_action_list,name=ar,if=hero_tree.aldrachi_reaver
actions+=/run_action_list,name=fs,if=hero_tree.felscarred

actions.ar=variable,name=spb_threshold,op=setif,condition=talent.fiery_demise&dot.fiery_brand.ticking,value=(variable.single_target*5)+(variable.small_aoe*5)+(variable.big_aoe*4),value_else=(variable.single_target*5)+(variable.small_aoe*5)+(variable.big_aoe*4)
actions.ar+=/variable,name=can_spb,value=soul_fragments>=variable.spb_threshold
actions.ar+=/variable,name=can_spb_soon,value=soul_fragments.total>=variable.spb_threshold
actions.ar+=/variable,name=can_spb_one_gcd,value=(soul_fragments.total+variable.num_spawnable_souls)>=variable.spb_threshold
actions.ar+=/variable,name=dont_soul_cleave,value=variable.can_spb|variable.can_spb_soon|variable.can_spb_one_gcd|prev_gcd.1.fracture
actions.ar+=/variable,name=rg_enhance_cleave,op=setif,condition=variable.big_aoe|fight_remains<10,value=1,value_else=0
actions.ar+=/variable,name=cooldown_sync,value=(debuff.reavers_mark.up&buff.thrill_of_the_fight_damage.up)|fight_remains<20
actions.ar+=/potion,use_off_gcd=1,if=variable.cooldown_sync
actions.ar+=/use_items,use_off_gcd=1,if=variable.cooldown_sync
actions.ar+=/call_action_list,name=externals,if=variable.cooldown_sync
actions.ar+=/run_action_list,name=rg_active,if=buff.glaive_flurry.up|buff.rending_strike.up
actions.ar+=/call_action_list,name=ar_execute,if=fight_remains<20
actions.ar+=/metamorphosis,use_off_gcd=1,if=!buff.metamorphosis.up&!(cooldown.the_hunt.up|buff.reavers_glaive.up)
actions.ar+=/vengeful_retreat,use_off_gcd=1,if=talent.unhindered_assault&!cooldown.felblade.up&(((talent.spirit_bomb&(fury<40&(variable.can_spb|variable.can_spb_soon)))|(talent.spirit_bomb&(cooldown.sigil_of_spite.up|cooldown.soul_carver.up)&cooldown.fel_devastation.up&fury<50))|fury<30)
actions.ar+=/immolation_aura
actions.ar+=/sigil_of_flame,if=talent.ascending_flame|(!talent.ascending_flame&!prev_gcd.1.sigil_of_flame&(dot.sigil_of_flame.remains<(1+talent.quickened_sigils)))
actions.ar+=/soul_cleave,if=(debuff.reavers_mark.remains<=(gcd.remains+execute_time+(gcd.max*2)))&(buff.art_of_the_glaive.stack+soul_fragments>=30&buff.art_of_the_glaive.stack>=28)&(fury<40|!variable.can_spb)
actions.ar+=/spirit_bomb,if=(debuff.reavers_mark.remains<=(gcd.remains+execute_time+(gcd.max*2)))&(buff.art_of_the_glaive.stack+soul_fragments>=30)
actions.ar+=/bulk_extraction,if=(debuff.reavers_mark.remains<=(gcd.remains+execute_time+(gcd.max*2)))&(buff.art_of_the_glaive.stack+(spell_targets>?5)>=30)
actions.ar+=/reavers_glaive,if=(buff.art_of_the_glaive.stack+soul_fragments>=30)|(debuff.reavers_mark.remains<=(gcd.remains+execute_time+(gcd.max*4)))|cooldown.the_hunt.remains<(gcd.remains+execute_time+(gcd.max*4))|variable.rg_enhance_cleave
actions.ar+=/the_hunt,if=!buff.reavers_glaive.up
actions.ar+=/fiery_brand,if=!talent.fiery_demise|(talent.fiery_demise&((talent.down_in_flames&charges>=max_charges)|(active_dot.fiery_brand=0)))
actions.ar+=/fel_devastation,if=talent.spirit_bomb&!variable.can_spb&(variable.can_spb_soon|soul_fragments.inactive>=2)
actions.ar+=/spirit_bomb,if=variable.can_spb
actions.ar+=/fracture,if=talent.spirit_bomb&((fury<40&(!cooldown.felblade.up&(!talent.unhindered_assault|!cooldown.vengeful_retreat.up)))|(fury<40&variable.can_spb_one_gcd))
actions.ar+=/soul_carver,if=!talent.spirit_bomb|(((soul_fragments.total+3)<=6)&fury>=15&!prev_gcd.1.sigil_of_spite)
actions.ar+=/sigil_of_spite,if=!talent.spirit_bomb|((variable.can_spb&fury>=40)|variable.can_spb_soon|soul_fragments<=1)
actions.ar+=/fel_devastation,if=!variable.single_target|buff.thrill_of_the_fight_damage.up
actions.ar+=/bulk_extraction,if=spell_targets>=5
actions.ar+=/felblade,if=(((talent.spirit_bomb&(fury<40&(variable.can_spb|variable.can_spb_soon)))|(talent.spirit_bomb&(cooldown.sigil_of_spite.up|cooldown.soul_carver.up)&cooldown.fel_devastation.up&fury<50))|fury<30)
actions.ar+=/soul_cleave,if=fury.deficit<=25|(!talent.spirit_bomb|!variable.dont_soul_cleave)
actions.ar+=/fracture
actions.ar+=/shear
actions.ar+=/felblade
actions.ar+=/throw_glaive

actions.ar_execute=metamorphosis,use_off_gcd=1
actions.ar_execute+=/reavers_glaive
actions.ar_execute+=/the_hunt,if=!buff.reavers_glaive.up
actions.ar_execute+=/bulk_extraction,if=spell_targets>=3&buff.art_of_the_glaive.stack>=20
actions.ar_execute+=/sigil_of_flame
actions.ar_execute+=/fiery_brand
actions.ar_execute+=/sigil_of_spite
actions.ar_execute+=/soul_carver
actions.ar_execute+=/fel_devastation

actions.externals=invoke_external_buff,name=symbol_of_hope
actions.externals+=/invoke_external_buff,name=power_infusion

actions.fel_dev=spirit_burst,if=talent.spirit_bomb&(variable.can_spburst|(buff.metamorphosis.remains<(gcd.remains+execute_time+1)&buff.demonsurge_spirit_burst.up))
actions.fel_dev+=/soul_sunder,if=buff.demonsurge_soul_sunder.up|!variable.dont_soul_cleave|(buff.metamorphosis.remains<(gcd.remains+execute_time+1)&buff.demonsurge_soul_sunder.up)
actions.fel_dev+=/sigil_of_spite,if=soul_fragments.total<=2&buff.demonsurge_spirit_burst.up
actions.fel_dev+=/soul_carver,if=soul_fragments.total<=2&!prev_gcd.1.sigil_of_spite&buff.demonsurge_spirit_burst.up
actions.fel_dev+=/immolation_aura
actions.fel_dev+=/sigil_of_flame,if=!variable.hold_sof
actions.fel_dev+=/felblade
actions.fel_dev+=/fracture

actions.fel_dev_prep=fiery_brand,if=talent.fiery_demise&((talent.darkglare_boon&fury>=70)|(!talent.darkglare_boon&fury>=100))&(variable.can_spburst|variable.can_spburst_soon)&active_dot.fiery_brand=0&(cooldown.metamorphosis.up|cooldown.metamorphosis.remains<(gcd.remains+execute_time+action.fel_devastation.execute_time+(gcd.max*2)))
actions.fel_dev_prep+=/fel_devastation,if=((talent.darkglare_boon&fury>=70)|(!talent.darkglare_boon&fury>=100))&(variable.can_spburst|variable.can_spburst_soon)
actions.fel_dev_prep+=/sigil_of_spite,if=!(variable.can_spburst|variable.can_spburst_soon)&soul_fragments.total<=2&((talent.darkglare_boon&fury>=70)|(!talent.darkglare_boon&fury>=100))
actions.fel_dev_prep+=/felblade,if=!((talent.darkglare_boon&fury>=70)|(!talent.darkglare_boon&fury>=100))
actions.fel_dev_prep+=/fracture,if=!(variable.can_spburst|variable.can_spburst_soon)|!((talent.darkglare_boon&fury>=70)|(!talent.darkglare_boon&fury>=100))
actions.fel_dev_prep+=/felblade
actions.fel_dev_prep+=/fracture

actions.fs=variable,name=spbomb_threshold,op=setif,condition=talent.fiery_demise&dot.fiery_brand.ticking,value=(variable.single_target*5)+(variable.small_aoe*4)+(variable.big_aoe*3),value_else=(variable.single_target*5)+(variable.small_aoe*4)+(variable.big_aoe*4)
actions.fs+=/variable,name=can_spbomb,value=soul_fragments>=variable.spbomb_threshold
actions.fs+=/variable,name=can_spbomb_soon,value=soul_fragments.total>=variable.spbomb_threshold
actions.fs+=/variable,name=can_spbomb_one_gcd,value=(soul_fragments.total+variable.num_spawnable_souls)>=variable.spbomb_threshold
actions.fs+=/variable,name=spburst_threshold,op=setif,condition=talent.fiery_demise&dot.fiery_brand.ticking,value=(variable.single_target*4)+(variable.small_aoe*4)+(variable.big_aoe*3),value_else=(variable.single_target*5)+(variable.small_aoe*4)+(variable.big_aoe*3)
actions.fs+=/variable,name=can_spburst,value=soul_fragments>=variable.spburst_threshold
actions.fs+=/variable,name=can_spburst_soon,value=soul_fragments.total>=variable.spburst_threshold
actions.fs+=/variable,name=can_spburst_one_gcd,value=(soul_fragments.total+variable.num_spawnable_souls)>=variable.spburst_threshold
actions.fs+=/variable,name=dont_soul_cleave,op=setif,condition=buff.metamorphosis.up&buff.demonsurge_hardcast.up,value=((cooldown.fel_desolation.remains<=gcd.remains+execute_time)&fury<80)|(variable.can_spburst|variable.can_spburst_soon)|(prev_gcd.1.sigil_of_spite|prev_gcd.1.soul_carver),value_else=((cooldown.fel_devastation.remains<=gcd.remains+execute_time)&fury<80)|(variable.can_spbomb|variable.can_spbomb_soon)|(buff.metamorphosis.up&!buff.demonsurge_hardcast.up&buff.demonsurge_spirit_burst.up)|(prev_gcd.1.sigil_of_spite|prev_gcd.1.soul_carver)
actions.fs+=/variable,name=fiery_brand_back_before_meta,op=setif,condition=talent.down_in_flames,value=charges>=max_charges|(charges_fractional>=1&cooldown.fiery_brand.full_recharge_time<=gcd.remains+execute_time)|(charges_fractional>=1&((max_charges-(charges_fractional-1))*cooldown.fiery_brand.duration)<=cooldown.metamorphosis.remains),value_else=cooldown.fiery_brand.duration<=cooldown.metamorphosis.remains
actions.fs+=/variable,name=hold_sof,op=setif,condition=talent.student_of_suffering,value=(buff.student_of_suffering.remains>(1+talent.quickened_sigils))|(!talent.ascending_flame&(dot.sigil_of_flame.remains>(1+talent.quickened_sigils)))|prev_gcd.1.sigil_of_flame|(talent.illuminated_sigils&charges=1&time<(2-talent.quickened_sigils.rank))|cooldown.metamorphosis.up,value_else=cooldown.metamorphosis.up|(cooldown.sigil_of_flame.max_charges>1&talent.ascending_flame&((cooldown.sigil_of_flame.max_charges-(cooldown.sigil_of_flame.charges_fractional-1))*cooldown.sigil_of_flame.duration)>cooldown.metamorphosis.remains)|((prev_gcd.1.sigil_of_flame|dot.sigil_of_flame.remains>(1+talent.quickened_sigils)))
actions.fs+=/cancel_buff,name=metamorphosis,if=(!buff.demonsurge_soul_sunder.up&!buff.demonsurge_spirit_burst.up&!buff.demonsurge_fel_desolation.up&!buff.demonsurge_consuming_fire.up&!buff.demonsurge_sigil_of_doom.up&cooldown.sigil_of_doom.charges<1)&(cooldown.fel_devastation.remains<(gcd.max*2)|cooldown.metamorphosis.remains<(gcd.max*2))
actions.fs+=/immolation_aura,if=!(prev_gcd.1.sigil_of_flame&cooldown.metamorphosis.up)
actions.fs+=/sigil_of_flame,if=!variable.hold_sof
actions.fs+=/fiery_brand,if=!talent.fiery_demise|talent.fiery_demise&((talent.down_in_flames&charges>=max_charges)|(active_dot.fiery_brand=0&variable.fiery_brand_back_before_meta))
actions.fs+=/use_items,use_off_gcd=1,if=!buff.metamorphosis.up
actions.fs+=/call_action_list,name=fs_execute,if=fight_remains<20
actions.fs+=/run_action_list,name=fel_dev,if=buff.metamorphosis.up&!buff.demonsurge_hardcast.up&(buff.demonsurge_soul_sunder.up|buff.demonsurge_spirit_burst.up)
actions.fs+=/call_action_list,name=metamorphosis,if=buff.metamorphosis.up&buff.demonsurge_hardcast.up
actions.fs+=/call_action_list,name=fel_dev_prep,if=!buff.demonsurge_hardcast.up&(cooldown.fel_devastation.up|(cooldown.fel_devastation.remains<=(gcd.max*2)))
actions.fs+=/call_action_list,name=meta_prep,if=(cooldown.metamorphosis.up|cooldown.metamorphosis.remains<=(gcd.max*3))&!cooldown.fel_devastation.up&!buff.demonsurge_soul_sunder.up&!buff.demonsurge_spirit_burst.up
actions.fs+=/the_hunt
actions.fs+=/soul_carver,if=(!talent.fiery_demise|talent.fiery_demise&dot.fiery_brand.ticking)&(((soul_fragments.total+3)<=6)&fury>=15&!prev_gcd.1.sigil_of_spite)
actions.fs+=/sigil_of_spite,if=(((variable.can_spbomb|(buff.metamorphosis.up&variable.can_spburst))&fury>=40))|((variable.can_spbomb_soon|(buff.metamorphosis.up&variable.can_spburst_soon))|soul_fragments<=1)
actions.fs+=/bulk_extraction,if=spell_targets>=5
actions.fs+=/spirit_burst,if=talent.spirit_bomb&variable.can_spburst
actions.fs+=/spirit_bomb,if=variable.can_spbomb
actions.fs+=/felblade,if=(fury<40&((buff.metamorphosis.up&(variable.can_spburst|variable.can_spburst_soon))|(!buff.metamorphosis.up&(variable.can_spbomb|variable.can_spbomb_soon))))|fury<30
actions.fs+=/fracture,if=(fury<40&((buff.metamorphosis.up&(variable.can_spburst|variable.can_spburst_soon))|(!buff.metamorphosis.up&(variable.can_spbomb|variable.can_spbomb_soon))))|((buff.metamorphosis.up&variable.can_spburst_one_gcd)|(!buff.metamorphosis.up&variable.can_spbomb_one_gcd))
actions.fs+=/soul_sunder,if=!variable.dont_soul_cleave
actions.fs+=/soul_cleave,if=!variable.dont_soul_cleave
actions.fs+=/fracture
actions.fs+=/throw_glaive

actions.fs_execute=metamorphosis,use_off_gcd=1
actions.fs_execute+=/the_hunt
actions.fs_execute+=/sigil_of_flame
actions.fs_execute+=/fiery_brand
actions.fs_execute+=/sigil_of_spite
actions.fs_execute+=/soul_carver
actions.fs_execute+=/fel_devastation

actions.meta_prep=metamorphosis,use_off_gcd=1,if=cooldown.sigil_of_flame.charges<1
actions.meta_prep+=/fiery_brand,if=talent.fiery_demise&active_dot.fiery_brand=0
actions.meta_prep+=/potion,use_off_gcd=1
actions.meta_prep+=/sigil_of_flame

actions.metamorphosis=call_action_list,name=externals
actions.metamorphosis+=/spirit_burst,if=talent.spirit_bomb&(buff.metamorphosis.remains<(gcd.remains+execute_time+1))&buff.demonsurge_spirit_burst.up
actions.metamorphosis+=/sigil_of_spite,if=((variable.can_spburst&fury>=40)|variable.can_spburst_soon)
actions.metamorphosis+=/spirit_burst,if=talent.spirit_bomb&variable.can_spburst&buff.demonsurge_spirit_burst.up|soul_fragments>=5
actions.metamorphosis+=/soul_carver,if=soul_fragments.total<=2&!prev_gcd.1.sigil_of_spite
actions.metamorphosis+=/sigil_of_spite,if=soul_fragments<=1
actions.metamorphosis+=/fel_desolation,if=prev_gcd.2.sigil_of_spite|prev_gcd.2.soul_carver|!variable.can_spburst&(variable.can_spburst_soon|soul_fragments.inactive>=2)|(!buff.demonsurge_soul_sunder.up&!buff.demonsurge_spirit_burst.up&!buff.demonsurge_consuming_fire.up&!buff.demonsurge_sigil_of_doom.up&cooldown.sigil_of_doom.charges<1&buff.demonsurge_fel_desolation.up)
actions.metamorphosis+=/sigil_of_doom,if=talent.ascending_flame|(!talent.ascending_flame&(dot.sigil_of_doom.remains<(1+talent.quickened_sigils)&!prev_gcd.1.sigil_of_doom))
actions.metamorphosis+=/bulk_extraction,if=(variable.can_spburst|variable.can_spburst_soon)&!buff.soul_furnace_damage_amp.up&buff.soul_furnace_stack.stack<=6&buff.soul_furnace_stack.stack+(spell_targets.bulk_extraction>?5)>=10
actions.metamorphosis+=/spirit_burst,if=(talent.spirit_bomb&variable.can_spburst)
actions.metamorphosis+=/fracture,if=variable.big_aoe&(soul_fragments>=2&soul_fragments<=3)
actions.metamorphosis+=/felblade,if=(fury<40&(variable.can_spburst|variable.can_spburst_soon))|fury<30
actions.metamorphosis+=/soul_sunder,if=!variable.dont_soul_cleave
actions.metamorphosis+=/felblade
actions.metamorphosis+=/fracture

actions.rg_active=metamorphosis,use_off_gcd=1,if=!buff.metamorphosis.up&(buff.rending_strike.up&!buff.glaive_flurry.up)&soul_fragments<=1
actions.rg_active+=/felblade,if=fury<30&!variable.rg_enhance_cleave&buff.rending_strike.up&buff.glaive_flurry.up
actions.rg_active+=/the_hunt,if=!buff.reavers_glaive.up&(debuff.reavers_mark.remains>(gcd.remains+execute_time+action.soul_cleave.execute_time+(talent.fracture&action.fracture.execute_time|!talent.fracture&action.shear.execute_time)+gcd.max))
actions.rg_active+=/fracture,if=variable.rg_enhance_cleave&buff.rending_strike.up&buff.glaive_flurry.up|!variable.rg_enhance_cleave&!buff.glaive_flurry.up
actions.rg_active+=/shear,if=variable.rg_enhance_cleave&buff.rending_strike.up&buff.glaive_flurry.up|!variable.rg_enhance_cleave&!buff.glaive_flurry.up
actions.rg_active+=/bulk_extraction,if=!buff.soul_furnace_damage_amp.up&buff.soul_furnace_stack.stack+(spell_targets>?5)>=10
actions.rg_active+=/soul_cleave,if=!variable.rg_enhance_cleave&buff.glaive_flurry.up&buff.rending_strike.up|variable.rg_enhance_cleave&!buff.rending_strike.up
actions.rg_active+=/felblade
actions.rg_active+=/fracture,if=!buff.rending_strike.up

```

# ActionPriorityLists\demonhunter_havoc.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/augmentation
actions.precombat+=/food
actions.precombat+=/snapshot_stats
actions.precombat+=/variable,name=3min_trinket,value=trinket.1.cooldown.duration=180|trinket.2.cooldown.duration=180
actions.precombat+=/variable,name=trinket_sync_slot,value=1,if=trinket.1.has_stat.any_dps&(!trinket.2.has_stat.any_dps|trinket.1.cooldown.duration>=trinket.2.cooldown.duration)
actions.precombat+=/variable,name=trinket_sync_slot,value=2,if=trinket.2.has_stat.any_dps&(!trinket.1.has_stat.any_dps|trinket.2.cooldown.duration>trinket.1.cooldown.duration)
actions.precombat+=/arcane_torrent
actions.precombat+=/immolation_aura

# Executed every time the actor is available.
actions=auto_attack,if=!buff.out_of_range.up
actions+=/retarget_auto_attack,line_cd=1,target_if=min:debuff.burning_wound.remains,if=talent.burning_wound&talent.demon_blades&active_dot.burning_wound<(spell_targets>?3)
actions+=/retarget_auto_attack,line_cd=1,target_if=min:!target.is_boss,if=talent.burning_wound&talent.demon_blades&active_dot.burning_wound=(spell_targets>?3)
actions+=/variable,name=fel_barrage,op=set,value=talent.fel_barrage&(cooldown.fel_barrage.remains<gcd.max*7&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in<gcd.max*7|raid_event.adds.in>90)&(cooldown.metamorphosis.remains|active_enemies>2)|buff.fel_barrage.up)&!(active_enemies=1&!raid_event.adds.exists)
actions+=/disrupt
actions+=/call_action_list,name=cooldown
actions+=/fel_rush,if=buff.unbound_chaos.up&buff.unbound_chaos.remains<gcd.max*2
actions+=/pick_up_fragment,mode=nearest,type=lesser,if=fury.deficit>=45&(!cooldown.eye_beam.ready|fury<30)
actions+=/run_action_list,name=opener,if=(cooldown.eye_beam.up|cooldown.metamorphosis.up)&time<15&(raid_event.adds.in>40)
actions+=/run_action_list,name=fel_barrage,if=variable.fel_barrage&raid_event.adds.up
actions+=/immolation_aura,if=active_enemies>2&talent.ragefire&buff.unbound_chaos.down&(!talent.fel_barrage|cooldown.fel_barrage.remains>recharge_time)&debuff.essence_break.down
actions+=/immolation_aura,if=active_enemies>2&talent.ragefire&raid_event.adds.up&raid_event.adds.remains<15&raid_event.adds.remains>5&debuff.essence_break.down
actions+=/fel_rush,if=buff.unbound_chaos.up&active_enemies>2&(!talent.inertia|cooldown.eye_beam.remains+2>buff.unbound_chaos.remains)
actions+=/vengeful_retreat,use_off_gcd=1,if=talent.initiative&(cooldown.eye_beam.remains>15&gcd.remains<0.3|gcd.remains<0.1&cooldown.eye_beam.remains<=gcd.remains&(cooldown.metamorphosis.remains>10|cooldown.blade_dance.remains<gcd.max*2))&time>4
actions+=/run_action_list,name=fel_barrage,if=variable.fel_barrage|!talent.demon_blades&talent.fel_barrage&(buff.fel_barrage.up|cooldown.fel_barrage.up)&buff.metamorphosis.down
actions+=/run_action_list,name=meta,if=buff.metamorphosis.up
actions+=/fel_rush,if=buff.unbound_chaos.up&talent.inertia&buff.inertia.down&cooldown.blade_dance.remains<4&cooldown.eye_beam.remains>5&(action.immolation_aura.charges>0|action.immolation_aura.recharge_time+2<cooldown.eye_beam.remains|cooldown.eye_beam.remains>buff.unbound_chaos.remains-2)
actions+=/fel_rush,if=talent.momentum&cooldown.eye_beam.remains<gcd.max*2
actions+=/immolation_aura,if=buff.unbound_chaos.down&full_recharge_time<gcd.max*2&(raid_event.adds.in>full_recharge_time|active_enemies>desired_targets)
actions+=/immolation_aura,if=immolation_aura,if=active_enemies>desired_targets&buff.unbound_chaos.down&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>full_recharge_time)
actions+=/immolation_aura,if=talent.inertia&buff.unbound_chaos.down&cooldown.eye_beam.remains<5&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>full_recharge_time)
actions+=/immolation_aura,if=talent.inertia&buff.inertia.down&buff.unbound_chaos.down&recharge_time+5<cooldown.eye_beam.remains&cooldown.blade_dance.remains&cooldown.blade_dance.remains<4&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>full_recharge_time)&charges_fractional>1.00
actions+=/immolation_aura,if=fight_remains<15&cooldown.blade_dance.remains
actions+=/eye_beam,if=!talent.essence_break&(!talent.chaotic_transformation|cooldown.metamorphosis.remains<5+3*talent.shattered_destiny|cooldown.metamorphosis.remains>15)&(active_enemies>desired_targets*2|raid_event.adds.in>30-talent.cycle_of_hatred.rank*13)
actions+=/eye_beam,if=talent.essence_break&(cooldown.essence_break.remains<gcd.max*2+5*talent.shattered_destiny|talent.shattered_destiny&cooldown.essence_break.remains>10)&(cooldown.blade_dance.remains<7|raid_event.adds.up)&(!talent.initiative|cooldown.vengeful_retreat.remains>10|raid_event.adds.up)&(active_enemies+3>=desired_targets+raid_event.adds.count|raid_event.adds.in>30-talent.cycle_of_hatred.rank*6)&(!talent.inertia|buff.unbound_chaos.up|action.immolation_aura.charges=0&action.immolation_aura.recharge_time>5)&(!raid_event.adds.up|raid_event.adds.remains>8)|fight_remains<10
actions+=/blade_dance,if=cooldown.eye_beam.remains>gcd.max|cooldown.eye_beam.up
actions+=/glaive_tempest,if=active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>10
actions+=/sigil_of_flame,if=active_enemies>3
actions+=/chaos_strike,if=debuff.essence_break.up
actions+=/felblade
actions+=/throw_glaive,if=full_recharge_time<=cooldown.blade_dance.remains&cooldown.metamorphosis.remains>5&talent.soulscar&set_bonus.tier31_2pc
actions+=/throw_glaive,if=!set_bonus.tier31_2pc&(active_enemies>1|talent.soulscar)
actions+=/chaos_strike,if=cooldown.eye_beam.remains>gcd.max*2|fury>80
actions+=/immolation_aura,if=!talent.inertia&(raid_event.adds.in>full_recharge_time|active_enemies>desired_targets&active_enemies>2)
actions+=/sigil_of_flame,if=buff.out_of_range.down&debuff.essence_break.down&(!talent.fel_barrage|cooldown.fel_barrage.remains>25|(active_enemies=1&!raid_event.adds.exists))
actions+=/demons_bite
actions+=/fel_rush,if=buff.unbound_chaos.down&recharge_time<cooldown.eye_beam.remains&debuff.essence_break.down&(cooldown.eye_beam.remains>8|charges_fractional>1.01)
actions+=/arcane_torrent,if=buff.out_of_range.down&debuff.essence_break.down&fury<100

actions.cooldown=metamorphosis,if=(!talent.initiative|cooldown.vengeful_retreat.remains)&((!talent.demonic|prev_gcd.1.death_sweep|prev_gcd.2.death_sweep|prev_gcd.3.death_sweep)&cooldown.eye_beam.remains&(!talent.essence_break|debuff.essence_break.up)&buff.fel_barrage.down&(raid_event.adds.in>40|(raid_event.adds.remains>8|!talent.fel_barrage)&active_enemies>2)|!talent.chaotic_transformation|fight_remains<30)
actions.cooldown+=/potion,if=fight_remains<35|buff.metamorphosis.up
actions.cooldown+=/invoke_external_buff,name=power_infusion,if=buff.metamorphosis.up|fight_remains<=20
actions.cooldown+=/use_item,slot=trinket1,use_off_gcd=1,if=((cooldown.eye_beam.remains<gcd.max&active_enemies>1|buff.metamorphosis.up)&(raid_event.adds.in>trinket.1.cooldown.duration-15|raid_event.adds.remains>8)|!trinket.1.has_buff.any|fight_remains<25)&(!equipped.witherbarks_branch|trinket.2.cooldown.remains>20)&time>0
actions.cooldown+=/use_item,slot=trinket2,use_off_gcd=1,if=((cooldown.eye_beam.remains<gcd.max&active_enemies>1|buff.metamorphosis.up)&(raid_event.adds.in>trinket.2.cooldown.duration-15|raid_event.adds.remains>8)|!trinket.2.has_buff.any|fight_remains<25)&(!equipped.witherbarks_branch|trinket.1.cooldown.remains>20)&time>0
actions.cooldown+=/use_item,name=witherbarks_branch,if=(talent.essence_break&cooldown.essence_break.remains<gcd.max|!talent.essence_break)&(active_enemies+3>=desired_targets+raid_event.adds.count|raid_event.adds.in>105)|fight_remains<25
actions.cooldown+=/the_hunt,if=debuff.essence_break.down&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>(1+!set_bonus.tier31_2pc)*45)&time>5
actions.cooldown+=/sigil_of_spite,if=debuff.essence_break.down

actions.fel_barrage=variable,name=generator_up,op=set,value=cooldown.felblade.remains<gcd.max|cooldown.sigil_of_flame.remains<gcd.max
actions.fel_barrage+=/variable,name=fury_gen,op=set,value=1%(2.6*attack_haste)*12+buff.immolation_aura.stack*6+buff.tactical_retreat.up*10
actions.fel_barrage+=/variable,name=gcd_drain,op=set,value=gcd.max*32
actions.fel_barrage+=/annihilation,if=buff.inner_demon.up
actions.fel_barrage+=/eye_beam,if=buff.fel_barrage.down&(active_enemies>1&raid_event.adds.up|raid_event.adds.in>40)
actions.fel_barrage+=/essence_break,if=buff.fel_barrage.down&buff.metamorphosis.up
actions.fel_barrage+=/death_sweep,if=buff.fel_barrage.down
actions.fel_barrage+=/immolation_aura,if=buff.unbound_chaos.down&(active_enemies>2|buff.fel_barrage.up)
actions.fel_barrage+=/glaive_tempest,if=buff.fel_barrage.down&active_enemies>1
actions.fel_barrage+=/blade_dance,if=buff.fel_barrage.down
actions.fel_barrage+=/fel_barrage,if=fury>100&(raid_event.adds.in>90|raid_event.adds.in<gcd.max|raid_event.adds.remains>4&active_enemies>2)
actions.fel_barrage+=/fel_rush,if=buff.unbound_chaos.up&fury>20&buff.fel_barrage.up
actions.fel_barrage+=/sigil_of_flame,if=fury.deficit>40&buff.fel_barrage.up
actions.fel_barrage+=/felblade,if=buff.fel_barrage.up&fury.deficit>40
actions.fel_barrage+=/death_sweep,if=fury-variable.gcd_drain-35>0&(buff.fel_barrage.remains<3|variable.generator_up|fury>80|variable.fury_gen>18)
actions.fel_barrage+=/glaive_tempest,if=fury-variable.gcd_drain-30>0&(buff.fel_barrage.remains<3|variable.generator_up|fury>80|variable.fury_gen>18)
actions.fel_barrage+=/blade_dance,if=fury-variable.gcd_drain-35>0&(buff.fel_barrage.remains<3|variable.generator_up|fury>80|variable.fury_gen>18)
actions.fel_barrage+=/arcane_torrent,if=fury.deficit>40&buff.fel_barrage.up
actions.fel_barrage+=/fel_rush,if=buff.unbound_chaos.up
actions.fel_barrage+=/the_hunt,if=fury>40&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>(1+set_bonus.tier31_2pc)*40)
actions.fel_barrage+=/demons_bite

actions.meta=death_sweep,if=buff.metamorphosis.remains<gcd.max
actions.meta+=/annihilation,if=buff.metamorphosis.remains<gcd.max
actions.meta+=/fel_rush,if=buff.unbound_chaos.up&talent.inertia
actions.meta+=/fel_rush,if=talent.momentum&buff.momentum.remains<gcd.max*2
actions.meta+=/annihilation,if=buff.inner_demon.up&(cooldown.eye_beam.remains<gcd.max*3&cooldown.blade_dance.remains|cooldown.metamorphosis.remains<gcd.max*3)
actions.meta+=/essence_break,if=fury>20&(cooldown.metamorphosis.remains>10|cooldown.blade_dance.remains<gcd.max*2)&(buff.unbound_chaos.down|buff.inertia.up|!talent.inertia)|fight_remains<10
actions.meta+=/immolation_aura,if=debuff.essence_break.down&cooldown.blade_dance.remains>gcd.max+0.5&buff.unbound_chaos.down&talent.inertia&buff.inertia.down&full_recharge_time+3<cooldown.eye_beam.remains&buff.metamorphosis.remains>5
actions.meta+=/death_sweep
actions.meta+=/eye_beam,if=debuff.essence_break.down&buff.inner_demon.down
actions.meta+=/glaive_tempest,if=debuff.essence_break.down&(cooldown.blade_dance.remains>gcd.max*2|fury>60)&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>10)
actions.meta+=/sigil_of_flame,if=active_enemies>2
actions.meta+=/annihilation,if=cooldown.blade_dance.remains>gcd.max*2|fury>60|buff.metamorphosis.remains<5&cooldown.felblade.up
actions.meta+=/sigil_of_flame,if=buff.metamorphosis.remains>5
actions.meta+=/felblade
actions.meta+=/sigil_of_flame,if=debuff.essence_break.down
actions.meta+=/immolation_aura,if=buff.out_of_range.down&recharge_time<(cooldown.eye_beam.remains<?buff.metamorphosis.remains)&(active_enemies>=desired_targets+raid_event.adds.count|raid_event.adds.in>full_recharge_time)
actions.meta+=/fel_rush,if=talent.momentum
actions.meta+=/fel_rush,if=buff.unbound_chaos.down&recharge_time<cooldown.eye_beam.remains&debuff.essence_break.down&(cooldown.eye_beam.remains>8|charges_fractional>1.01)&buff.out_of_range.down
actions.meta+=/demons_bite

actions.opener=use_items
actions.opener+=/vengeful_retreat,if=prev_gcd.1.death_sweep
actions.opener+=/metamorphosis,if=prev_gcd.1.death_sweep|(!talent.chaotic_transformation)&(!talent.initiative|cooldown.vengeful_retreat.remains>2)|!talent.demonic
actions.opener+=/felblade,if=debuff.essence_break.down,line_cd=60
actions.opener+=/potion
actions.opener+=/immolation_aura,if=charges=2&buff.unbound_chaos.down&(buff.inertia.down|active_enemies>2)
actions.opener+=/annihilation,if=buff.inner_demon.up&(!talent.chaotic_transformation|cooldown.metamorphosis.up)
actions.opener+=/eye_beam,if=debuff.essence_break.down&buff.inner_demon.down&(!buff.metamorphosis.up|cooldown.blade_dance.remains)
actions.opener+=/fel_rush,if=talent.inertia&(buff.inertia.down|active_enemies>2)&buff.unbound_chaos.up
actions.opener+=/the_hunt,if=active_enemies>desired_targets|raid_event.adds.in>40+50*!set_bonus.tier31_2pc
actions.opener+=/essence_break
actions.opener+=/death_sweep
actions.opener+=/annihilation
actions.opener+=/demons_bite

```

# ActionPriorityLists\deathknight_unholy.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/snapshot_stats
actions.precombat+=/raise_dead
actions.precombat+=/army_of_the_dead,precombat_time=2
actions.precombat+=/variable,name=trinket_1_buffs,value=trinket.1.has_use_buff|trinket.1.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_2_buffs,value=trinket.2.has_use_buff|trinket.2.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_1_duration,op=setif,value=20,value_else=trinket.1.proc.any_dps.duration,condition=trinket.1.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_2_duration,op=setif,value=20,value_else=trinket.2.proc.any_dps.duration,condition=trinket.2.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_1_sync,op=setif,value=1,value_else=0.5,condition=variable.trinket_1_buffs&(talent.apocalypse&trinket.1.cooldown.duration%%cooldown.apocalypse.duration=0|talent.dark_transformation&trinket.1.cooldown.duration%%cooldown.dark_transformation.duration=0)|trinket.1.is.treacherous_transmitter
actions.precombat+=/variable,name=trinket_2_sync,op=setif,value=1,value_else=0.5,condition=variable.trinket_2_buffs&(talent.apocalypse&trinket.2.cooldown.duration%%cooldown.apocalypse.duration=0|talent.dark_transformation&trinket.2.cooldown.duration%%cooldown.dark_transformation.duration=0)|trinket.2.is.treacherous_transmitter
actions.precombat+=/variable,name=trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_1_buffs&variable.trinket_2_buffs&(trinket.2.has_cooldown|!trinket.1.has_cooldown)|variable.trinket_2_buffs&((trinket.2.cooldown.duration%trinket.2.proc.any_dps.duration)*(1.5+trinket.2.has_buff.strength)*(variable.trinket_2_sync))>((trinket.1.cooldown.duration%trinket.1.proc.any_dps.duration)*(1.5+trinket.1.has_buff.strength)*(variable.trinket_1_sync)*(1+((trinket.1.ilvl-trinket.2.ilvl)%100)))
actions.precombat+=/variable,name=damage_trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_1_buffs&!variable.trinket_2_buffs&trinket.2.ilvl>=trinket.1.ilvl

# Executed every time the actor is available.
actions=auto_attack
# Call Action Lists
actions+=/call_action_list,name=variables
actions+=/call_action_list,name=san_trinkets,if=talent.vampiric_strike
actions+=/call_action_list,name=trinkets,if=!talent.vampiric_strike
actions+=/call_action_list,name=racials
actions+=/call_action_list,name=cds_shared
actions+=/call_action_list,name=cds,if=!talent.vampiric_strike
actions+=/call_action_list,name=cds_san,if=talent.vampiric_strike
actions+=/call_action_list,name=cleave,if=active_enemies<4&active_enemies>=2
actions+=/call_action_list,name=aoe_burst,if=active_enemies>=4&buff.death_and_decay.up
actions+=/call_action_list,name=aoe,if=active_enemies>=4&!buff.death_and_decay.up
actions+=/run_action_list,name=san_fishing,if=talent.gift_of_the_sanlayn&!buff.gift_of_the_sanlayn.up&buff.essence_of_the_blood_queen.remains<cooldown.dark_transformation.remains+2
actions+=/call_action_list,name=san_st,if=active_enemies=1&talent.vampiric_strike
actions+=/call_action_list,name=st,if=active_enemies=1&!talent.vampiric_strike

# AOE
actions.aoe=any_dnd,if=!buff.death_and_decay.up&(!talent.bursting_sores|death_knight.fwounded_targets=active_enemies|death_knight.fwounded_targets>=8|raid_event.adds.exists&raid_event.adds.remains<=11&raid_event.adds.remains>5)
actions.aoe+=/epidemic,if=!variable.pooling_runic_power
actions.aoe+=/festering_strike,target_if=min:debuff.festering_wound.stack,if=cooldown.apocalypse.remains<gcd&debuff.festering_wound.stack=0|buff.festering_scythe.react
actions.aoe+=/wound_spender,target_if=max:debuff.festering_wound.stack,if=debuff.festering_wound.stack>=1&cooldown.apocalypse.remains>gcd
actions.aoe+=/festering_strike,target_if=min:debuff.festering_wound.stack,if=debuff.festering_wound.stack<4

# AoE Burst
actions.aoe_burst=defile,if=!defile.ticking
actions.aoe_burst+=/epidemic,if=!variable.pooling_runic_power&(active_enemies>=6&!talent.bursting_sores|talent.bursting_sores&death_knight.fwounded_targets!=active_enemies&death_knight.fwounded_targets<6|!talent.bursting_sores&runic_power.deficit<30|buff.sudden_doom.react)
actions.aoe_burst+=/wound_spender,target_if=max:debuff.festering_wound.stack,if=debuff.festering_wound.stack>=1
actions.aoe_burst+=/festering_strike,if=buff.festering_scythe.react
actions.aoe_burst+=/epidemic,if=!variable.pooling_runic_power
actions.aoe_burst+=/wound_spender

# Non-San'layn Cooldowns
actions.cds=dark_transformation,if=(variable.st_planning|variable.adds_remain)&(cooldown.apocalypse.remains<8|!talent.apocalypse|active_enemies>=1)
actions.cds+=/unholy_assault,if=(variable.st_planning|variable.adds_remain)&(cooldown.apocalypse.remains<gcd*2|!talent.apocalypse|active_enemies>=2&buff.dark_transformation.up)
actions.cds+=/apocalypse,if=(variable.st_planning|variable.adds_remain)
actions.cds+=/outbreak,target_if=target.time_to_die>dot.virulent_plague.remains,if=(dot.virulent_plague.refreshable|talent.superstrain&(dot.frost_fever.refreshable|dot.blood_plague.refreshable))&(!talent.unholy_blight|talent.unholy_blight&cooldown.dark_transformation.remains>15%((3*talent.superstrain)+(2*talent.ebon_fever)+(2*talent.plaguebringer)))&(!talent.raise_abomination|talent.raise_abomination&cooldown.raise_abomination.remains>15%((3*talent.superstrain)+(2*talent.ebon_fever)+(2*talent.plaguebringer)))
actions.cds+=/abomination_limb,if=(variable.st_planning|variable.adds_remain)&(active_enemies>=2|!buff.sudden_doom.react&buff.festermight.up&debuff.festering_wound.stack<=2)

# San'layn Cooldowns
actions.cds_san=dark_transformation,if=active_enemies>=1&(variable.st_planning|variable.adds_remain)&(talent.apocalypse&(pet.apoc_ghoul.active|active_enemies>=2)|!talent.apocalypse)
actions.cds_san+=/unholy_assault,if=(variable.st_planning|variable.adds_remain)&(buff.dark_transformation.up&buff.dark_transformation.remains<12)
actions.cds_san+=/apocalypse,if=(variable.st_planning|variable.adds_remain)&(debuff.festering_wound.stack>=3|active_enemies>=2)
actions.cds_san+=/outbreak,target_if=target.time_to_die>dot.virulent_plague.remains,if=(pet.abomination.remains<15&dot.virulent_plague.refreshable|talent.morbidity&buff.infliction_of_sorrow.up&talent.superstrain&dot.frost_fever.refreshable&dot.blood_plague.refreshable)&(!talent.unholy_blight|talent.unholy_blight&cooldown.dark_transformation.remains>15%((3*talent.superstrain)+(2*talent.ebon_fever)+(2*talent.plaguebringer)))&(!talent.raise_abomination|talent.raise_abomination&cooldown.raise_abomination.remains>15%((3*talent.superstrain)+(2*talent.ebon_fever)+(2*talent.plaguebringer)))
actions.cds_san+=/abomination_limb,if=active_enemies>=1&(variable.st_planning|variable.adds_remain)&(active_enemies>=2|!buff.dark_transformation.up&!buff.sudden_doom.react&buff.festermight.up&debuff.festering_wound.stack<=2)

# Shared Cooldowns
actions.cds_shared=potion,if=active_enemies>=1&(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&30>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=30|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=30|pet.abomination.active&pet.abomination.remains<=30)|fight_remains<=30
# Use <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> while <a href='https://www.wowhead.com/spell=49206/summon-gargoyle'>Gargoyle</a> is up, as well as <a href='https://www.wowhead.com/spell=275699/apocalypse'>Apocalypse</a> or with <a href='https://www.wowhead.com/spell=63560/dark-transformation'>Dark Transformation</a> if <a href='https://www.wowhead.com/spell=275699/apocalypse'>Apocalypse</a> or <a href='https://www.wowhead.com/spell=49206/summon-gargoyle'>Gargoyle</a> are not talented
actions.cds_shared+=/invoke_external_buff,name=power_infusion,if=active_enemies>=1&(variable.st_planning|variable.adds_remain)&(pet.gargoyle.active&pet.gargoyle.remains<=22|!talent.summon_gargoyle&talent.army_of_the_dead&(talent.raise_abomination&pet.abomination.active&pet.abomination.remains<18|!talent.raise_abomination&pet.army_ghoul.active&pet.army_ghoul.remains<=18)|!talent.summon_gargoyle&!talent.army_of_the_dead&buff.dark_transformation.up|!talent.summon_gargoyle&buff.dark_transformation.up|!pet.gargoyle.active&cooldown.summon_gargoyle.remains+10>cooldown.invoke_external_buff_power_infusion.duration|active_enemies>=3&(buff.dark_transformation.up|death_and_decay.ticking))
actions.cds_shared+=/army_of_the_dead,if=(variable.st_planning|variable.adds_remain)&(talent.commander_of_the_dead&cooldown.dark_transformation.remains<5|!talent.commander_of_the_dead&active_enemies>=1)|fight_remains<35
actions.cds_shared+=/raise_abomination,if=(variable.st_planning|variable.adds_remain)&(talent.commander_of_the_dead&cooldown.dark_transformation.remains<gcd*2|!talent.commander_of_the_dead&active_enemies>=1)|fight_remains<30
actions.cds_shared+=/summon_gargoyle,use_off_gcd=1,if=(variable.st_planning|variable.adds_remain)&(buff.commander_of_the_dead.up|!talent.commander_of_the_dead&active_enemies>=1)
actions.cds_shared+=/vile_contagion,target_if=max:debuff.festering_wound.stack,if=variable.adds_remain&(debuff.festering_wound.stack=6&(defile.ticking|death_and_decay.ticking|cooldown.any_dnd.remains<3)|raid_event.adds.exists&raid_event.adds.remains<=11&raid_event.adds.remains>5|buff.death_and_decay.up&debuff.festering_wound.stack>=4|cooldown.any_dnd.remains<3&debuff.festering_wound.stack>=4)

# Cleave
actions.cleave=any_dnd,if=!buff.death_and_decay.up
actions.cleave+=/death_coil,if=!variable.pooling_runic_power&talent.improved_death_coil
actions.cleave+=/festering_strike,if=!variable.pop_wounds&debuff.festering_wound.stack<4|buff.festering_scythe.react
actions.cleave+=/wound_spender,if=variable.pop_wounds
actions.cleave+=/epidemic,if=!variable.pooling_runic_power

# Racials
actions.racials=arcane_torrent,if=runic_power<20&rune<2
actions.racials+=/blood_fury,if=(buff.blood_fury.duration+3>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(pet.army_ghoul.active&pet.army_ghoul.remains<=buff.blood_fury.duration+3|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.blood_fury.duration+3|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.blood_fury.duration+3
actions.racials+=/berserking,if=(buff.berserking.duration+3>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(pet.army_ghoul.active&pet.army_ghoul.remains<=buff.berserking.duration+3|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.berserking.duration+3|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.berserking.duration+3
actions.racials+=/lights_judgment,if=buff.unholy_strength.up&(!talent.festermight|buff.festermight.remains<target.time_to_die|buff.unholy_strength.remains<target.time_to_die)
actions.racials+=/ancestral_call,if=(18>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(pet.army_ghoul.active&pet.army_ghoul.remains<=18|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=18|active_enemies>=2&death_and_decay.ticking)|fight_remains<=18
actions.racials+=/arcane_pulse,if=active_enemies>=2|(rune.deficit>=5&runic_power.deficit>=60)
actions.racials+=/fireblood,if=(buff.fireblood.duration+3>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(pet.army_ghoul.active&pet.army_ghoul.remains<=buff.fireblood.duration+3|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.fireblood.duration+3|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.fireblood.duration+3
actions.racials+=/bag_of_tricks,if=active_enemies=1&(buff.unholy_strength.up|fight_remains<5)

# San'layn Fishing
actions.san_fishing=antimagic_shell,if=death_knight.ams_absorb_percent>0&runic_power<40
actions.san_fishing+=/any_dnd,if=!buff.death_and_decay.up&!buff.vampiric_strike.react
actions.san_fishing+=/death_coil,if=buff.sudden_doom.react&talent.doomed_bidding
actions.san_fishing+=/soul_reaper,if=target.health.pct<=35&fight_remains>5
actions.san_fishing+=/death_coil,if=!buff.vampiric_strike.react
actions.san_fishing+=/wound_spender,if=(debuff.festering_wound.stack>=3-pet.abomination.active&cooldown.apocalypse.remains>variable.apoc_timing)|buff.vampiric_strike.react
actions.san_fishing+=/festering_strike,if=debuff.festering_wound.stack<3-pet.abomination.active

# Single Target San'layn
actions.san_st=wound_spender,if=buff.essence_of_the_blood_queen.remains<3&buff.vampiric_strike.react|talent.gift_of_the_sanlayn&buff.dark_transformation.up&buff.dark_transformation.remains<gcd
actions.san_st+=/death_coil,if=buff.sudden_doom.react&buff.gift_of_the_sanlayn.remains&buff.essence_of_the_blood_queen.stack>=3&(talent.doomed_bidding|talent.rotten_touch)|rune<2&!buff.runic_corruption.up
actions.san_st+=/soul_reaper,if=target.health.pct<=35&!buff.gift_of_the_sanlayn.up&fight_remains>5
actions.san_st+=/festering_strike,if=(debuff.festering_wound.stack<4&cooldown.apocalypse.remains<variable.apoc_timing)|(talent.gift_of_the_sanlayn&!buff.gift_of_the_sanlayn.up|!talent.gift_of_the_sanlayn)&(buff.festering_scythe.react|debuff.festering_wound.stack<=1-pet.abomination.active)
actions.san_st+=/wound_spender,if=(debuff.festering_wound.stack>=3-pet.abomination.active&cooldown.apocalypse.remains>variable.apoc_timing)|buff.vampiric_strike.react&cooldown.apocalypse.remains>variable.apoc_timing
actions.san_st+=/death_coil,if=!variable.pooling_runic_power&debuff.death_rot.remains<gcd|(buff.sudden_doom.react&debuff.festering_wound.stack>=1|rune<2)
actions.san_st+=/wound_spender,if=debuff.festering_wound.stack>4
actions.san_st+=/death_coil,if=!variable.pooling_runic_power

# Trinkets San'layn
actions.san_trinkets=use_item,name=fyralath_the_dreamrender,if=dot.mark_of_fyralath.ticking&(active_enemies<5|active_enemies>21|fight_remains<4)&(pet.abomination.active|pet.army_ghoul.active|!talent.raise_abomination&!talent.army_of_the_dead|time>15)
actions.san_trinkets+=/do_treacherous_transmitter_task,use_off_gcd=1,if=buff.errant_manaforge_emission.up&buff.dark_transformation.up|buff.cryptic_instructions.up&buff.dark_transformation.up|buff.realigning_nexus_convergence_divergence.up&buff.dark_transformation.up
actions.san_trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=(variable.trinket_1_buffs|trinket.1.is.treacherous_transmitter)&(buff.dark_transformation.up&buff.dark_transformation.remains<variable.trinket_1_duration*0.73&(variable.trinket_priority=1|trinket.2.cooldown.remains|!trinket.2.has_cooldown))|variable.trinket_1_duration>=fight_remains
actions.san_trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=(variable.trinket_2_buffs|trinket.2.is.treacherous_transmitter)&(buff.dark_transformation.up&buff.dark_transformation.remains<variable.trinket_2_duration*0.73&(variable.trinket_priority=2|trinket.1.cooldown.remains|!trinket.1.has_cooldown))|variable.trinket_2_duration>=fight_remains
actions.san_trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=!variable.trinket_1_buffs&(variable.damage_trinket_priority=1|trinket.2.cooldown.remains|!trinket.2.has_cooldown|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination|!talent.summon_gargoyle&talent.army_of_the_dead&(!talent.raise_abomination&cooldown.army_of_the_dead.remains>20|talent.raise_abomination&cooldown.raise_abomination.remains>20)|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination&cooldown.dark_transformation.remains>20|talent.summon_gargoyle&cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15
actions.san_trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=!variable.trinket_2_buffs&(variable.damage_trinket_priority=2|trinket.1.cooldown.remains|!trinket.1.has_cooldown|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination|!talent.summon_gargoyle&talent.army_of_the_dead&(!talent.raise_abomination&cooldown.army_of_the_dead.remains>20|talent.raise_abomination&cooldown.raise_abomination.remains>20)|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination&cooldown.dark_transformation.remains>20|talent.summon_gargoyle&cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15

# Single Taget Non-San'layn
actions.st=soul_reaper,if=target.health.pct<=35&fight_remains>5
actions.st+=/death_coil,if=!variable.pooling_runic_power&variable.spend_rp|fight_remains<10
actions.st+=/festering_strike,if=!variable.pop_wounds&debuff.festering_wound.stack<4
actions.st+=/wound_spender,if=variable.pop_wounds
actions.st+=/death_coil,if=!variable.pooling_runic_power
actions.st+=/wound_spender,if=!variable.pop_wounds&debuff.festering_wound.stack>=4

# Trinkets Non-San'layn
actions.trinkets=use_item,name=fyralath_the_dreamrender,if=dot.mark_of_fyralath.ticking&(active_enemies<5|active_enemies>21|fight_remains<4)&(pet.abomination.active|pet.army_ghoul.active|!talent.raise_abomination&!talent.army_of_the_dead|time>15)
actions.trinkets+=/do_treacherous_transmitter_task,use_off_gcd=1,if=buff.errant_manaforge_emission.up&buff.dark_transformation.up|buff.cryptic_instructions.up&buff.dark_transformation.up|buff.realigning_nexus_convergence_divergence.up&buff.dark_transformation.up
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=(variable.trinket_1_buffs|trinket.1.is.treacherous_transmitter)&((!talent.summon_gargoyle&((!talent.army_of_the_dead|talent.army_of_the_dead&cooldown.army_of_the_dead.remains>trinket.1.cooldown.duration*0.51|death_knight.disable_aotd|talent.raise_abomination&cooldown.raise_abomination.remains>trinket.1.cooldown.duration*0.51)&((20>variable.trinket_1_duration&pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=variable.trinket_1_duration*1.2|20<=variable.trinket_1_duration&cooldown.apocalypse.remains<gcd&buff.dark_transformation.up)|(!talent.apocalypse|active_enemies>=2)&buff.dark_transformation.up)|pet.army_ghoul.active&pet.army_ghoul.remains<variable.trinket_1_duration*1.2|pet.abomination.active&pet.abomination.remains<variable.trinket_1_duration*1.2)|talent.summon_gargoyle&pet.gargoyle.active&pet.gargoyle.remains<variable.trinket_1_duration*1.2|cooldown.summon_gargoyle.remains>80)&(variable.trinket_priority=1|trinket.2.cooldown.remains|!trinket.2.has_cooldown))|variable.trinket_1_duration>=fight_remains
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=(variable.trinket_2_buffs|trinket.2.is.treacherous_transmitter)&((!talent.summon_gargoyle&((!talent.army_of_the_dead|talent.army_of_the_dead&cooldown.army_of_the_dead.remains>trinket.2.cooldown.duration*0.51|death_knight.disable_aotd|talent.raise_abomination&cooldown.raise_abomination.remains>trinket.2.cooldown.duration*0.51)&((20>variable.trinket_2_duration&pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=variable.trinket_2_duration*1.2|20<=variable.trinket_2_duration&cooldown.apocalypse.remains<gcd&buff.dark_transformation.up)|(!talent.apocalypse|active_enemies>=2)&buff.dark_transformation.up)|pet.army_ghoul.active&pet.army_ghoul.remains<variable.trinket_2_duration*1.2|pet.abomination.active&pet.abomination.remains<variable.trinket_2_duration*1.2)|talent.summon_gargoyle&pet.gargoyle.active&pet.gargoyle.remains<variable.trinket_2_duration*1.2|cooldown.summon_gargoyle.remains>80)&(variable.trinket_priority=2|trinket.1.cooldown.remains|!trinket.1.has_cooldown))|variable.trinket_2_duration>=fight_remains
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=!variable.trinket_1_buffs&(variable.damage_trinket_priority=1|trinket.2.cooldown.remains|!trinket.2.has_cooldown|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination|!talent.summon_gargoyle&talent.army_of_the_dead&(!talent.raise_abomination&cooldown.army_of_the_dead.remains>20|talent.raise_abomination&cooldown.raise_abomination.remains>20)|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination&cooldown.dark_transformation.remains>20|talent.summon_gargoyle&cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=!variable.trinket_2_buffs&(variable.damage_trinket_priority=2|trinket.1.cooldown.remains|!trinket.1.has_cooldown|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination|!talent.summon_gargoyle&talent.army_of_the_dead&(!talent.raise_abomination&cooldown.army_of_the_dead.remains>20|talent.raise_abomination&cooldown.raise_abomination.remains>20)|!talent.summon_gargoyle&!talent.army_of_the_dead&!talent.raise_abomination&cooldown.dark_transformation.remains>20|talent.summon_gargoyle&cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15

# Variables
actions.variables=variable,name=st_planning,op=setif,value=1,value_else=0,condition=active_enemies=1&(!raid_event.adds.exists|raid_event.adds.in>15)
actions.variables+=/variable,name=adds_remain,op=setif,value=1,value_else=0,condition=active_enemies>=2&(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.remains>6)
actions.variables+=/variable,name=apoc_timing,op=setif,value=7,value_else=3,condition=cooldown.apocalypse.remains<10&debuff.festering_wound.stack<=4&cooldown.unholy_assault.remains>10
actions.variables+=/variable,name=pop_wounds,op=setif,value=1,value_else=0,condition=(cooldown.apocalypse.remains>variable.apoc_timing|!talent.apocalypse)&(debuff.festering_wound.stack>=1&cooldown.unholy_assault.remains<20&talent.unholy_assault&variable.st_planning|debuff.rotten_touch.up&debuff.festering_wound.stack>=1|debuff.festering_wound.stack>=4-pet.abomination.active)|fight_remains<5&debuff.festering_wound.stack>=1
actions.variables+=/variable,name=pooling_runic_power,op=setif,value=1,value_else=0,condition=talent.vile_contagion&cooldown.vile_contagion.remains<3&runic_power<60&!variable.st_planning
actions.variables+=/variable,name=spend_rp,op=setif,value=1,value_else=0,condition=(!talent.rotten_touch|talent.rotten_touch&!debuff.rotten_touch.up|runic_power.deficit<20)&((talent.improved_death_coil&(active_enemies=2|talent.coil_of_devastation)|rune<3|pet.gargoyle.active|buff.sudden_doom.react|!variable.pop_wounds&debuff.festering_wound.stack>=4))

```

# ActionPriorityLists\deathknight_frost.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/variable,name=trinket_1_exclude,value=trinket.1.is.ruby_whelp_shell|trinket.1.is.whispering_incarnate_icon
actions.precombat+=/variable,name=trinket_2_exclude,value=trinket.2.is.ruby_whelp_shell|trinket.2.is.whispering_incarnate_icon
# Evaluates a trinkets cooldown, divided by pillar of frost, empower rune weapon, or breath of sindragosa's cooldown. If it's value has no remainder return 1, else return 0.5.
actions.precombat+=/variable,name=trinket_1_sync,op=setif,value=1,value_else=0.5,condition=trinket.1.has_use_buff&(talent.pillar_of_frost&!talent.breath_of_sindragosa&(trinket.1.cooldown.duration%%cooldown.pillar_of_frost.duration=0)|talent.breath_of_sindragosa&(cooldown.breath_of_sindragosa.duration%%trinket.1.cooldown.duration=0))
actions.precombat+=/variable,name=trinket_2_sync,op=setif,value=1,value_else=0.5,condition=trinket.2.has_use_buff&(talent.pillar_of_frost&!talent.breath_of_sindragosa&(trinket.2.cooldown.duration%%cooldown.pillar_of_frost.duration=0)|talent.breath_of_sindragosa&(cooldown.breath_of_sindragosa.duration%%trinket.2.cooldown.duration=0))
actions.precombat+=/variable,name=trinket_1_buffs,value=trinket.1.has_use_buff|(trinket.1.has_buff.strength|trinket.1.has_buff.mastery|trinket.1.has_buff.versatility|trinket.1.has_buff.haste|trinket.1.has_buff.crit&!variable.trinket_1_exclude)
actions.precombat+=/variable,name=trinket_2_buffs,value=trinket.2.has_use_buff|(trinket.2.has_buff.strength|trinket.2.has_buff.mastery|trinket.2.has_buff.versatility|trinket.2.has_buff.haste|trinket.2.has_buff.crit&!variable.trinket_2_exclude)
actions.precombat+=/variable,name=trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_1_buffs&variable.trinket_2_buffs&(trinket.2.has_cooldown&!variable.trinket_2_exclude|!trinket.1.has_cooldown)|variable.trinket_2_buffs&((trinket.2.cooldown.duration%trinket.2.proc.any_dps.duration)*(1.5+trinket.2.has_buff.strength)*(variable.trinket_2_sync))>((trinket.1.cooldown.duration%trinket.1.proc.any_dps.duration)*(1.5+trinket.1.has_buff.strength)*(variable.trinket_1_sync)*(1+((trinket.1.ilvl-trinket.2.ilvl)%100)))
actions.precombat+=/variable,name=damage_trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_1_buffs&!variable.trinket_2_buffs&trinket.2.ilvl>=trinket.1.ilvl
actions.precombat+=/variable,name=trinket_1_manual,value=trinket.1.is.algethar_puzzle_box
actions.precombat+=/variable,name=trinket_2_manual,value=trinket.2.is.algethar_puzzle_box
actions.precombat+=/variable,name=rw_buffs,value=talent.gathering_storm|talent.biting_cold
actions.precombat+=/variable,name=2h_check,value=main_hand.2h
actions.precombat+=/variable,name=static_obliterate_buffs,value=talent.arctic_assault|talent.frigid_executioner|variable.2h_check
actions.precombat+=/variable,name=breath_rp_cost,value=dbc.power.9067.cost_per_tick%10
actions.precombat+=/variable,name=static_rime_buffs,value=talent.rage_of_the_frozen_champion|talent.icebreaker
# APL Variable Option: How much Runic Power to pool before casting Breath of Sindragosa
actions.precombat+=/variable,name=breath_rp_threshold,default=70,op=reset
# APL Variable Option: Used with erw_breath_rune_trigger to determine when resources are low enough to use Empower Rune Weapon
actions.precombat+=/variable,name=erw_breath_rp_trigger,default=70,op=reset
# APL Variable Option: Used with erw_breath_rp_trigger to determine when resources are low enough to use Empower Rune Weapon
actions.precombat+=/variable,name=erw_breath_rune_trigger,default=3,op=reset
# APL Variable Option: How many Runes the APL will try to pool for Pillar of Frost with Obliteration. It is not a guarantee, just a goal.
actions.precombat+=/variable,name=oblit_rune_pooling,default=4,op=reset
# APL Variable Option: Amount of Runic Power pooled during Breath of Sindragosa to be able to use Rime
actions.precombat+=/variable,name=breath_rime_rp_threshold,default=60,op=reset

# Executed every time the actor is available.
actions=auto_attack
# Choose Action list to run
actions+=/call_action_list,name=variables
actions+=/call_action_list,name=trinkets
actions+=/call_action_list,name=high_prio_actions
actions+=/call_action_list,name=cooldowns
actions+=/call_action_list,name=racials
actions+=/call_action_list,name=cold_heart,if=talent.cold_heart&(!buff.killing_machine.up|talent.breath_of_sindragosa)&((debuff.razorice.stack=5|!death_knight.runeforge.razorice&!talent.glacial_advance&!talent.avalanche&!talent.arctic_assault)|fight_remains<=gcd)
actions+=/run_action_list,name=breath,if=buff.breath_of_sindragosa.up
actions+=/run_action_list,name=obliteration,if=talent.obliteration&buff.pillar_of_frost.up&!buff.breath_of_sindragosa.up
actions+=/call_action_list,name=aoe,if=active_enemies>=2
actions+=/call_action_list,name=single_target,if=active_enemies=1

# AoE Action List
actions.aoe=obliterate,if=buff.killing_machine.react&talent.cleaving_strikes&buff.death_and_decay.up
actions.aoe+=/howling_blast,if=!dot.frost_fever.ticking
actions.aoe+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=!variable.pooling_runic_power&debuff.razorice.stack=5&talent.shattering_blade&(talent.shattered_frost|active_enemies<4)
actions.aoe+=/howling_blast,if=buff.rime.react|!dot.frost_fever.ticking
actions.aoe+=/glacial_advance,target_if=max:(debuff.razorice.stack),if=!variable.pooling_runic_power&(variable.ga_priority|debuff.razorice.stack<5)
actions.aoe+=/obliterate
actions.aoe+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=!variable.pooling_runic_power
actions.aoe+=/horn_of_winter,if=rune<2&runic_power.deficit>25
actions.aoe+=/arcane_torrent,if=runic_power.deficit>25

# Breath Active Rotation
actions.breath=howling_blast,if=variable.rime_buffs&runic_power>(variable.breath_rime_rp_threshold-(talent.rage_of_the_frozen_champion*(dbc.effect.842306.base_value%10)))
actions.breath+=/horn_of_winter,if=rune<2&runic_power.deficit>30&(!buff.empower_rune_weapon.up|variable.breath_dying)
actions.breath+=/obliterate,target_if=max:(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=buff.killing_machine.react|runic_power.deficit>20
actions.breath+=/remorseless_winter,if=variable.breath_dying
actions.breath+=/death_and_decay,if=!buff.mograines_might.up&variable.st_planning&talent.unholy_ground&!buff.death_and_decay.up&runic_power.deficit>=10&!talent.obliteration|variable.breath_dying
actions.breath+=/howling_blast,if=variable.breath_dying
actions.breath+=/arcane_torrent,if=runic_power<60
actions.breath+=/howling_blast,if=buff.rime.react

# Cold Heart
actions.cold_heart=chains_of_ice,if=fight_remains<gcd&(rune<2|!buff.killing_machine.up&(!variable.2h_check&buff.cold_heart.stack>=4|variable.2h_check&buff.cold_heart.stack>8)|buff.killing_machine.up&(!variable.2h_check&buff.cold_heart.stack>8|variable.2h_check&buff.cold_heart.stack>10))
actions.cold_heart+=/chains_of_ice,if=!talent.obliteration&buff.pillar_of_frost.up&buff.cold_heart.stack>=10&(buff.pillar_of_frost.remains<gcd*(1+(talent.frostwyrms_fury&cooldown.frostwyrms_fury.ready))|buff.unholy_strength.up&buff.unholy_strength.remains<gcd)
actions.cold_heart+=/chains_of_ice,if=!talent.obliteration&death_knight.runeforge.fallen_crusader&!buff.pillar_of_frost.up&cooldown.pillar_of_frost.remains_expected>15&(buff.cold_heart.stack>=10&buff.unholy_strength.up|buff.cold_heart.stack>=13)
actions.cold_heart+=/chains_of_ice,if=!talent.obliteration&!death_knight.runeforge.fallen_crusader&buff.cold_heart.stack>=10&!buff.pillar_of_frost.up&cooldown.pillar_of_frost.remains_expected>20
actions.cold_heart+=/chains_of_ice,if=talent.obliteration&!buff.pillar_of_frost.up&(buff.cold_heart.stack>=14&buff.unholy_strength.up|buff.cold_heart.stack>=19|cooldown.pillar_of_frost.remains_expected<3&buff.cold_heart.stack>=14)

# Cooldowns
actions.cooldowns=potion,if=(talent.pillar_of_frost&buff.pillar_of_frost.up|!talent.pillar_of_frost&buff.empower_rune_weapon.up|!talent.pillar_of_frost&!talent.empower_rune_weapon|active_enemies>=2&buff.pillar_of_frost.up)|fight_remains<25
actions.cooldowns+=/abomination_limb,if=talent.obliteration&!buff.pillar_of_frost.up&variable.sending_cds|fight_remains<15
actions.cooldowns+=/abomination_limb,if=!talent.obliteration&variable.sending_cds
actions.cooldowns+=/remorseless_winter,if=variable.rw_buffs&variable.sending_cds&(!talent.arctic_assault|!buff.pillar_of_frost.up)
actions.cooldowns+=/chill_streak,if=variable.sending_cds&(!talent.arctic_assault|!buff.pillar_of_frost.up)
actions.cooldowns+=/reapers_mark,target_if=first:!debuff.reapers_mark_debuff.up
actions.cooldowns+=/empower_rune_weapon,if=talent.obliteration&!talent.breath_of_sindragosa&buff.pillar_of_frost.up|fight_remains<20
actions.cooldowns+=/empower_rune_weapon,if=buff.breath_of_sindragosa.up&runic_power<variable.erw_breath_rp_trigger&rune<variable.erw_breath_rune_trigger|fight_remains<20
actions.cooldowns+=/empower_rune_weapon,if=!talent.breath_of_sindragosa&!talent.obliteration&!buff.empower_rune_weapon.up&rune<5&(cooldown.pillar_of_frost.remains_expected<7|buff.pillar_of_frost.up|!talent.pillar_of_frost)
actions.cooldowns+=/pillar_of_frost,if=talent.obliteration&!talent.breath_of_sindragosa&variable.sending_cds|fight_remains<12
actions.cooldowns+=/pillar_of_frost,if=talent.breath_of_sindragosa&variable.sending_cds&(buff.breath_of_sindragosa.up|cooldown.breath_of_sindragosa.remains>cooldown.pillar_of_frost.duration-20)|fight_remains<12
actions.cooldowns+=/pillar_of_frost,if=!talent.obliteration&!talent.breath_of_sindragosa&variable.sending_cds
actions.cooldowns+=/breath_of_sindragosa,if=!buff.breath_of_sindragosa.up&cooldown.empower_rune_weapon.remains_expected<15&runic_power>variable.breath_rp_threshold&(variable.adds_remain|variable.st_planning|fight_remains<30)|(time<10&rune<1)
actions.cooldowns+=/frostwyrms_fury,if=hero_tree.rider_of_the_apocalypse&talent.apocalypse_now&(!talent.breath_of_sindragosa&variable.sending_cds|buff.breath_of_sindragosa.up&buff.pillar_of_frost.up)|fight_remains<20
actions.cooldowns+=/frostwyrms_fury,if=!talent.apocalypse_now&active_enemies=1&(talent.pillar_of_frost&buff.pillar_of_frost.up&!talent.obliteration|!talent.pillar_of_frost)&(!raid_event.adds.exists|(raid_event.adds.in>15+raid_event.adds.duration|talent.absolute_zero&raid_event.adds.in>15+raid_event.adds.duration))|fight_remains<3
actions.cooldowns+=/frostwyrms_fury,if=!talent.apocalypse_now&active_enemies>=2&(talent.pillar_of_frost&buff.pillar_of_frost.up|raid_event.adds.exists&raid_event.adds.up&raid_event.adds.in>cooldown.pillar_of_frost.remains_expected-raid_event.adds.in-raid_event.adds.duration)
actions.cooldowns+=/frostwyrms_fury,if=!talent.apocalypse_now&talent.obliteration&(talent.pillar_of_frost&buff.pillar_of_frost.up&!variable.2h_check|!buff.pillar_of_frost.up&variable.2h_check&cooldown.pillar_of_frost.remains|!talent.pillar_of_frost)&((buff.pillar_of_frost.remains<gcd|buff.unholy_strength.up)&(debuff.razorice.stack=5|!death_knight.runeforge.razorice&!talent.glacial_advance))
actions.cooldowns+=/raise_dead
actions.cooldowns+=/soul_reaper,if=fight_remains>5&target.time_to_pct_35<5&target.time_to_pct_0>5&active_enemies<=2&(talent.obliteration&(buff.pillar_of_frost.up&!buff.killing_machine.react&rune>2|!buff.pillar_of_frost.up)|talent.breath_of_sindragosa&(buff.breath_of_sindragosa.up&runic_power>50|!buff.breath_of_sindragosa.up)|!talent.breath_of_sindragosa&!talent.obliteration)
actions.cooldowns+=/frostscythe,if=!buff.killing_machine.up&(!talent.arctic_assault|!buff.pillar_of_frost.up)
actions.cooldowns+=/any_dnd,if=!buff.death_and_decay.up&!buff.mograines_might.up&variable.adds_remain&(buff.pillar_of_frost.up&buff.killing_machine.react&(talent.enduring_strength|buff.pillar_of_frost.remains>5)|!buff.pillar_of_frost.up&(cooldown.death_and_decay.charges=2|cooldown.pillar_of_frost.remains>cooldown.death_and_decay.duration)|!talent.the_long_winter&cooldown.pillar_of_frost.remains<gcd.max*2|fight_remains<11)&(active_enemies>5|talent.cleaving_strikes&active_enemies>=2)

# High Priority Actions Use <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> while <a href='https://www.wowhead.com/spell=51271/pillar-of-frost'>Pillar of Frost</a> is up, as well as <a href='https://www.wowhead.com/spell=152279/breath-of-sindragosa'>Breath of Sindragosa</a> or on cooldown if <a href='https://www.wowhead.com/spell=51271/pillar-of-frost'>Pillar of Frost</a> and <a href='https://www.wowhead.com/spell=152279/breath-of-sindragosa'>Breath of Sindragosa</a> are not talented
actions.high_prio_actions=invoke_external_buff,name=power_infusion,if=(buff.pillar_of_frost.up|!talent.pillar_of_frost)&(talent.obliteration|talent.breath_of_sindragosa&buff.breath_of_sindragosa.up|!talent.breath_of_sindragosa&!talent.obliteration)
# Interrupt
actions.high_prio_actions+=/mind_freeze,if=target.debuff.casting.react
actions.high_prio_actions+=/antimagic_shell,if=runic_power.deficit>40&death_knight.first_ams_cast<time&(!talent.breath_of_sindragosa|talent.breath_of_sindragosa&cooldown.breath_of_sindragosa.remains>cooldown.antimagic_shell.duration)
# Maintain Frost Fever, Icy Talons and Unleashed Frenzy
actions.high_prio_actions+=/howling_blast,if=!dot.frost_fever.ticking&active_enemies>=2&((!talent.obliteration|talent.obliteration&(!cooldown.pillar_of_frost.ready|buff.pillar_of_frost.up&!buff.killing_machine.react))|(equipped.fyralath_the_dreamrender&!dot.mark_of_fyralath.ticking))
actions.high_prio_actions+=/glacial_advance,if=variable.ga_priority&variable.rp_buffs&talent.obliteration&talent.breath_of_sindragosa&!buff.pillar_of_frost.up&!buff.breath_of_sindragosa.up&cooldown.breath_of_sindragosa.remains>variable.breath_pooling_time
actions.high_prio_actions+=/glacial_advance,if=variable.ga_priority&variable.rp_buffs&talent.breath_of_sindragosa&!buff.breath_of_sindragosa.up&cooldown.breath_of_sindragosa.remains>variable.breath_pooling_time
actions.high_prio_actions+=/glacial_advance,if=variable.ga_priority&variable.rp_buffs&!talent.breath_of_sindragosa&talent.obliteration&!buff.pillar_of_frost.up&!talent.shattered_frost
actions.high_prio_actions+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=active_enemies=1&variable.rp_buffs&talent.obliteration&talent.breath_of_sindragosa&!buff.pillar_of_frost.up&!buff.breath_of_sindragosa.up&cooldown.breath_of_sindragosa.remains>variable.breath_pooling_time
actions.high_prio_actions+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=active_enemies=1&variable.rp_buffs&talent.breath_of_sindragosa&!buff.breath_of_sindragosa.up&cooldown.breath_of_sindragosa.remains>variable.breath_pooling_time
actions.high_prio_actions+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=active_enemies=1&variable.rp_buffs&!talent.breath_of_sindragosa&talent.obliteration&!buff.pillar_of_frost.up

# Obliteration Active Rotation
actions.obliteration=howling_blast,if=buff.killing_machine.stack<2&buff.pillar_of_frost.remains<gcd&variable.rime_buffs
actions.obliteration+=/glacial_advance,if=buff.killing_machine.react<2&buff.pillar_of_frost.remains<gcd&!buff.death_and_decay.up&variable.ga_priority
actions.obliteration+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=buff.killing_machine.react<2&buff.pillar_of_frost.remains<gcd&!buff.death_and_decay.up
actions.obliteration+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=debuff.razorice.stack=5&talent.shattering_blade&talent.a_feast_of_souls&buff.a_feast_of_souls.up&!talent.arctic_assault
actions.obliteration+=/obliterate,target_if=max:(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=buff.killing_machine.react
actions.obliteration+=/howling_blast,if=!buff.killing_machine.react&(!dot.frost_fever.ticking)
actions.obliteration+=/glacial_advance,target_if=max:(debuff.razorice.stack),if=(variable.ga_priority|debuff.razorice.stack<5)&(!death_knight.runeforge.razorice&(debuff.razorice.stack<5|debuff.razorice.remains<gcd*3)|((variable.rp_buffs|rune<2)&active_enemies>1))
actions.obliteration+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=(rune<2|variable.rp_buffs|debuff.razorice.stack=5&talent.shattering_blade)&!variable.pooling_runic_power&(!talent.glacial_advance|active_enemies=1|talent.shattered_frost)
actions.obliteration+=/howling_blast,if=buff.rime.react
actions.obliteration+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=!variable.pooling_runic_power&(!talent.glacial_advance|active_enemies=1|talent.shattered_frost)
actions.obliteration+=/glacial_advance,target_if=max:(debuff.razorice.stack),if=!variable.pooling_runic_power&variable.ga_priority
actions.obliteration+=/frost_strike,target_if=max:((talent.shattering_blade&debuff.razorice.stack=5)*5)+(debuff.razorice.stack+1)%(debuff.razorice.remains+1)*death_knight.runeforge.razorice,if=!variable.pooling_runic_power
actions.obliteration+=/horn_of_winter,if=rune<3
actions.obliteration+=/arcane_torrent,if=rune<1&runic_power<30
actions.obliteration+=/howling_blast,if=!buff.killing_machine.up

# Racial Abilities
actions.racials=blood_fury,if=variable.cooldown_check
actions.racials+=/berserking,if=variable.cooldown_check
actions.racials+=/arcane_pulse,if=variable.cooldown_check
actions.racials+=/lights_judgment,if=variable.cooldown_check
actions.racials+=/ancestral_call,if=variable.cooldown_check
actions.racials+=/fireblood,if=variable.cooldown_check
actions.racials+=/bag_of_tricks,if=talent.obliteration&!buff.pillar_of_frost.up&buff.unholy_strength.up
actions.racials+=/bag_of_tricks,if=!talent.obliteration&buff.pillar_of_frost.up&(buff.unholy_strength.up&buff.unholy_strength.remains<gcd*3|buff.pillar_of_frost.remains<gcd*3)

# Single Target Rotation
actions.single_target=frost_strike,if=debuff.razorice.stack=5&talent.shattering_blade&talent.a_feast_of_souls&buff.a_feast_of_souls.up
actions.single_target+=/obliterate,if=buff.killing_machine.react&variable.static_obliterate_buffs
actions.single_target+=/frost_strike,if=(debuff.razorice.stack=5&talent.shattering_blade)|(buff.killing_machine.up&rune<2&!talent.icebreaker)
actions.single_target+=/howling_blast,if=variable.rime_buffs
actions.single_target+=/obliterate,if=buff.killing_machine.react&(!variable.pooling_runes|buff.killing_machine.react=2)
actions.single_target+=/glacial_advance,if=!variable.pooling_runic_power&!death_knight.runeforge.razorice&(debuff.razorice.stack<5|debuff.razorice.remains<gcd*3)
actions.single_target+=/frost_strike,if=!variable.pooling_runic_power&(variable.rp_buffs|(!talent.shattering_blade&runic_power.deficit<20)|debuff.razorice.stack=5&talent.shattering_blade)
actions.single_target+=/howling_blast,if=buff.rime.react
actions.single_target+=/frost_strike,if=!variable.pooling_runic_power&!(variable.2h_check|talent.shattering_blade)
actions.single_target+=/obliterate,if=!variable.pooling_runes
actions.single_target+=/frost_strike,if=!variable.pooling_runic_power
actions.single_target+=/howling_blast,if=!dot.frost_fever.ticking
actions.single_target+=/any_dnd,if=talent.breath_of_sindragosa&!buff.breath_of_sindragosa.up&!cooldown.breath_of_sindragosa.remains&rune<2&!buff.death_and_decay.up
actions.single_target+=/horn_of_winter,if=rune<2&runic_power.deficit>25&(!talent.breath_of_sindragosa|cooldown.breath_of_sindragosa.remains>cooldown.horn_of_winter.duration-15)
actions.single_target+=/arcane_torrent,if=!talent.breath_of_sindragosa&runic_power.deficit>20

# Trinkets
actions.trinkets=use_item,name=fyralath_the_dreamrender,if=dot.mark_of_fyralath.ticking&!buff.pillar_of_frost.up&!buff.empower_rune_weapon.up&!buff.death_and_decay.up&(active_enemies<2|dot.frost_fever.ticking)
actions.trinkets+=/use_item,use_off_gcd=1,name=algethar_puzzle_box,if=!buff.pillar_of_frost.up&cooldown.pillar_of_frost.remains<2&(!talent.breath_of_sindragosa|runic_power>60&(buff.breath_of_sindragosa.up|cooldown.breath_of_sindragosa.remains<2))
# Trinkets The trinket with the highest estimated value, will be used first and paired with Pillar of Frost.
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=variable.trinket_1_buffs&!variable.trinket_1_manual&(!talent.breath_of_sindragosa&buff.pillar_of_frost.remains>10|talent.breath_of_sindragosa)&(!buff.pillar_of_frost.up&trinket.1.cast_time>0|!trinket.1.cast_time>0)&(buff.breath_of_sindragosa.up&buff.pillar_of_frost.up|!talent.breath_of_sindragosa)&(variable.trinket_2_exclude|!trinket.2.has_cooldown|trinket.2.cooldown.remains|variable.trinket_priority=1)|trinket.1.proc.any_dps.duration>=fight_remains
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=variable.trinket_2_buffs&!variable.trinket_2_manual&(!talent.breath_of_sindragosa&buff.pillar_of_frost.remains>10|talent.breath_of_sindragosa)&(!buff.pillar_of_frost.up&trinket.2.cast_time>0|!trinket.2.cast_time>0)&(buff.breath_of_sindragosa.up&buff.pillar_of_frost.up|!talent.breath_of_sindragosa)&(variable.trinket_1_exclude|!trinket.1.has_cooldown|trinket.1.cooldown.remains|variable.trinket_priority=2)|trinket.2.proc.any_dps.duration>=fight_remains
# If only one on use trinket provides a buff, use the other on cooldown. Or if neither trinket provides a buff, use both on cooldown.
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=!variable.trinket_1_buffs&!variable.trinket_1_manual&((variable.damage_trinket_priority=1|trinket.2.cooldown.remains)|(trinket.1.cast_time>0&!buff.pillar_of_frost.up|!trinket.1.cast_time>0&cooldown.pillar_of_frost.remains>20)|talent.pillar_of_frost&cooldown.pillar_of_frost.remains_expected>20|!talent.pillar_of_frost)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=!variable.trinket_2_buffs&!variable.trinket_2_manual&((variable.damage_trinket_priority=2|trinket.1.cooldown.remains)|(trinket.2.cast_time>0&!buff.pillar_of_frost.up|!trinket.2.cast_time>0&cooldown.pillar_of_frost.remains>20)|talent.pillar_of_frost&cooldown.pillar_of_frost.remains_expected>20|!talent.pillar_of_frost)
actions.trinkets+=/use_item,use_off_gcd=1,slot=main_hand,if=!equipped.fyralath_the_dreamrender&(!variable.trinket_1_buffs|trinket.1.cooldown.remains)&(!variable.trinket_2_buffs|trinket.2.cooldown.remains)

# Variables
actions.variables=variable,name=st_planning,value=active_enemies=1&(raid_event.adds.in>15|!raid_event.adds.exists)
actions.variables+=/variable,name=adds_remain,value=active_enemies>=2&(!raid_event.adds.exists|raid_event.adds.exists&raid_event.adds.remains>5)
actions.variables+=/variable,name=sending_cds,value=(variable.st_planning|variable.adds_remain)
actions.variables+=/variable,name=rime_buffs,value=buff.rime.react&(variable.static_rime_buffs|talent.avalanche&!talent.arctic_assault&debuff.razorice.stack<5)
actions.variables+=/variable,name=rp_buffs,value=talent.unleashed_frenzy&(buff.unleashed_frenzy.remains<gcd.max*3|buff.unleashed_frenzy.stack<3)|talent.icy_talons&(buff.icy_talons.remains<gcd.max*3|buff.icy_talons.stack<(3+(2*talent.smothering_offense)+(2*talent.dark_talons)))
actions.variables+=/variable,name=cooldown_check,value=talent.pillar_of_frost&buff.pillar_of_frost.up&(talent.obliteration&buff.pillar_of_frost.remains>10|!talent.obliteration)|!talent.pillar_of_frost&buff.empower_rune_weapon.up|!talent.pillar_of_frost&!talent.empower_rune_weapon|active_enemies>=2&buff.pillar_of_frost.up
# Formulaic approach to determine the time before these abilities come off cooldown that the simulation should star to pool resources. Capped at 15s in the run_action_list call.
actions.variables+=/variable,name=oblit_pooling_time,op=setif,value=((cooldown.pillar_of_frost.remains_expected+1)%gcd.max)%((rune+3)*(runic_power+5))*100,value_else=3,condition=runic_power<35&rune<2&cooldown.pillar_of_frost.remains_expected<10
actions.variables+=/variable,name=breath_pooling_time,op=setif,value=((cooldown.breath_of_sindragosa.remains+1)%gcd.max)%((rune+1)*(runic_power+20))*100,value_else=2,condition=runic_power.deficit>10&cooldown.breath_of_sindragosa.remains<10
actions.variables+=/variable,name=pooling_runes,value=rune<variable.oblit_rune_pooling&talent.obliteration&(!talent.breath_of_sindragosa|cooldown.breath_of_sindragosa.remains)&cooldown.pillar_of_frost.remains_expected<variable.oblit_pooling_time
actions.variables+=/variable,name=pooling_runic_power,value=talent.breath_of_sindragosa&cooldown.breath_of_sindragosa.remains<variable.breath_pooling_time|talent.obliteration&runic_power<35&cooldown.pillar_of_frost.remains_expected<variable.oblit_pooling_time
actions.variables+=/variable,name=ga_priority,value=(talent.shattered_frost&active_enemies>=2)|(!talent.shattered_frost&talent.shattering_blade&active_enemies>=4)|(!talent.shattered_frost&!talent.shattering_blade&active_enemies>=2)
actions.variables+=/variable,name=breath_dying,value=runic_power<variable.breath_rp_cost*2&rune.time_to_2>runic_power%variable.breath_rp_cost

```

# ActionPriorityLists\deathknight_blood.simc

```simc

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
actions.precombat+=/food
actions.precombat+=/augmentation
actions.precombat+=/snapshot_stats
actions.precombat+=/variable,name=trinket_1_buffs,value=trinket.1.has_use_buff|(trinket.1.has_buff.strength|trinket.1.has_buff.mastery|trinket.1.has_buff.versatility|trinket.1.has_buff.haste|trinket.1.has_buff.crit)|trinket.1.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_2_buffs,value=trinket.2.has_use_buff|(trinket.2.has_buff.strength|trinket.2.has_buff.mastery|trinket.2.has_buff.versatility|trinket.2.has_buff.haste|trinket.2.has_buff.crit)|trinket.2.is.mirror_of_fractured_tomorrows
actions.precombat+=/variable,name=trinket_1_exclude,value=trinket.1.is.ruby_whelp_shell|trinket.1.is.whispering_incarnate_icon
actions.precombat+=/variable,name=trinket_2_exclude,value=trinket.2.is.ruby_whelp_shell|trinket.2.is.whispering_incarnate_icon
actions.precombat+=/variable,name=damage_trinket_priority,op=setif,value=2,value_else=1,condition=!variable.trinket_2_buffs&trinket.2.ilvl>=trinket.1.ilvl|variable.trinket_1_buffs

# Executed every time the actor is available.
actions=auto_attack
actions+=/variable,name=death_strike_dump_amount,value=65
actions+=/variable,name=bone_shield_refresh_value,value=4,op=setif,condition=talent.consumption.enabled|talent.blooddrinker.enabled,value_else=5
actions+=/mind_freeze,if=target.debuff.casting.react
# Use <a href='https://www.wowhead.com/spell=10060/power-infusion'>Power Infusion</a> while <a href='https://www.wowhead.com/spell=49028/dancing-rune-weapon'>Dancing Rune Weapon</a> is up, or on cooldown if <a href='https://www.wowhead.com/spell=49028/dancing-rune-weapon'>Dancing Rune Weapon</a> is not talented
actions+=/invoke_external_buff,name=power_infusion,if=buff.dancing_rune_weapon.up|!talent.dancing_rune_weapon
actions+=/potion,if=buff.dancing_rune_weapon.up
actions+=/call_action_list,name=trinkets
actions+=/raise_dead
actions+=/reapers_mark
actions+=/icebound_fortitude,if=!(buff.dancing_rune_weapon.up|buff.vampiric_blood.up)&(target.cooldown.pause_action.remains>=8|target.cooldown.pause_action.duration>0)
actions+=/vampiric_blood,if=!(buff.dancing_rune_weapon.up|buff.icebound_fortitude.up|buff.vampiric_blood.up)&(target.cooldown.pause_action.remains>=13|target.cooldown.pause_action.duration>0)
actions+=/deaths_caress,if=!buff.bone_shield.up
actions+=/death_and_decay,if=!death_and_decay.ticking&(talent.unholy_ground|talent.sanguine_ground|spell_targets.death_and_decay>3|buff.crimson_scourge.up)
actions+=/death_strike,if=buff.coagulopathy.remains<=gcd|buff.icy_talons.remains<=gcd|runic_power>=variable.death_strike_dump_amount|runic_power.deficit<=variable.heart_strike_rp|target.time_to_die<10
actions+=/blooddrinker,if=!buff.dancing_rune_weapon.up
actions+=/call_action_list,name=racials
actions+=/sacrificial_pact,if=!buff.dancing_rune_weapon.up&(pet.ghoul.remains<2|target.time_to_die<gcd)
actions+=/blood_tap,if=(rune<=2&rune.time_to_4>gcd&charges_fractional>=1.8)|rune.time_to_3>gcd
actions+=/gorefiends_grasp,if=talent.tightening_grasp.enabled
actions+=/empower_rune_weapon,if=rune<6&runic_power.deficit>5
actions+=/abomination_limb
actions+=/dancing_rune_weapon,if=!buff.dancing_rune_weapon.up
actions+=/run_action_list,name=drw_up,if=buff.dancing_rune_weapon.up
actions+=/call_action_list,name=standard

actions.drw_up=blood_boil,if=!dot.blood_plague.ticking
actions.drw_up+=/tombstone,if=buff.bone_shield.stack>5&rune>=2&runic_power.deficit>=30&!talent.shattering_bone|(talent.shattering_bone.enabled&death_and_decay.ticking)
actions.drw_up+=/death_strike,if=buff.coagulopathy.remains<=gcd|buff.icy_talons.remains<=gcd
actions.drw_up+=/marrowrend,if=(buff.bone_shield.remains<=4|buff.bone_shield.stack<variable.bone_shield_refresh_value)&runic_power.deficit>20
actions.drw_up+=/soul_reaper,if=active_enemies=1&target.time_to_pct_35<5&target.time_to_die>(dot.soul_reaper.remains+5)
actions.drw_up+=/soul_reaper,target_if=min:dot.soul_reaper.remains,if=target.time_to_pct_35<5&active_enemies>=2&target.time_to_die>(dot.soul_reaper.remains+5)
actions.drw_up+=/death_and_decay,if=!death_and_decay.ticking&(talent.sanguine_ground|talent.unholy_ground)
actions.drw_up+=/blood_boil,if=spell_targets.blood_boil>2&charges_fractional>=1.1
actions.drw_up+=/variable,name=heart_strike_rp_drw,value=(25+spell_targets.heart_strike*talent.heartbreaker.enabled*2)
actions.drw_up+=/death_strike,if=runic_power.deficit<=variable.heart_strike_rp_drw|runic_power>=variable.death_strike_dump_amount
actions.drw_up+=/consumption
actions.drw_up+=/blood_boil,if=charges_fractional>=1.1&buff.hemostasis.stack<5
actions.drw_up+=/heart_strike,if=rune.time_to_2<gcd|runic_power.deficit>=variable.heart_strike_rp_drw

actions.racials=blood_fury,if=cooldown.dancing_rune_weapon.ready&(!cooldown.blooddrinker.ready|!talent.blooddrinker.enabled)
actions.racials+=/berserking
actions.racials+=/arcane_pulse,if=active_enemies>=2|rune<1&runic_power.deficit>60
actions.racials+=/lights_judgment,if=buff.unholy_strength.up
actions.racials+=/ancestral_call
actions.racials+=/fireblood
actions.racials+=/bag_of_tricks
actions.racials+=/arcane_torrent,if=runic_power.deficit>20

actions.standard=tombstone,if=buff.bone_shield.stack>5&rune>=2&runic_power.deficit>=30&!talent.shattering_bone|(talent.shattering_bone.enabled&death_and_decay.ticking)&cooldown.dancing_rune_weapon.remains>=25
actions.standard+=/variable,name=heart_strike_rp,value=(10+spell_targets.heart_strike*talent.heartbreaker.enabled*2)
actions.standard+=/death_strike,if=buff.coagulopathy.remains<=gcd|buff.icy_talons.remains<=gcd|runic_power>=variable.death_strike_dump_amount|runic_power.deficit<=variable.heart_strike_rp|target.time_to_die<10
actions.standard+=/deaths_caress,if=(buff.bone_shield.remains<=4|(buff.bone_shield.stack<variable.bone_shield_refresh_value+1))&runic_power.deficit>10&!(talent.insatiable_blade&cooldown.dancing_rune_weapon.remains<buff.bone_shield.remains)&!talent.consumption.enabled&!talent.blooddrinker.enabled&rune.time_to_3>gcd
actions.standard+=/marrowrend,if=(buff.bone_shield.remains<=4|buff.bone_shield.stack<variable.bone_shield_refresh_value)&runic_power.deficit>20&!(talent.insatiable_blade&cooldown.dancing_rune_weapon.remains<buff.bone_shield.remains)
actions.standard+=/consumption
actions.standard+=/soul_reaper,if=active_enemies=1&target.time_to_pct_35<5&target.time_to_die>(dot.soul_reaper.remains+5)
actions.standard+=/soul_reaper,target_if=min:dot.soul_reaper.remains,if=target.time_to_pct_35<5&active_enemies>=2&target.time_to_die>(dot.soul_reaper.remains+5)
actions.standard+=/bonestorm,if=buff.bone_shield.stack>=5
actions.standard+=/blood_boil,if=charges_fractional>=1.8&(buff.hemostasis.stack<=(5-spell_targets.blood_boil)|spell_targets.blood_boil>2)
actions.standard+=/heart_strike,if=rune.time_to_4<gcd
actions.standard+=/blood_boil,if=charges_fractional>=1.1
actions.standard+=/heart_strike,if=(rune>1&(rune.time_to_3<gcd|buff.bone_shield.stack>7))

# Trinkets
actions.trinkets=use_item,name=fyralath_the_dreamrender,if=dot.mark_of_fyralath.ticking
# Prioritize damage dealing on use trinkets over trinkets that give buffs
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=!variable.trinket_1_buffs&(variable.damage_trinket_priority=1|trinket.2.cooldown.remains|!trinket.2.has_cooldown)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=!variable.trinket_2_buffs&(variable.damage_trinket_priority=2|trinket.1.cooldown.remains|!trinket.1.has_cooldown)
actions.trinkets+=/use_item,use_off_gcd=1,slot=main_hand,if=!equipped.fyralath_the_dreamrender&(variable.trinket_1_buffs|trinket.1.cooldown.remains)&(variable.trinket_2_buffs|trinket.2.cooldown.remains)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket1,if=variable.trinket_1_buffs&(buff.dancing_rune_weapon.up|!talent.dancing_rune_weapon|cooldown.dancing_rune_weapon.remains>20)&(variable.trinket_2_exclude|trinket.2.cooldown.remains|!trinket.2.has_cooldown|variable.trinket_2_buffs)
actions.trinkets+=/use_item,use_off_gcd=1,slot=trinket2,if=variable.trinket_2_buffs&(buff.dancing_rune_weapon.up|!talent.dancing_rune_weapon|cooldown.dancing_rune_weapon.remains>20)&(variable.trinket_1_exclude|trinket.1.cooldown.remains|!trinket.1.has_cooldown|variable.trinket_1_buffs)

```

