# This file was generated!
import enum

import construct

from mercury_engine_data_structures import common_types
from mercury_engine_data_structures.object import Object
from mercury_engine_data_structures.pointer_set import PointerSet
from mercury_engine_data_structures.formats.property_enum import PropertyEnum, PropertyEnumUnsafe
from mercury_engine_data_structures.construct_extensions.enum import StrictEnum

Pointer_CAcidBlobsLaunchPattern = PointerSet("CAcidBlobsLaunchPattern")
Pointer_CActor = PointerSet("CActor")
Pointer_CActorComponent = PointerSet("CActorComponent")
Pointer_CAttackPreset = PointerSet("CAttackPreset")
Pointer_CBarelyFrozenIceInfo = PointerSet("CBarelyFrozenIceInfo")
Pointer_CBlackboard_CSection = PointerSet("CBlackboard::CSection")
Pointer_CBouncingCreaturesLaunchPattern = PointerSet("CBouncingCreaturesLaunchPattern")
Pointer_CCentralUnitWeightedEdges = PointerSet("CCentralUnitWeightedEdges")
Pointer_CChozoRobotSoldierCannonShotPattern = PointerSet("CChozoRobotSoldierCannonShotPattern")
Pointer_CCooldownXBossFireWallDef = PointerSet("CCooldownXBossFireWallDef")
Pointer_CCooldownXBossLavaCarpetDef = PointerSet("CCooldownXBossLavaCarpetDef")
Pointer_CCooldownXBossLavaDropsDef = PointerSet("CCooldownXBossLavaDropsDef")
Pointer_CCutSceneDef = PointerSet("CCutSceneDef")
Pointer_CEmmyAutoForbiddenEdgesDef = PointerSet("CEmmyAutoForbiddenEdgesDef")
Pointer_CEmmyAutoGlobalSmartLinkDef = PointerSet("CEmmyAutoGlobalSmartLinkDef")
Pointer_CEmmyOverrideDeathPositionDef = PointerSet("CEmmyOverrideDeathPositionDef")
Pointer_CEnemyPreset = PointerSet("CEnemyPreset")
Pointer_CEnvironmentData_SAmbient = PointerSet("CEnvironmentData::SAmbient")
Pointer_CEnvironmentData_SBloom = PointerSet("CEnvironmentData::SBloom")
Pointer_CEnvironmentData_SCubeMap = PointerSet("CEnvironmentData::SCubeMap")
Pointer_CEnvironmentData_SDepthTint = PointerSet("CEnvironmentData::SDepthTint")
Pointer_CEnvironmentData_SFog = PointerSet("CEnvironmentData::SFog")
Pointer_CEnvironmentData_SHemisphericalLight = PointerSet("CEnvironmentData::SHemisphericalLight")
Pointer_CEnvironmentData_SIBLAttenuation = PointerSet("CEnvironmentData::SIBLAttenuation")
Pointer_CEnvironmentData_SMaterialTint = PointerSet("CEnvironmentData::SMaterialTint")
Pointer_CEnvironmentData_SPlayerLight = PointerSet("CEnvironmentData::SPlayerLight")
Pointer_CEnvironmentData_SSSAO = PointerSet("CEnvironmentData::SSSAO")
Pointer_CEnvironmentData_SToneMapping = PointerSet("CEnvironmentData::SToneMapping")
Pointer_CEnvironmentData_SVerticalFog = PointerSet("CEnvironmentData::SVerticalFog")
Pointer_CEnvironmentManager = PointerSet("CEnvironmentManager")
Pointer_CEnvironmentMusicPresets = PointerSet("CEnvironmentMusicPresets")
Pointer_CEnvironmentSoundPresets = PointerSet("CEnvironmentSoundPresets")
Pointer_CEnvironmentVisualPresets = PointerSet("CEnvironmentVisualPresets")
Pointer_CKraidSpinningNailsDef = PointerSet("CKraidSpinningNailsDef")
Pointer_CLightManager = PointerSet("CLightManager")
Pointer_CLogicCamera = PointerSet("CLogicCamera")
Pointer_CPattern = PointerSet("CPattern")
Pointer_CPlaythrough_SCheckpointData = PointerSet("CPlaythrough::SCheckpointData")
Pointer_CPlaythroughDef_SCheckpointDef = PointerSet("CPlaythroughDef::SCheckpointDef")
Pointer_CPolypFallPattern = PointerSet("CPolypFallPattern")
Pointer_CScenario = PointerSet("CScenario")
Pointer_CShootDCBones = PointerSet("CShootDCBones")
Pointer_CShotLaunchConfig = PointerSet("CShotLaunchConfig")
Pointer_CShotManager = PointerSet("CShotManager")
Pointer_CSubAreaManager = PointerSet("CSubAreaManager")
Pointer_CSubareaCharclassGroup = PointerSet("CSubareaCharclassGroup")
Pointer_CSubareaInfo = PointerSet("CSubareaInfo")
Pointer_CSubareaSetup = PointerSet("CSubareaSetup")
Pointer_CTentacle = PointerSet("CTentacle")
Pointer_CTriggerComponent_SActivationCondition = PointerSet("CTriggerComponent::SActivationCondition")
Pointer_CTriggerLogicAction = PointerSet("CTriggerLogicAction")
Pointer_CXParasiteBehavior = PointerSet("CXParasiteBehavior")
Pointer_GUI_CDisplayObject = PointerSet("GUI::CDisplayObject")
Pointer_GUI_CDisplayObjectAnimationDef = PointerSet("GUI::CDisplayObjectAnimationDef")
Pointer_GUI_CDisplayObjectDef = PointerSet("GUI::CDisplayObjectDef")
Pointer_GUI_CDisplayObjectStateDef = PointerSet("GUI::CDisplayObjectStateDef")
Pointer_GUI_CSkin = PointerSet("GUI::CSkin")
Pointer_GUI_CSpriteSheet = PointerSet("GUI::CSpriteSheet")
Pointer_GUI_CSpriteSheetItem = PointerSet("GUI::CSpriteSheetItem")
Pointer_GUI_CTrackSet = PointerSet("GUI::CTrackSet")
Pointer_GUI_IDisplayObjectTrack = PointerSet("GUI::IDisplayObjectTrack")
Pointer_animtree_CAnimTreeElementDef = PointerSet("animtree::CAnimTreeElementDef")
Pointer_base_global_CFilePathStrId = PointerSet("base::global::CFilePathStrId")
Pointer_base_global_CRntFile = PointerSet("base::global::CRntFile")
Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_ = PointerSet("base::global::CRntSmallDictionary<base::global::CStrId, CActorComponent*>")
Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SAmbientTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SBloomTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SCubeMapTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SDepthTintTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SFogTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SHemisphericalLightTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SIBLAttenuationTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SMaterialTintTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SPlayerLightTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SSSAOTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SToneMappingTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SVerticalFogTransition>")
Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__ = PointerSet("base::global::CRntVector<std::unique_ptr<CSubareaCharclassGroup>>")
Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__ = PointerSet("base::global::CRntVector<std::unique_ptr<CSubareaSetup>>")
Pointer_base_spatial_CPolygon2D = PointerSet("base::spatial::CPolygon2D")
Pointer_base_tunable_CTunable = PointerSet("base::tunable::CTunable")
Pointer_engine_scene_CScene = PointerSet("engine::scene::CScene")
Pointer_engine_scene_CSceneSlot = PointerSet("engine::scene::CSceneSlot")
Pointer_game_logic_collision_CCollider = PointerSet("game::logic::collision::CCollider")
Pointer_game_logic_collision_CShape = PointerSet("game::logic::collision::CShape")
Pointer_querysystem_CEvaluator = PointerSet("querysystem::CEvaluator")
Pointer_querysystem_CFilter = PointerSet("querysystem::CFilter")
Pointer_sound_CAudioPresets = PointerSet("sound::CAudioPresets")
Pointer_sound_CMusicManager = PointerSet("sound::CMusicManager")
Pointer_sound_CSoundEventsDef_SSoundEventsRule = PointerSet("sound::CSoundEventsDef::SSoundEventsRule")
Pointer_sound_CSoundEventsDef_SSoundEventsSelector = PointerSet("sound::CSoundEventsDef::SSoundEventsSelector")
Pointer_sound_CSoundManager = PointerSet("sound::CSoundManager")


CActionInstance = Object(CActionInstanceFields := {})

CAIAction = Object(CAIActionFields := CActionInstanceFields)

CAIAimAction = Object(CAIActionFields)

CAIAimAngToFrameAction = Object(CAIActionFields)

base_core_CBaseObject = Object(base_core_CBaseObjectFields := {})

CGameObject = Object(CGameObjectFields := base_core_CBaseObjectFields)

CActorComponent = Object(CActorComponentFields := CGameObjectFields)

CComponent = Object(CComponentFields := {
    **CActorComponentFields,
    "bEnabled": construct.Flag,
    "bWantsEnabled": construct.Flag,
    "bUseDefaultValues": construct.Flag,
})

CAttackComponent = Object(CAttackComponentFields := {
    **CComponentFields,
    "bRotateToDamagedEntity": construct.Flag,
    "fRotateToDamagedEntityMaxAngle": common_types.Float,
    "fRotateToDamagedEntityMinAngle": common_types.Float,
})

CAIAttackComponent = Object(CAIAttackComponentFields := CAttackComponentFields)


class IPath_EType(enum.IntEnum):
    NONE = 0
    Once = 1
    PingPong = 2
    Loop = 3
    Invalid = 2147483647


construct_IPath_EType = StrictEnum(IPath_EType)

SFallBackPath = Object({
    "wpPath": common_types.StrId,
    "ePathType": construct_IPath_EType,
})

base_global_CRntVector_SFallBackPath_ = common_types.make_vector(SFallBackPath)

CAIComponent = Object(CAIComponentFields := {
    **CComponentFields,
    "sForcedAttack": common_types.StrId,
    "iForcedAttackPreset": common_types.Int,
    "fTimeSinceTargetLastSeen": common_types.Float,
    "fTimeSinceLastDamage": common_types.Float,
    "fTimeSinceLastFrozen": common_types.Float,
    "fPathLeftCut": common_types.Float,
    "fPathRightCut": common_types.Float,
    "fCutDistanceClockwise": common_types.Float,
    "fCutDistanceCounterClockwise": common_types.Float,
    "wpPathToFollow": common_types.StrId,
    "tFallbackPaths": base_global_CRntVector_SFallBackPath_,
    "ePathType": construct_IPath_EType,
    "bIndividualRequiresActivationPerception": construct.Flag,
    "bIgnoreAttack": construct.Flag,
    "bInBlindAttack": construct.Flag,
})


class CAIComponent_PathLimitSelectionMode(enum.IntEnum):
    FarthestFromTarget = 0
    FarthestFromEntity = 1
    InCurrentDir = 2
    InOppositeDir2Target = 3
    InOppositePathDir2Target = 4
    InDir2Target = 5
    InPathDir2Target = 6
    Invalid = 2147483647


construct_CAIComponent_PathLimitSelectionMode = StrictEnum(CAIComponent_PathLimitSelectionMode)

CAIGotoPointNavigationState_STarget = Object(CAIGotoPointNavigationState_STargetFields := {})

CAIGotoPointNavigationState_SPointTarget = Object(CAIGotoPointNavigationState_SPointTargetFields := CAIGotoPointNavigationState_STargetFields)

CAIGotoPointNavigationState_SEntityTarget = Object(CAIGotoPointNavigationState_SPointTargetFields)

CGrapplePointComponent = Object(CGrapplePointComponentFields := CComponentFields)

CPullableGrapplePointComponent = Object(CPullableGrapplePointComponentFields := CGrapplePointComponentFields)

CAIGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

base_tunable_CTunable = Object(base_tunable_CTunableFields := {
    **base_core_CBaseObjectFields,
    "sName": common_types.StrId,
})


class CAIManager_EBumpMode(enum.IntEnum):
    EnemyPos2Hit = 0
    SamusRay2Enemy = 1
    SamusShape2Enemy = 2
    SamusShape2EnemyAvg = 3
    Invalid = 2147483647


construct_CAIManager_EBumpMode = StrictEnum(CAIManager_EBumpMode)

CAIManager_CTunableAIManager = Object({
    **base_tunable_CTunableFields,
    "iIgnorePlayerMode": common_types.Int,
    "bShowBossLifebar": construct.Flag,
    "eBumpMode": construct_CAIManager_EBumpMode,
    "bShowEnemyLife": construct.Flag,
    "bShowEnemyDamage": construct.Flag,
    "bShowPlayerDamage": construct.Flag,
    "fDistanceToDestroyProjectile": common_types.Float,
})


class CAIManager_EAIGroup(enum.IntEnum):
    Emmy = 0
    Invalid = 2147483647


construct_CAIManager_EAIGroup = StrictEnum(CAIManager_EAIGroup)

CAINavigationComponent = Object(CComponentFields)

CAINavigationState_SParams = Object({})

CAISmartObjectComponent = Object({
    **CComponentFields,
    "fResetTime": common_types.Float,
    "fUseTime": common_types.Float,
    "iSpawnDirection": common_types.Int,
})

CAbility = Object(CAbilityFields := CGameObjectFields)

CAbilityComponent = Object({
    **CComponentFields,
    "bAccurateAiming": construct.Flag,
    "sBlockSyncFX": common_types.StrId,
})

CAbilityComponent_CTunableAbilityComponent = Object({
    **base_tunable_CTunableFields,
    "fSynchronizedBlockTime": common_types.Float,
    "fSpecialEnergyConsumedOnBlock": common_types.Float,
    "fMinTimeBetweenMeleeActions": common_types.Float,
    "fActivationHoldToStartDeactivateAll": common_types.Float,
    "fActivationHoldToCompleteDeactivateAll": common_types.Float,
    "fDashMeleeAutoLockOnMoveLockedTime": common_types.Float,
    "bAllMeleeAutoLockOn": construct.Flag,
    "fDashMeleeExtraDistanceToEnemies": common_types.Float,
    "fDashMeleePowerSuitDamage": common_types.Float,
    "fDashMeleeVariaSuitDamage": common_types.Float,
    "fDashMeleeGravitySuitDamage": common_types.Float,
    "bStunnedEnemiesLoseCollision": construct.Flag,
})

CAbilityEnergyWave = Object(CAbilityFields)

CAbilityEnergyWave_CTunableAbilityEnergyWave = Object({
    **base_tunable_CTunableFields,
    "fWeaponBoostDamageMult_emmy": common_types.Float,
    "fWeaponBoostDamageMult_emmycave": common_types.Float,
    "fSpecialBurstWidth": common_types.Float,
    "fSpecialRocketTimeActivate": common_types.Float,
    "fSpecialRocketSpeed": common_types.Float,
    "bSpecialRocketUseInitialAcceleration": construct.Flag,
})

CAbilityGhostAura = Object(CAbilityFields)

CAbilityGhostAura_CTunableAbilityGhostAura = Object({
    **base_tunable_CTunableFields,
    "fMinDistance": common_types.Float,
    "fMaxObstacleDistanceHorizontal": common_types.Float,
    "fMaxObstacleDistanceDiagonal": common_types.Float,
    "fMaxObstacleDistanceVertical": common_types.Float,
    "fExtraDistanceToScenario": common_types.Float,
    "fElectricFXTime": common_types.Float,
    "fChainFXTime": common_types.Float,
    "iNumFadingStepsPerFrame": common_types.Int,
    "fTrailVerticalOffset": common_types.Float,
    "fTrailHorizontalOffset": common_types.Float,
    "fTrailVerticalSize": common_types.Float,
    "bInvulnerableDash": construct.Flag,
    "fDashTime": common_types.Float,
    "bHorizontalDashOnly": construct.Flag,
    "iChainDashMax": common_types.Int,
    "fCornerDashDistance": common_types.Float,
    "fBackSafeDistance": common_types.Float,
    "fFrontSafeDistance": common_types.Float,
    "fAirBackSafeDistance": common_types.Float,
    "fAirFrontSafeDistance": common_types.Float,
    "fBackCloseSafeDistance": common_types.Float,
    "fFrontCloseSafeDistance": common_types.Float,
    "fEnemiesAirBackSafeDistance": common_types.Float,
    "fEnemiesAirFrontSafeDistance": common_types.Float,
    "fEnemiesBackCloseSafeDistance": common_types.Float,
    "fEnemiesFrontCloseSafeDistance": common_types.Float,
    "fCloseFrontIgnoreInitDistance": common_types.Float,
    "fCloseBackIgnoreInitDistance": common_types.Float,
    "fActivationDelayTime": common_types.Float,
    "fFailMinTimeDelay": common_types.Float,
    "fBezierCurveDistance": common_types.Float,
    "fBezierCurveStep": common_types.Float,
    "bNoInputBackDash": construct.Flag,
    "bHoldToChain": construct.Flag,
    "bAutoLauchOnTime": construct.Flag,
    "bChainWithDirectionTrigger": construct.Flag,
    "bChainWithButtonTrigger": construct.Flag,
    "bCloseAnimationWithoutInput": construct.Flag,
})

CAbilityMultiLockon = Object({
    **CAbilityFields,
    "sTargetFXModel": common_types.StrId,
})

CAbilityMultiLockon_CTunableAbilityMultiLockon = Object({
    **base_tunable_CTunableFields,
    "vColorLocked0": common_types.CVector3D,
    "vColorUnLocked0": common_types.CVector3D,
    "vColorLocked2": common_types.CVector3D,
    "vColorUnLocked2": common_types.CVector3D,
    "fMinChargeTime": common_types.Float,
    "fChargeTime": common_types.Float,
    "fTargetBumbingEffectScale": common_types.Float,
    "fTargetBumbingEffectSize": common_types.Float,
    "fTargetBumbingEffectSpeed": common_types.Float,
    "fTargetingTime": common_types.Float,
    "bActivationInput_R3": construct.Flag,
    "bActivationInput_FireCharge": construct.Flag,
    "bActivationInput_AimCharge": construct.Flag,
})


class CAbilityMultiLockon_SSubState(enum.IntEnum):
    NONE = 0
    Idle = 1
    LockingTargets = 2
    Firing = 3
    Invalid = 2147483647


construct_CAbilityMultiLockon_SSubState = StrictEnum(CAbilityMultiLockon_SSubState)

CAbilityOpticCamouflage = Object(CAbilityFields)

CAbilityOpticCamouflage_CTunableAbilityOpticCamouflage = Object({
    **base_tunable_CTunableFields,
    "fDamagePerSecondStill": common_types.Float,
    "fDamagePerSecondMoving": common_types.Float,
    "iMode": common_types.Int,
    "iSelectionMode": common_types.Int,
    "iSelectionInput": common_types.Int,
    "fSpecialEnergyConsumptionPerSecondStill": common_types.Float,
    "fSpecialEnergyConsumptionPerSecondMoving": common_types.Float,
    "fSpecialEnergyConsumptionOnActivation": common_types.Float,
    "bCanBeActivatedInsideChaseRange": construct.Flag,
    "bRequireMovementToRegenerateSpecialEnergy": construct.Flag,
    "fSpecialEnergyConsumptionOnFireBeam": common_types.Float,
    "fSpecialEnergyConsumptionOnFireGrappleBeam": common_types.Float,
    "fSpecialEnergyConsumptionOnFireHyperBeam": common_types.Float,
    "fSpecialEnergyConsumptionOnFireMissile": common_types.Float,
    "fSpecialEnergyConsumptionOnFireBomb": common_types.Float,
    "fSpecialEnergyConsumptionOnFireLineBomb": common_types.Float,
    "fSpecialEnergyConsumptionOnFirePowerBomb": common_types.Float,
    "fSpecialEnergyConsumptionOnMelee": common_types.Float,
    "bIfNoAeionActionsDeactivateOC": construct.Flag,
    "fDamageOnFireBeam": common_types.Float,
    "fDamageOnFireGrappleBeam": common_types.Float,
    "fDamageOnFireHyperBeam": common_types.Float,
    "fDamageOnFireMissile": common_types.Float,
    "fDamageOnFireBomb": common_types.Float,
    "fDamageOnFireLineBomb": common_types.Float,
    "fDamageOnFirePowerBomb": common_types.Float,
    "fDamageOnMelee": common_types.Float,
})


class CAbilityOpticCamouflage_ESelectionInput(enum.IntEnum):
    RS = 0
    ZR = 1
    Invalid = 4294967295


construct_CAbilityOpticCamouflage_ESelectionInput = StrictEnum(CAbilityOpticCamouflage_ESelectionInput)


class CAbilityOpticCamouflage_ESelectionMode(enum.IntEnum):
    Toggle = 0
    Hold = 1
    Invalid = 4294967295


construct_CAbilityOpticCamouflage_ESelectionMode = StrictEnum(CAbilityOpticCamouflage_ESelectionMode)

CAbilityShinespark = Object(CAbilityFields)

CAbilityShinespark_CTunableAbilityShinespark = Object({
    **base_tunable_CTunableFields,
    "fAllowedActivationTime": common_types.Float,
    "fAllowActivationFXPulseSpeed": common_types.Float,
    "fAfterActivationPreparingLaunchTime": common_types.Float,
    "fSlopeToSpeedBoosterTransitionAngleMin": common_types.Float,
    "fSlopeToSpeedBoosterTransitionAngleMax": common_types.Float,
    "fDefaultImpactDamage": common_types.Float,
    "fDefaultDamageAndRepelVerticalImpulse": common_types.Float,
    "fMorphBallDamageAndRepelImpulse": common_types.Float,
    "fMorphBallPhysicsLaunchSpeed": common_types.Float,
    "fBufferedActivationTime": common_types.Float,
    "fLaunchDirectionAngleInterpolationTime": common_types.Float,
    "fFXFloorNearMaxDistanceCm": common_types.Float,
    "fFXFloorFarMaxDistanceCm": common_types.Float,
    "fMinLaunchAngleUp": common_types.Float,
    "fMinLaunchAngleDiagonalUp": common_types.Float,
    "fMinLaunchAngleForward": common_types.Float,
    "fMinLaunchAngleDiagonalDown": common_types.Float,
    "fMinLaunchAngleUpCoolShinespark": common_types.Float,
    "fMinLaunchAngleDiagonalUpCoolShinespark": common_types.Float,
    "fMinLaunchAngleForwardCoolShinespark": common_types.Float,
    "fMinLaunchAngleDiagonalDownCoolShinespark": common_types.Float,
    "bCoolShinesparkOneOff": construct.Flag,
    "fCoolShinesparkDistanceToCheckPrepareInitTurn": common_types.Float,
    "bActiveCollisionChecksEnabled": construct.Flag,
    "fActiveCollisionChecksSamusOffset": common_types.Float,
    "fActiveCollisionChecksMorphBallOffset": common_types.Float,
})

CAbilitySonar = Object(CAbilityFields)

CAbilitySonar_CTunableAbilitySonar = Object({
    **base_tunable_CTunableFields,
    "fConsumptionOnActivation": common_types.Float,
    "fDiscoveredBreakableTilesTime": common_types.Float,
    "fDiscoveredBreakableTilesDistance": common_types.Float,
    "vDiscoveredBreakableTileInitialColor": common_types.CVector3D,
    "fDiscoveredBreakableTileInitialAlpha": common_types.Float,
    "vDiscoveredBreakableTileColor": common_types.CVector3D,
    "fDiscoveredBreakableTileAlpha": common_types.Float,
    "vDiscoveredBreakableTileEndColor": common_types.CVector3D,
    "fDiscoveredBreakableTileEndAlpha": common_types.Float,
    "fChargingTime": common_types.Float,
    "fDiscoveredLoopFadeTime": common_types.Float,
    "sChargePlaySound": common_types.StrId,
    "sChargeCancelSound": common_types.StrId,
    "fRadiusPropagationTotalTime": common_types.Float,
    "sRadiusPropagationEasingFunction": common_types.StrId,
})

CAbilitySpeedBooster = Object(CAbilityFields)

CAbilitySpeedBooster_CTunableAbilitySpeedBooster = Object({
    **base_tunable_CTunableFields,
    "fTimeToShowPreparationFX": common_types.Float,
    "bInstantActivation": construct.Flag,
    "fTimeToActivate": common_types.Float,
    "fVelocityXFactor": common_types.Float,
    "fMorphballVelocityXFactor": common_types.Float,
    "bAllowJump": construct.Flag,
    "fWallVerticalEndDistance": common_types.Float,
    "fDefaultImpactDamage": common_types.Float,
    "fDefaultDamageAndRepelVerticalImpulse": common_types.Float,
    "fMorphBallDamageAndRepelImpulse": common_types.Float,
    "fBufferedActivationTime": common_types.Float,
})

CUsableComponent = Object(CUsableComponentFields := {
    **CComponentFields,
    "bFadeInActived": construct.Flag,
})

base_global_CRntVector_CGameLink_CEntity__ = common_types.make_vector(common_types.StrId)

base_global_CRntVector_base_global_CStrId_ = common_types.make_vector(common_types.StrId)

base_global_CRntDictionary_base_global_CStrId__base_global_CRntVector_base_global_CStrId__ = common_types.make_dict(base_global_CRntVector_base_global_CStrId_, key=common_types.StrId)

CAccessPointComponent = Object(CAccessPointComponentFields := {
    **CUsableComponentFields,
    "vDoorsToChange": base_global_CRntVector_CGameLink_CEntity__,
    "sInteractionLiteralID": common_types.StrId,
    "tCaptionList": base_global_CRntDictionary_base_global_CStrId__base_global_CRntVector_base_global_CStrId__,
    "wpThermalDevice": common_types.StrId,
})

CAccessPointCommanderComponent = Object({
    **CAccessPointComponentFields,
    "wpAfterFirstDialogueScenePlayer": common_types.StrId,
})

CAccessPointComponent_CTunableAccessPointComponent = Object({
    **base_tunable_CTunableFields,
    "fLoopGainMax": common_types.Float,
    "fLoopFadeInTime": common_types.Float,
    "fLoopFadeOutTime": common_types.Float,
    "fLoopReverb": common_types.Float,
    "fVoiceGainMax": common_types.Float,
    "fVoiceFadeInTime": common_types.Float,
    "fVoiceFadeOutTime": common_types.Float,
    "fVoiceReverb": common_types.Float,
    "fAdamSpeechVolume": common_types.Float,
})

CAcidBlobsLaunchPattern = Object({
    "iDistance": common_types.Int,
    "fTime": common_types.Float,
    "bBreakable": construct.Flag,
})

CAction = Object({})

base_core_CAsset = Object(base_core_CAssetFields := base_core_CBaseObjectFields)

CActionSet = Object(base_core_CAssetFields)

CActivatableComponent = Object(CActivatableComponentFields := CComponentFields)

CActionSwitcherComponent = Object(CActivatableComponentFields)

CActionSwitcherOnPullGrapplePointComponent = Object({
    **CPullableGrapplePointComponentFields,
    "sActionOnPull": common_types.StrId,
})

CActivatableByProjectileComponent = Object(CActivatableByProjectileComponentFields := CComponentFields)


class ELOSMode(enum.IntEnum):
    NONE = 0
    Position = 1
    FrontAndBack = 2
    Parabolic = 3
    Invalid = 2147483647


construct_ELOSMode = StrictEnum(ELOSMode)


class ELOSCheckLevel(enum.IntEnum):
    NONE = 0
    CenterPos = 1
    TopPos = 2
    DownPos = 3
    CenterTopPos = 4
    CenterDownPos = 5
    TopDownPos = 6
    CenterTopDownPos = 7
    Invalid = 2147483647


construct_ELOSCheckLevel = StrictEnum(ELOSCheckLevel)

CPerceptionRuleSet = Object(CPerceptionRuleSetFields := {
    "fTimeForTargetDetection": common_types.Float,
    "fTimeForTargetDetectionEnd": common_types.Float,
    "bForceTargetDetectionByOtherSpawnGroupMember": construct.Flag,
    "bCanSeeThroughOpticCamo": construct.Flag,
    "fInvisibleDetectionTime": common_types.Float,
    "bRequiresTargetInFront": construct.Flag,
    "bRequiresLOSToTarget": construct.Flag,
    "bRequiresDamaged": construct.Flag,
    "bRequiresShooted": construct.Flag,
    "bRequiresImpacted": construct.Flag,
    "eLOSMode": construct_ELOSMode,
    "eLOSCheckLevel": construct_ELOSCheckLevel,
    "fMaxDistanceToTarget": common_types.Float,
    "bShouldBeInFrustrum": construct.Flag,
    "bShouldBeTargetInAreaOfInterest": construct.Flag,
    "bUseStartAOIWhenEndAOIIsEmpty": construct.Flag,
    "bIsAreaOfInterestOptional": construct.Flag,
    "bShouldTargetBeReachable": construct.Flag,
    "bRequiresPathToTarget": construct.Flag,
    "bForceIfDamaged": construct.Flag,
    "fForceIfDamagedTime": common_types.Float,
    "fForceDetectionIfTargetBehindDist": common_types.Float,
    "fForceDetectionIfTargetBehindTime": common_types.Float,
    "bChangeAreaOfInterestOnDamage": construct.Flag,
    "fTimeToUseEndAOIAfterDamage": common_types.Float,
    "bCanDetectWhileFrozen": construct.Flag,
    "bShouldBeInCurrentSubarea": construct.Flag,
    "bShouldBeInCurrentSubareaFailSkipTimeWait": construct.Flag,
})


class EInFrustumMode(enum.IntEnum):
    Position = 0
    AnyDimension = 1
    AllDimensions = 2
    HalfDimensions = 3
    VerticalDimension = 4
    HorizontalDimension = 5
    Invalid = 2147483647


construct_EInFrustumMode = StrictEnum(EInFrustumMode)

CActivationPerceptionRuleSet = Object({
    **CPerceptionRuleSetFields,
    "eOverridedInFrustumMode": construct_EInFrustumMode,
    "fInstantDetectionFrontDistance": common_types.Float,
    "fInstantDetectionBackDistance": common_types.Float,
})

base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_Ptr = Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_.create_construct()

CActor = Object(CActorFields := {
    **CGameObjectFields,
    "sName": common_types.StrId,
    "oActorDefLink": common_types.StrId,
    "sActorDefName": common_types.StrId,
    "vPos": common_types.CVector3D,
    "vAng": common_types.CVector3D,
    "pComponents": base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_Ptr,
    "bEnabled": construct.Flag,
})

CActorPtr = Pointer_CActor.create_construct()

CActorComponentPtr = Pointer_CActorComponent.create_construct()

CActorComponentDef = Object(CActorComponentDefFields := {
    **base_core_CBaseObjectFields,
    "bStartEnabled": construct.Flag,
    "bDisabledInEditor": construct.Flag,
    "bPrePhysicsUpdateInEditor": construct.Flag,
    "bPostPhysicsUpdateInEditor": construct.Flag,
})

base_core_CDefinition = Object(base_core_CDefinitionFields := {
    **base_core_CAssetFields,
    "sLabel": common_types.StrId,
})

CActorDef = Object(CActorDefFields := base_core_CDefinitionFields)

base_global_CRntDictionary_base_global_CStrId__CActorPtr_ = common_types.make_dict(CActorPtr, key=common_types.StrId)

CActorSublayer = Object({
    "sName": common_types.StrId,
    "dctActors": base_global_CRntDictionary_base_global_CStrId__CActorPtr_,
})

base_global_CRntSmallDictionary_base_global_CStrId__CActorSublayer_ = common_types.make_dict(CActorSublayer, key=common_types.StrId)

base_global_CRntVector_CGameLink_CActor__ = common_types.make_vector(common_types.StrId)

base_global_CRntDictionary_base_global_CStrId__base_global_CRntVector_CGameLink_CActor___ = common_types.make_dict(base_global_CRntVector_CGameLink_CActor__, key=common_types.StrId)

CActorLayer = Object({
    "dctSublayers": base_global_CRntSmallDictionary_base_global_CStrId__CActorSublayer_,
    "dctActorGroups": base_global_CRntDictionary_base_global_CStrId__base_global_CRntVector_CGameLink_CActor___,
})

base_color_CColor4B_SRGB = Object(base_color_CColor4B_SRGBFields := {})

CAfterElementDeserializationWrapper = Object(base_color_CColor4B_SRGBFields)

CAimCameraEnabledVisibleOnlyComponent = Object(CComponentFields)

CAimComponent = Object({
    **CComponentFields,
    "sLaserFX": common_types.StrId,
    "sAutoAimLaserFX": common_types.StrId,
    "bAutoAimActive": construct.Flag,
    "bLockOnSoundAllowed": construct.Flag,
    "fCurrentAutoAimWidth": common_types.Float,
    "fCurrentAutoAimConeLength": common_types.Float,
})

CAimComponent_CTunableAim = Object({
    **base_tunable_CTunableFields,
    "vLaserLockedColor0": common_types.CVector3D,
    "fLaserLockedAlpha0": common_types.Float,
    "vLaserUnlockedColor0": common_types.CVector3D,
    "fLaserUnlockedAlpha0": common_types.Float,
    "vLaserLockedColor2": common_types.CVector3D,
    "vLaserUnlockedColor2": common_types.CVector3D,
    "fLaserLockedScale": common_types.Float,
    "fLaserUnlockedScale": common_types.Float,
    "vGrappleLaserLockedColor0": common_types.CVector3D,
    "vGrappleLaserUnlockedColor0": common_types.CVector3D,
    "vGrappleLaserLockedColor2": common_types.CVector3D,
    "vGrappleLaserUnlockedColor2": common_types.CVector3D,
    "bAutoLockOnForceAutoGrapple": construct.Flag,
    "fEndForceFullyChargedTime": common_types.Float,
    "fWalkToRunInputSize": common_types.Float,
    "fRunToWalkInputSize": common_types.Float,
    "fFrontUp": common_types.Float,
    "fFrontUpUp": common_types.Float,
    "fFrontUpDown": common_types.Float,
    "fFrontDown": common_types.Float,
    "fFrontDownUp": common_types.Float,
    "fFrontDownDown": common_types.Float,
    "fFrontLockUp": common_types.Float,
    "fFrontLockDown": common_types.Float,
})

CTriggerLogicAction = Object(CTriggerLogicActionFields := {})


class EShinesparkTravellingDirection(enum.IntEnum):
    No_Direction = 0
    Up = 1
    UpRight = 2
    UpLeft = 3
    Right = 4
    Left = 5
    DownRight = 6
    DownLeft = 7
    Down = 8


construct_EShinesparkTravellingDirection = StrictEnum(EShinesparkTravellingDirection)

base_global_CRntVector_EShinesparkTravellingDirection_ = common_types.make_vector(construct_EShinesparkTravellingDirection)


class ECoolShinesparkSituation(enum.IntEnum):
    Default = 0
    CooldownX = 1


construct_ECoolShinesparkSituation = StrictEnum(ECoolShinesparkSituation)

base_global_CRntVector_ECoolShinesparkSituation_ = common_types.make_vector(construct_ECoolShinesparkSituation)

CAllowCoolShinesparkLogicAction = Object({
    **CTriggerLogicActionFields,
    "lstAllowedDirections": base_global_CRntVector_EShinesparkTravellingDirection_,
    "lstAllowedSituations": base_global_CRntVector_ECoolShinesparkSituation_,
    "sCoolShinesparkId": common_types.StrId,
    "bAllow": construct.Flag,
    "bForce": construct.Flag,
})

CAlternativeActionPlayerComponent = Object(CAlternativeActionPlayerComponentFields := CComponentFields)

CAmmoRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})

CCameraCtrl = Object(CCameraCtrlFields := {
    **CGameObjectFields,
    "bEnabled": construct.Flag,
    "sLuaCallbackOnPossess": common_types.StrId,
    "sLuaCallbackOnUnPossess": common_types.StrId,
})

CCameraBoundaryCtrl = Object(CCameraBoundaryCtrlFields := CCameraCtrlFields)

CAnimatedCameraCtrl = Object(CCameraBoundaryCtrlFields)

CAnimationComponent = Object(CAnimationComponentFields := CComponentFields)

CNavMeshItemComponent = Object(CNavMeshItemComponentFields := {
    **CComponentFields,
    "tForbiddenEdgesSpawnPoints": base_global_CRntVector_CGameLink_CEntity__,
})

CAnimationNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CNavMeshItemStage = Object(CNavMeshItemStageFields := {})

CAnimationNavMeshItemStage = Object(CNavMeshItemStageFields)


class CAnimationPrefix_SPrefix_Enum(enum.IntEnum):
    NONE = 0
    water = 1
    speedbooster = 2
    speedbooster45up = 3
    left = 4
    right = 5
    patrol = 6
    search = 7
    chase = 8
    chase2 = 9
    chasereachable = 10
    combat = 11
    flee = 12
    brokenshield = 13
    grab2 = 14
    grabwater = 15
    protoemmytuto = 16
    preseta = 17
    presetb = 18
    presetc = 19
    Count = 20


construct_CAnimationPrefix_SPrefix_Enum = StrictEnum(CAnimationPrefix_SPrefix_Enum)

CBehaviorTreeAIComponent = Object(CBehaviorTreeAIComponentFields := CAIComponentFields)

CArachnusAIComponent = Object(CBehaviorTreeAIComponentFields)

CSceneComponent = Object(CSceneComponentFields := CComponentFields)

CAreaFXComponent = Object({
    **CSceneComponentFields,
    "sModelResPath": common_types.StrId,
})

CBaseTriggerComponent = Object(CBaseTriggerComponentFields := {
    **CActivatableComponentFields,
    "bCheckAllEntities": construct.Flag,
})


class base_snd_EReverbIntensity(enum.IntEnum):
    NONE = 0
    SMALL_ROOM = 1
    MEDIUM_ROOM = 2
    BIG_ROOM = 3
    CATHEDRAL = 4
    Invalid = 2147483647


construct_base_snd_EReverbIntensity = StrictEnum(base_snd_EReverbIntensity)


class base_snd_ELowPassFilter(enum.IntEnum):
    LPF_DISABLED = 0
    LPF_80HZ = 1
    LPF_100HZ = 2
    LPF_128HZ = 3
    LPF_160HZ = 4
    LPF_200HZ = 5
    LPF_256HZ = 6
    LPF_320HZ = 7
    LPF_400HZ = 8
    LPF_500HZ = 9
    LPF_640HZ = 10
    LPF_800HZ = 11
    LPF_1000HZ = 12
    LPF_1280HZ = 13
    LPF_1600HZ = 14
    LPF_2000HZ = 15
    LPF_2560HZ = 16
    LPF_3200HZ = 17
    LPF_4000HZ = 18
    LPF_5120HZ = 19
    LPF_6400HZ = 20
    LPF_8000HZ = 21
    LPF_10240HZ = 22
    LPF_12800HZ = 23
    LPF_16000HZ = 24
    Invalid = 2147483647


construct_base_snd_ELowPassFilter = StrictEnum(base_snd_ELowPassFilter)

CSoundTrigger = Object(CSoundTriggerFields := {
    **CBaseTriggerComponentFields,
    "eReverb": construct_base_snd_EReverbIntensity,
    "iLowPassFilter": construct_base_snd_ELowPassFilter,
})


class EMusicFadeType(enum.IntEnum):
    NONE = 0
    DEFAULT = 1
    CROSS_FADE = 2
    Invalid = 2147483647


construct_EMusicFadeType = StrictEnum(EMusicFadeType)

CAreaMusicComponent = Object({
    **CSoundTriggerFields,
    "fEnterFadeIn": common_types.Float,
    "fEnterFadeOut": common_types.Float,
    "fExitFadeIn": common_types.Float,
    "fExitFadeOut": common_types.Float,
    "sPreset": common_types.StrId,
    "eEnterFadeType": construct_EMusicFadeType,
    "eExitFadeType": construct_EMusicFadeType,
})


class base_snd_ESndType(enum.IntEnum):
    SFX = 0
    MUSIC = 1
    SPEECH = 2
    GRUNT = 3
    GUI = 4
    ENVIRONMENT_STREAMS = 5
    SFX_EMMY = 6
    CUTSCENE = 7
    Invalid = 2147483647


construct_base_snd_ESndType = StrictEnum(base_snd_ESndType)


class base_snd_EPositionalType(enum.IntEnum):
    POS_2D = 0
    POS_3D = 1
    Invalid = 2147483647


construct_base_snd_EPositionalType = StrictEnum(base_snd_EPositionalType)

CAreaSoundComponent = Object({
    **CSoundTriggerFields,
    "sOnEnterSound": common_types.StrId,
    "eOnEnterSoundType": construct_base_snd_ESndType,
    "fEnterVol": common_types.Float,
    "fEnterPitch": common_types.Float,
    "fEnterFadeInTime": common_types.Float,
    "fEnterFadeOutTime": common_types.Float,
    "eOnEnterPositional": construct_base_snd_EPositionalType,
    "sLoopSound": common_types.StrId,
    "eLoopSoundType": construct_base_snd_ESndType,
    "fLoopVol": common_types.Float,
    "fLoopPitch": common_types.Float,
    "fLoopPan": common_types.Float,
    "fLoopFadeInTime": common_types.Float,
    "fLoopFadeOutTime": common_types.Float,
    "sOnExitSound": common_types.StrId,
    "eOnExitSoundType": construct_base_snd_ESndType,
    "fExitVol": common_types.Float,
    "fExitPitch": common_types.Float,
    "fExitFadeInTime": common_types.Float,
    "fExitFadeOutTime": common_types.Float,
    "eOnExitPositional": construct_base_snd_EPositionalType,
})

CArenaManager_CTunableArenaManager = Object({
    **base_tunable_CTunableFields,
    "fSelectPreviousArenaProbability": common_types.Float,
})

CAttack = Object(CAttackFields := {})

CAttackPreset = Object({
    "bEnabled": construct.Flag,
    "fMinNextAttackTime": common_types.Float,
    "fMaxNextAttackTime": common_types.Float,
    "fMandatoryMinNextAttackTime": common_types.Float,
    "fMandatoryMaxNextAttackTime": common_types.Float,
    "fRepeatAttackTime": common_types.Float,
    "fShortDistanceProb": common_types.Float,
    "fMediumDistanceProb": common_types.Float,
    "fLongDistanceProb": common_types.Float,
    "fAbuseShortDistanceProb": common_types.Float,
    "fAbuseMediumDistanceProb": common_types.Float,
    "fAbuseLongDistanceProb": common_types.Float,
    "fAbuseTime": common_types.Float,
    "uMaxOccurrencesInLastAttacks": common_types.UInt,
    "uNumOfAttacksToEvaluate": common_types.UInt,
})

CAudioComponent = Object(CComponentFields)

CRobotAIComponent = Object(CRobotAIComponentFields := CBehaviorTreeAIComponentFields)

CAutclastAIComponent = Object(CRobotAIComponentFields)

CAutclastChargeAttack = Object(CAttackFields)


class EJumpType(enum.IntEnum):
    Short = 0
    Large = 1
    Invalid = 2147483647


construct_EJumpType = StrictEnum(EJumpType)

CAutectorAIComponent = Object({
    **CRobotAIComponentFields,
    "eJumpType": construct_EJumpType,
})

CLifeComponent = Object(CLifeComponentFields := {
    **CComponentFields,
    "bWantsCameraFXPreset": construct.Flag,
    "fMaxLife": common_types.Float,
    "fCurrentLife": common_types.Float,
    "bCurrentLifeLocked": construct.Flag,
})

CCharacterLifeComponent = Object(CCharacterLifeComponentFields := {
    **CLifeComponentFields,
    "sImpactAnim": common_types.StrId,
    "sDeadAnim": common_types.StrId,
})

CEnemyLifeComponent = Object(CEnemyLifeComponentFields := {
    **CCharacterLifeComponentFields,
    "sImpactBackAnim": common_types.StrId,
    "sDeadBackAnim": common_types.StrId,
    "sDeadAirAnim": common_types.StrId,
    "sDeadAirBackAnim": common_types.StrId,
})

CAutectorLifeComponent = Object(CEnemyLifeComponentFields)

CAutofocusAimCameraCtrl = Object(CCameraCtrlFields)

CAutofocusAimCameraCtrl_CTunableAutofocusAimCameraCtrl = Object({
    **base_tunable_CTunableFields,
    "bForceActivation": construct.Flag,
    "fInterpolationSpeed": common_types.Float,
    "fInterpolationAccel": common_types.Float,
    "fInterpolationInterruptFactor": common_types.Float,
    "v3TargetOffset": common_types.CVector3D,
    "v3TargetPadding": common_types.CVector3D,
    "fEmmyAlarmVolume": common_types.Float,
    "fAimNewCameraDistance": common_types.Float,
    "fAimNewCameraAng": common_types.Float,
    "fAimNewCameraOffsetY": common_types.Float,
    "bAimNewCameraAvoidWallOcclusion": construct.Flag,
    "fAimNewCameraChaseAutoAimMinInterpolationDist": common_types.Float,
    "fAimNewCameraChaseAutoAimMaxInterpolationDist": common_types.Float,
    "bAimNewCameraChaseAutoAimForceEmmyMaxYInsideCamera": construct.Flag,
    "fAimNewCameraFreeAimInterpolationSpeed": common_types.Float,
    "iAimNewCameraInputMode": common_types.Int,
})

CAutomperAIComponent = Object(CRobotAIComponentFields)

CAutomperAutomaticIrradiationAttack = Object(CAttackFields)

CAutoolAIComponent = Object({
    **CRobotAIComponentFields,
    "vAISmartObjects": base_global_CRntVector_CGameLink_CActor__,
})


class CAutoolAIComponent_EThrusterMode(enum.IntEnum):
    EPowerOff = 0
    EHalfPower = 1
    EFullPower = 2
    Invalid = 2147483647


construct_CAutoolAIComponent_EThrusterMode = StrictEnum(CAutoolAIComponent_EThrusterMode)

CAutsharpAIComponent = Object(CRobotAIComponentFields)

CAutsharpLifeComponent = Object(CEnemyLifeComponentFields)


class CSpawnPointComponent_EXCellSpawnPositionMode(enum.IntEnum):
    FarthestToSpawnPoint = 0
    ClosestToSpawnPoint = 1
    Invalid = 2147483647


construct_CSpawnPointComponent_EXCellSpawnPositionMode = StrictEnum(CSpawnPointComponent_EXCellSpawnPositionMode)


class CSpawnPointComponent_EDynamicSpawnPositionMode(enum.IntEnum):
    ClosestToPlayer = 0
    FarthestToPlayer = 1
    Random = 2
    Invalid = 2147483647


construct_CSpawnPointComponent_EDynamicSpawnPositionMode = StrictEnum(CSpawnPointComponent_EDynamicSpawnPositionMode)

base_reflection_CTypedValue = Pointer_base_global_CRntFile.create_construct()

CSpawnerActorBlueprint = Object({
    "InnerValue": base_reflection_CTypedValue,
})

base_global_CRntVector_CSpawnerActorBlueprint_ = common_types.make_vector(CSpawnerActorBlueprint)

CSpawnPointComponent = Object(CSpawnPointComponentFields := {
    **CComponentFields,
    "sOnBeforeGenerate": common_types.StrId,
    "sOnEntityGenerated": common_types.StrId,
    "sStartAnimation": common_types.StrId,
    "bSpawnOnFloor": construct.Flag,
    "bEntityCheckFloor": construct.Flag,
    "bCheckCollisions": construct.Flag,
    "fTimeToActivate": common_types.Float,
    "iMaxNumToGenerate": common_types.Int,
    "bAllowSpawnInFrustum": construct.Flag,
    "bStartEnabled": construct.Flag,
    "bAutomanaged": construct.Flag,
    "wpSceneShapeId": common_types.StrId,
    "wpCollisionSceneShapeId": common_types.StrId,
    "wpNavigableShape": common_types.StrId,
    "wpAreaOfInterest": common_types.StrId,
    "wpAreaOfInterestEnd": common_types.StrId,
    "fTimeOnAOIEndToUseAsMainAOI": common_types.Float,
    "fSpawnFromXCellProbability": common_types.Float,
    "fSpawnFromXCellProbabilityAfterFirst": common_types.Float,
    "eXCellSpawnPositionMode": construct_CSpawnPointComponent_EXCellSpawnPositionMode,
    "bUseDynamicSpawnPosition": construct.Flag,
    "eDynamicSpawnPositionMode": construct_CSpawnPointComponent_EDynamicSpawnPositionMode,
    "tDynamicSpawnPositions": base_global_CRntVector_CGameLink_CActor__,
    "tXCellTransformTargets": base_global_CRntVector_CGameLink_CActor__,
    "wpXCellActivationAreaShape": common_types.StrId,
    "sCharClass": common_types.StrId,
    "voActorBlueprint": base_global_CRntVector_CSpawnerActorBlueprint_,
})


class EAutsharpSpawnPointDir(enum.IntEnum):
    Left = 0
    Right = 1
    Both = 2
    Invalid = 2147483647


construct_EAutsharpSpawnPointDir = StrictEnum(EAutsharpSpawnPointDir)

CAutsharpSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": construct_EAutsharpSpawnPointDir,
    "wpSpawnShape": common_types.StrId,
})

CAutsniperAIComponent = Object(CRobotAIComponentFields)

CAutsniperShootAttack = Object(CAttackFields)


class CAutsniperShootAttack_EAutsniperState(enum.IntEnum):
    InMovementState = 0
    InIdleState = 1
    InFrozenState = 2
    Invalid = 2147483647


construct_CAutsniperShootAttack_EAutsniperState = StrictEnum(CAutsniperShootAttack_EAutsniperState)


class CAutsniperShootAttack_ELaserState(enum.IntEnum):
    WaitState = 0
    ChargeState = 1
    PrepareToShootState = 2
    CrazyBeforeShootState = 3
    BeforeShootState = 4
    ShootState = 5
    AfterShootState = 6
    RelocateCannonAndFinish = 7
    Invalid = 2147483647


construct_CAutsniperShootAttack_ELaserState = StrictEnum(CAutsniperShootAttack_ELaserState)


class EAutsniperSpawnPointDir(enum.IntEnum):
    Clockwise = 0
    Counterclockwise = 1
    Invalid = 2147483647


construct_EAutsniperSpawnPointDir = StrictEnum(EAutsniperSpawnPointDir)

CAutsniperSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": construct_EAutsniperSpawnPointDir,
})

CBTObserverComponent = Object(CActorComponentFields)

CBarelyFrozenIceInfo = Object({
    "sModel": common_types.StrId,
    "sNode": common_types.StrId,
    "fScale": common_types.Float,
})

CBossAIComponent = Object(CBossAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "sArenaLeftLandmark": common_types.StrId,
    "sArenaRightLandmark": common_types.StrId,
    "fArenaLimitDist": common_types.Float,
    "tDoors": base_global_CRntVector_CGameLink_CEntity__,
    "wpBossCamera": common_types.StrId,
    "wpBossCameraFloorLandmark": common_types.StrId,
    "wpBossCameraCeilingLandmark": common_types.StrId,
    "wpStartCombatCheckpointStartPoint": common_types.StrId,
    "sStartCombatCheckpointSnapshotId": common_types.StrId,
    "wpDeadCheckpointStartPoint": common_types.StrId,
    "bSaveGameOnAfterDead": construct.Flag,
})

CBaseBigFistAIComponent = Object(CBaseBigFistAIComponentFields := {
    **CBossAIComponentFields,
    "fMinTimeBetweenDigs": common_types.Float,
    "fMaxTimeBetweenDigs": common_types.Float,
    "fMinTimeDigging": common_types.Float,
    "fMaxTimeDigging": common_types.Float,
})

CBaseDamageTriggerComponent = Object(CBaseDamageTriggerComponentFields := {
    **CBaseTriggerComponentFields,
    "sContinuousDamageSound": common_types.StrId,
})

gameeditor_CGameModelIndex = Object({})

CBaseGameLink = Object({
    "oLinkIndex": gameeditor_CGameModelIndex,
})

CBaseGroundShockerAIComponent = Object(CBaseGroundShockerAIComponentFields := CBehaviorTreeAIComponentFields)


class engine_utils_ELightPreset(enum.IntEnum):
    E_LIGHT_PRESET_NONE = 0
    E_LIGHT_PRESET_PULSE = 1
    E_LIGHT_PRESET_BLINK = 2
    E_LIGHT_PRESET_LIGHTNING = 3
    ELIGHT_PRESET_COUNT = 4
    ELIGHT_PRESET_INVALID = 5
    Invalid = 2147483647


construct_engine_utils_ELightPreset = StrictEnum(engine_utils_ELightPreset)

CBaseLightComponent = Object(CBaseLightComponentFields := {
    **CComponentFields,
    "vLightPos": common_types.CVector3D,
    "fIntensity": common_types.Float,
    "fVIntensity": common_types.Float,
    "fFIntensity": common_types.Float,
    "vAmbient": common_types.CVector4D,
    "vDiffuse": common_types.CVector4D,
    "vSpecular0": common_types.CVector4D,
    "vSpecular1": common_types.CVector4D,
    "bVertexLight": construct.Flag,
    "eLightPreset": construct_engine_utils_ELightPreset,
    "vLightPresetParams": common_types.CVector4D,
    "bSubstractive": construct.Flag,
    "bUseFaceCull": construct.Flag,
    "bUseSpecular": construct.Flag,
})

CBasicLifeComponent = Object(CBasicLifeComponentFields := CLifeComponentFields)

CBatalloonAIComponent = Object({
    **CBaseGroundShockerAIComponentFields,
    "bReceivingCall": construct.Flag,
})

CItemLifeComponent = Object(CItemLifeComponentFields := CLifeComponentFields)

SBeamBoxActivatable = Object({
    "oActivatableObj": common_types.StrId,
    "sState": common_types.StrId,
})

base_global_CRntVector_SBeamBoxActivatable_ = common_types.make_vector(SBeamBoxActivatable)

CBeamBoxComponent = Object({
    **CItemLifeComponentFields,
    "fDisplaceDist": common_types.Float,
    "vActivatables": base_global_CRntVector_SBeamBoxActivatable_,
    "sAnimationId": common_types.StrId,
})


class CDoorShieldLifeComponent_EColor(enum.IntEnum):
    NONE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    Invalid = 2147483647


construct_CDoorShieldLifeComponent_EColor = StrictEnum(CDoorShieldLifeComponent_EColor)

CDoorShieldLifeComponent = Object(CDoorShieldLifeComponentFields := {
    **CItemLifeComponentFields,
    "fDamageFXTime": common_types.Float,
    "sDamageSound": common_types.StrId,
    "sKillSound": common_types.StrId,
    "eColor": construct_CDoorShieldLifeComponent_EColor,
})

CBeamDoorLifeComponent = Object(CDoorShieldLifeComponentFields)

CGun = Object(CGunFields := CGameObjectFields)

CPrimaryGun = Object(CPrimaryGunFields := CGunFields)

CBeamGun = Object(CBeamGunFields := CPrimaryGunFields)

CBigFistAIComponent = Object({
    **CBaseBigFistAIComponentFields,
    "timeForNextDig": common_types.Float,
})

CBigFistAttack = Object(CAttackFields)


class CBigFistAttack_EBigFistAttackState(enum.IntEnum):
    NONE = 0
    Started = 1
    PostAttackLoop = 2
    Recovering = 3
    Invalid = 2147483647


construct_CBigFistAttack_EBigFistAttackState = StrictEnum(CBigFistAttack_EBigFistAttackState)

CBigkranXAIComponent = Object(CBaseBigFistAIComponentFields)

CBigkranXMagmaRainAttack = Object(CAttackFields)


class CBigkranXMagmaRainAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    Loop = 2
    End = 3
    Invalid = 2147483647


construct_CBigkranXMagmaRainAttack_EState = StrictEnum(CBigkranXMagmaRainAttack_EState)

CBigkranXSpitAttack = Object(CAttackFields)


class CBigkranXSpitAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    Loop = 2
    End = 3
    Invalid = 2147483647


construct_CBigkranXSpitAttack_EState = StrictEnum(CBigkranXSpitAttack_EState)

CCollisionComponent = Object(CCollisionComponentFields := CComponentFields)

CBillboardCollisionComponent = Object(CCollisionComponentFields)

CBillboardComponent = Object({
    **CComponentFields,
    "iNumGroups": common_types.Int,
    "iMaxInhabitantsPerGroup": common_types.Int,
    "iMinInhabitantsPerGroup": common_types.Int,
})

CBillboardLifeComponent = Object(CLifeComponentFields)

CBlackboard_CSectionPtr = Pointer_CBlackboard_CSection.create_construct()

base_global_CRntDictionary_base_global_CStrId__CBlackboard_CSectionPtr_ = common_types.make_dict(CBlackboard_CSectionPtr, key=common_types.StrId)

CBlackboard_TSectionContainer = base_global_CRntDictionary_base_global_CStrId__CBlackboard_CSectionPtr_

CBlackboard = Object(CBlackboardFields := {
    "hashSections": CBlackboard_TSectionContainer,
})

base_global_CRntSmallDictionary_base_global_CStrId__base_reflection_CTypedValue_ = common_types.make_dict(base_reflection_CTypedValue, key=common_types.StrId)

CBlackboard_CSection = Object({
    "dctProps": base_global_CRntSmallDictionary_base_global_CStrId__base_reflection_CTypedValue_,
})

CBombGun = Object(CPrimaryGunFields)

CBombGun_CTunableBomb = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "sDamageSource": common_types.StrId,
    "fHeat": common_types.Float,
})

CMovementComponent = Object(CMovementComponentFields := {
    **CComponentFields,
    "bIsFlying": construct.Flag,
})

CWeaponMovement = Object(CWeaponMovementFields := CMovementComponentFields)

CBombMovement = Object(CBombMovementFields := {
    **CWeaponMovementFields,
    "sCollisionFX": common_types.StrId,
})

CBombMovement_CTunableBombMovement = Object({
    **base_tunable_CTunableFields,
    "fTimeToExplode": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fExplosionRadiusPlayer": common_types.Float,
    "fExplosionExpansionTime": common_types.Float,
    "fExplosionLifeTime": common_types.Float,
})

CBoneToConstantComponent = Object(CSceneComponentFields)

CBossCameraCtrl = Object(CCameraBoundaryCtrlFields)

CBossLifeComponent = Object(CEnemyLifeComponentFields)

base_global_CRntVector_CGameLink_CSpawnPointComponent__ = common_types.make_vector(common_types.StrId)

CSpawnGroupComponent = Object(CSpawnGroupComponentFields := {
    **CComponentFields,
    "bIsGenerator": construct.Flag,
    "bIsInfinite": construct.Flag,
    "iMaxToGenerate": common_types.Int,
    "iMaxSimultaneous": common_types.Int,
    "fGenerateEvery": common_types.Float,
    "sOnBeforeGenerateEntity": common_types.StrId,
    "sOnEntityGenerated": common_types.StrId,
    "sOnEnable": common_types.StrId,
    "sOnDisable": common_types.StrId,
    "sOnMaxSimultaneous": common_types.StrId,
    "sOnMaxGenerated": common_types.StrId,
    "sOnEntityDead": common_types.StrId,
    "sOnEntityDamaged": common_types.StrId,
    "sOnAllEntitiesDead": common_types.StrId,
    "bAutomanaged": construct.Flag,
    "bDisableOnAllDead": construct.Flag,
    "bAutoenabled": construct.Flag,
    "bSpawnPointsNotInFrustrum": construct.Flag,
    "bGenerateEntitiesByOrder": construct.Flag,
    "sLogicCollisionShapeID": common_types.StrId,
    "wpAreaOfInterest": common_types.StrId,
    "wpAreaOfInterestEnd": common_types.StrId,
    "fDropAmmoProb": common_types.Float,
    "iInitToGenerate": common_types.Int,
    "sArenaId": common_types.StrId,
    "bCheckActiveDrops": construct.Flag,
    "iNumDeaths": common_types.Int,
    "vectSpawnPoints": base_global_CRntVector_CGameLink_CSpawnPointComponent__,
})

CBossSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "sBossBattleLabel": common_types.StrId,
})

CBouncingCreaturesLaunchPattern = Object({
    "fAngle": common_types.Float,
    "fSpeed": common_types.Float,
    "fReboundImpulse": common_types.Float,
    "fDelay": common_types.Float,
})

std_unique_ptr_game_logic_collision_CShape_ = Pointer_game_logic_collision_CShape.create_construct()

CLogicShapeComponent = Object(CLogicShapeComponentFields := {
    **CActorComponentFields,
    "pLogicShape": std_unique_ptr_game_logic_collision_CShape_,
    "bWantsToGenerateNavMeshEdges": construct.Flag,
})

CBreakableHintComponent = Object(CLogicShapeComponentFields)

CBreakableScenarioComponent = Object({
    **CComponentFields,
    "aVignettes": base_global_CRntVector_CGameLink_CActor__,
})

CBreakableTileGroup = Object(CGameObjectFields)


class EBreakableTileType(enum.IntEnum):
    UNDEFINED = 0
    POWERBEAM = 1
    BOMB = 2
    MISSILE = 3
    SUPERMISSILE = 4
    POWERBOMB = 5
    SCREWATTACK = 6
    WEIGHT = 7
    BABYHATCHLING = 8
    SPEEDBOOST = 9
    Invalid = 2147483647


construct_EBreakableTileType = StrictEnum(EBreakableTileType)

CBreakableTileGroupComponent_STileInfo = Object({
    "eTileType": construct_EBreakableTileType,
    "vGridCoords": common_types.CVector2D,
    "sHiddenSG": common_types.StrId,
    "bIsHidingSecret": construct.Flag,
    "aVignettes": base_global_CRntVector_CGameLink_CActor__,
})

base_global_CRntVector_CBreakableTileGroupComponent_STileInfo_ = common_types.make_vector(CBreakableTileGroupComponent_STileInfo)


class game_logic_collision_EColMat(enum.IntEnum):
    DEFAULT = 0
    SCENARIO_GENERIC = 1
    FLESH_GENERIC = 2
    DAMAGE_BLOCKED = 3
    METAL = 4
    ENERGY = 5
    DIRT = 6
    ROCK = 7
    ICE = 8
    UNDER_WATER = 9
    UNDER_WATER_SP = 10
    MID_WATER = 11
    MID_WATER_SP = 12
    PUDDLE = 13
    OIL = 14
    END_WORLD = 15
    Invalid = 4294967295


construct_game_logic_collision_EColMat = StrictEnum(game_logic_collision_EColMat)

CBreakableTileGroupComponent = Object({
    **CSceneComponentFields,
    "uGroupId": common_types.UInt,
    "aGridTiles": base_global_CRntVector_CBreakableTileGroupComponent_STileInfo_,
    "bFakeHusks": construct.Flag,
    "eCollisionMaterial": construct_game_logic_collision_EColMat,
})

CBreakableTileGroupComponent_SMinimapTileState = Object({
    "fX": common_types.Float,
    "fY": common_types.Float,
    "eTileType": construct_EBreakableTileType,
    "uState": common_types.UInt,
})

CSonarTargetComponent = Object(CSonarTargetComponentFields := CComponentFields)

CBreakableTileGroupSonarTargetComponent = Object(CSonarTargetComponentFields)

CBreakableTileLoader = Object({})

CBreakableTileManager_STileGroupGroup = Object({})

base_global_CRntPooledDictionary_base_global_CStrId__CBreakableTileManager_STileGroupGroup_ = common_types.make_dict(CBreakableTileManager_STileGroupGroup, key=common_types.StrId)

CBreakableTileManager = Object({
    "dctBreakableTileGroupGroups": base_global_CRntPooledDictionary_base_global_CStrId__CBreakableTileManager_STileGroupGroup_,
})

CBreakableTileManager_CTunableBreakableTileManager = Object({
    **base_tunable_CTunableFields,
    "fPowerBeamRespawnTime": common_types.Float,
    "fBombRespawnTime": common_types.Float,
    "fMissileRespawnTime": common_types.Float,
    "fSuperMissileRespawnTime": common_types.Float,
    "fPowerBombRespawnTime": common_types.Float,
    "fScrewAttackRespawnTime": common_types.Float,
    "fWeightRespawnTime": common_types.Float,
    "fSpeedBoostRespawnTime": common_types.Float,
    "fChainDestructionTimePerTile": common_types.Float,
    "fRespawnTimeWhenDestroyedWithHyperBeam": common_types.Float,
})

CBreakableVignetteComponent = Object({
    **CLogicShapeComponentFields,
    "sVignetteSG": common_types.StrId,
    "bUnhideWhenPlayerInside": construct.Flag,
    "bPreventVisibilityOnly": construct.Flag,
    "bForceNotVisible": construct.Flag,
})

CCameraComponent = Object({
    **CComponentFields,
    "fCurrentInterp": common_types.Float,
    "vCurrentPos": common_types.CVector3D,
    "vCurrentDir": common_types.CVector3D,
    "fDefaultInterp": common_types.Float,
    "fCurrentInterpChangeSpeed": common_types.Float,
    "fDefaultNear": common_types.Float,
    "fDefaultFar": common_types.Float,
    "bIgnoreSlomo": construct.Flag,
})

CCameraFX = Object(CCameraFXFields := {
    **CGameObjectFields,
    "sID": common_types.StrId,
})

CCameraFX_Shake = Object(CCameraFX_ShakeFields := {
    **CCameraFXFields,
    "fTime": common_types.Float,
    "fAttMinRange": common_types.Float,
    "fAttMaxRange": common_types.Float,
    "fAttRange": common_types.Float,
    "sAttRangeFunction": common_types.StrId,
})

CCameraFX_CrossShake = Object({
    **CCameraFX_ShakeFields,
    "fDistance": common_types.Float,
    "fIterations": common_types.Float,
})

CCameraFX_MotionShake = Object({
    **CCameraFX_ShakeFields,
    "fDistance": common_types.Float,
    "sFunction": common_types.StrId,
})

CCameraFX_OscillationShake = Object({
    **CCameraFX_ShakeFields,
    "sFunction": common_types.StrId,
    "fAmplitudeX": common_types.Float,
    "fSpeedX": common_types.Float,
    "fAmplitudeY": common_types.Float,
    "fSpeedY": common_types.Float,
    "fAmplitudeZ": common_types.Float,
    "fSpeedZ": common_types.Float,
    "fTimeToMax": common_types.Float,
})

CCameraFX_RandShake = Object({
    **CCameraFX_ShakeFields,
    "sFunction": common_types.StrId,
    "fDistance": common_types.Float,
    "fTwist": common_types.Float,
})

CCameraFX_RotationShake = Object({
    **CCameraFX_ShakeFields,
    "fAmplitude": common_types.Float,
    "sFunction": common_types.StrId,
    "bCentered": construct.Flag,
})

CCameraFX_SteadyCamera = Object({
    **CCameraFXFields,
    "fMinAngleXAxis": common_types.Float,
    "fMaxAngleXAxis": common_types.Float,
    "fMinAngleYAxis": common_types.Float,
    "fMaxAngleYAxis": common_types.Float,
    "sFunction": common_types.StrId,
    "bCentered": construct.Flag,
})

IPath = Object(IPathFields := {})

ISubPath = Object(ISubPathFields := {})

IPathNode = Object(IPathNodeFields := {})

SCameraRailNode = Object({
    **IPathNodeFields,
    "vPos": common_types.CVector3D,
    "wpLogicCamera": common_types.StrId,
})

base_global_CRntVector_SCameraRailNode_ = common_types.make_vector(SCameraRailNode)

SCameraSubRail = Object({
    **ISubPathFields,
    "tNodes": base_global_CRntVector_SCameraRailNode_,
})

base_global_CRntVector_SCameraSubRail_ = common_types.make_vector(SCameraSubRail)

SCameraRail = Object({
    **IPathFields,
    "tSubRails": base_global_CRntVector_SCameraSubRail_,
    "fMaxRailSpeed": common_types.Float,
    "fMinRailSpeed": common_types.Float,
    "fMaxRailDistance": common_types.Float,
})

CCameraRailComponent = Object({
    **CActorComponentFields,
    "oCameraRail": SCameraRail,
})

CCameraToRailLogicAction = Object({
    **CTriggerLogicActionFields,
    "bCameraToRail": construct.Flag,
})


class EElevatorDirection(enum.IntEnum):
    UP = 0
    DOWN = 1
    Invalid = 2147483647


construct_EElevatorDirection = StrictEnum(EElevatorDirection)


class ELoadingScreen(enum.IntEnum):
    E_LOADINGSCREEN_GUI_2D = 0
    E_LOADINGSCREEN_VIDEO = 1
    E_LOADINGSCREEN_ELEVATOR_UP = 2
    E_LOADINGSCREEN_ELEVATOR_DOWN = 3
    E_LOADINGSCREEN_MAIN_ELEVATOR_UP = 4
    E_LOADINGSCREEN_MAIN_ELEVATOR_DOWN = 5
    E_LOADINGSCREEN_TELEPORTER = 6
    E_LOADINGSCREEN_TRAIN_LEFT = 7
    E_LOADINGSCREEN_TRAIN_LEFT_AQUA = 8
    E_LOADINGSCREEN_TRAIN_RIGHT = 9
    E_LOADINGSCREEN_TRAIN_RIGHT_AQUA = 10
    Invalid = 2147483647


construct_ELoadingScreen = StrictEnum(ELoadingScreen)

CElevatorUsableComponent = Object(CElevatorUsableComponentFields := {
    **CUsableComponentFields,
    "eDirection": construct_EElevatorDirection,
    "eLoadingScreen": construct_ELoadingScreen,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "sMapConnectionId": common_types.StrId,
    "fMinTimeLoad": common_types.Float,
})

CCapsuleUsableComponent = Object({
    **CElevatorUsableComponentFields,
    "wpCapsule": common_types.StrId,
    "wpSkybase": common_types.StrId,
})

CCaterzillaAIComponent = Object(CBehaviorTreeAIComponentFields)


class ECaterzillaSpawnPointDir(enum.IntEnum):
    Front = 0
    Side = 1
    Invalid = 2147483647


construct_ECaterzillaSpawnPointDir = StrictEnum(ECaterzillaSpawnPointDir)


class ECaterzillaSpawnPointOrder(enum.IntEnum):
    First = 0
    Second = 1
    InFrustrum = 2
    Invalid = 2147483647


construct_ECaterzillaSpawnPointOrder = StrictEnum(ECaterzillaSpawnPointOrder)

CCaterzillaSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": construct_ECaterzillaSpawnPointDir,
    "eSpawnOrder": construct_ECaterzillaSpawnPointOrder,
    "NumCaterzillas": common_types.UInt,
    "fTimeToGenerateNextWave": common_types.Float,
    "wpSpawnPointLinked": common_types.StrId,
    "fTimeToRespawnAllCaterzillas": common_types.Float,
    "aHomeLandmarks": base_global_CRntVector_CGameLink_CActor__,
    "bInOutSpawnPoint": construct.Flag,
})


class CCentralUnitComponent_ECentralUnitMode(enum.IntEnum):
    Default = 0
    Decayed = 1
    Cave = 2
    Shipyard = 3
    Invalid = 2147483647


construct_CCentralUnitComponent_ECentralUnitMode = StrictEnum(CCentralUnitComponent_ECentralUnitMode)

CCentralUnitComponent_SStartPointInfo = Object({
    "wpStartPoint": common_types.StrId,
    "wpEmmyLandmark": common_types.StrId,
})

base_global_CRntVector_CCentralUnitComponent_SStartPointInfo_ = common_types.make_vector(CCentralUnitComponent_SStartPointInfo)

std_unique_ptr_CCentralUnitWeightedEdges_ = Pointer_CCentralUnitWeightedEdges.create_construct()

base_global_CRntVector_std_unique_ptr_CCentralUnitWeightedEdges__ = common_types.make_vector(std_unique_ptr_CCentralUnitWeightedEdges_)

CCentralUnitComponent = Object(CCentralUnitComponentFields := {
    **CActorComponentFields,
    "eMode": construct_CCentralUnitComponent_ECentralUnitMode,
    "bStartEnabled": construct.Flag,
    "wpBossSpawnPoint": common_types.StrId,
    "wpCentralUnitAI": common_types.StrId,
    "wpBossAlive": common_types.StrId,
    "wpBossDestroyed": common_types.StrId,
    "wpBossDoor": common_types.StrId,
    "sBossCollisionCameraID": common_types.StrId,
    "wpEmmySpawnPoint": common_types.StrId,
    "tEmmyStartPointsInfo": base_global_CRntVector_CCentralUnitComponent_SStartPointInfo_,
    "wpEmmyZoneShape": common_types.StrId,
    "wpDestroySearchLandmark": common_types.StrId,
    "tEmmyForbiddenShapes": base_global_CRntVector_CGameLink_CActor__,
    "tEmmyWeightedShapes": base_global_CRntVector_std_unique_ptr_CCentralUnitWeightedEdges__,
    "bUnlockDoorsOnEmmyDead": construct.Flag,
    "tEmmyLockedDoors": base_global_CRntVector_CGameLink_CEntity__,
    "tEmmyPhase2DeactivatedActors": base_global_CRntVector_CGameLink_CActor__,
    "wpStartCombatCheckpointStartPoint": common_types.StrId,
    "sStartCombatCheckpointSnapshotId": common_types.StrId,
    "wpDeadCheckpointStartPoint": common_types.StrId,
})

CCaveCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CCentralUnitComponentDef = Object(CCentralUnitComponentDefFields := CActorComponentDefFields)

CCaveCentralUnitComponentDef = Object(CCentralUnitComponentDefFields)


class CRinkaUnitComponent_ECentralUnitType(enum.IntEnum):
    Caves = 0
    Magma = 1
    Lab = 2
    Forest = 3
    Sanc = 4
    Invalid = 2147483647


construct_CRinkaUnitComponent_ECentralUnitType = StrictEnum(CRinkaUnitComponent_ECentralUnitType)

CCentralUnitAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "vSpawnPointActors": base_global_CRntVector_CGameLink_CActor__,
    "eType": construct_CRinkaUnitComponent_ECentralUnitType,
    "wpDoorCentralUnit": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CCentralUnitCannonAIComponent = Object(CAIComponentFields)


class CCentralUnitCannonAIComponent_EState(enum.IntEnum):
    NONE = 0
    Closed = 1
    Opening = 2
    Opened = 3
    Preparing = 4
    Shot = 5
    Closing = 6
    Invalid = 2147483647


construct_CCentralUnitCannonAIComponent_EState = StrictEnum(CCentralUnitCannonAIComponent_EState)

CProjectileMovement = Object(CProjectileMovementFields := {
    **CWeaponMovementFields,
    "fMaxDist": common_types.Float,
    "fMaxLifeTime": common_types.Float,
    "sCollisionFX": common_types.StrId,
    "fFXAngZOffset": common_types.Float,
    "fFXScl": common_types.Float,
    "sNoDamageFX": common_types.StrId,
    "sEnergyCollisionFX": common_types.StrId,
})

CCentralUnitCannonBeamMovementComponent = Object(CProjectileMovementFields)

CCentralUnitWeightedEdges = Object({
    "sId": common_types.StrId,
    "pLogicShape": common_types.StrId,
    "fFactorToAdd": common_types.Float,
    "fFactorToMultiply": common_types.Float,
})

CChainReactionActionSwitcherComponent = Object(CComponentFields)

CChangeSetupLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSetupID": common_types.StrId,
    "bPersistent": construct.Flag,
    "bForceChange": construct.Flag,
    "bPush": construct.Flag,
})

CChangeStageNavMeshItemComponent = Object(CComponentFields)


class eDoorStateLogicAction(enum.IntEnum):
    Open = 0
    Close = 1
    Lock = 2
    Unlock = 3
    Invalid = 2147483647


construct_eDoorStateLogicAction = StrictEnum(eDoorStateLogicAction)

DoorStateInfo = Object({
    "pDoor": common_types.StrId,
    "eDoorState": construct_eDoorStateLogicAction,
})

base_global_CRntVector_DoorStateInfo_ = common_types.make_vector(DoorStateInfo)

CChangeStateDoorsLogicAction = Object({
    **CTriggerLogicActionFields,
    "vDoorStateInfo": base_global_CRntVector_DoorStateInfo_,
    "bEnabled": construct.Flag,
})

CCharClass = Object(CActorDefFields)

base_global_timeline_CEvent = Object(base_global_timeline_CEventFields := {})

CCharClassAIAttackCheckFinishedEvent = Object(base_global_timeline_CEventFields)

CCharClassComponent = Object(CCharClassComponentFields := CActorComponentDefFields)


class EDamageType(enum.IntEnum):
    UNKNOWN = 0
    ELECTRIC = 1
    FIRE = 2
    BLOOD = 3
    STEAM = 4
    NO_DAMAGE = 5
    Invalid = 2147483647


construct_EDamageType = StrictEnum(EDamageType)


class EDamageStrength(enum.IntEnum):
    DEFAULT = 0
    MEDIUM = 1
    MEDIUM_HORIZONTAL = 2
    HARD_WITHOUT_SHAKE = 3
    HARD = 4
    SUPER_HARD = 5
    Invalid = 2147483647


construct_EDamageStrength = StrictEnum(EDamageStrength)

base_global_CRntSmallDictionary_base_global_CStrId__base_global_CStrId_ = common_types.make_dict(common_types.StrId, key=common_types.StrId)

CCharClassAttackComponent = Object(CCharClassAttackComponentFields := {
    **CCharClassComponentFields,
    "sDefaultDamageID": common_types.StrId,
    "sDamageSource": common_types.StrId,
    "bRotateToInstigatorHitCollider": construct.Flag,
    "eDamageType": construct_EDamageType,
    "sSuccessDownDefaultAnim": common_types.StrId,
    "sSuccessUpDefaultAnim": common_types.StrId,
    "sSuccessFrontDefaultAnim": common_types.StrId,
    "sSuccessBackDefaultAnim": common_types.StrId,
    "bIgnoreReaction": construct.Flag,
    "bForceReaction": construct.Flag,
    "eDamageStrengthOnForcedReaction": construct_EDamageStrength,
    "bIgnoreInmune": construct.Flag,
    "dictDamageIDOverrides": base_global_CRntSmallDictionary_base_global_CStrId__base_global_CStrId_,
    "sIgnoreBumpColliders": common_types.StrId,
})

CCharClassAIAttackComponent = Object(CCharClassAIAttackComponentFields := {
    **CCharClassAttackComponentFields,
    "bAllowFloorSlideTunnel": construct.Flag,
})

CCharClassAIAttackEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
    "fProbability": common_types.Float,
    "bPlayerOnViewDir": construct.Flag,
    "bCheckPlayerNotInvulnerable": construct.Flag,
    "bCheckPlayerInvulnerable": construct.Flag,
    "fCheckPlayerMaxDistance": common_types.Float,
    "fCheckPlayerMinDistance": common_types.Float,
    "fCheckPlayerMinUpDistance": common_types.Float,
    "fCheckPlayerMaxUpDistance": common_types.Float,
    "fCheckNavPathMaxDistance": common_types.Float,
    "fCheckNavPathMinDistance": common_types.Float,
    "iFrame": common_types.Int,
    "iBehaviorPresetMin": common_types.Int,
    "iBehaviorPresetMax": common_types.Int,
    "bCheckInCombat": construct.Flag,
})

CCharClassAIAttackNotificationEvent = Object(base_global_timeline_CEventFields)


class ENavigablePathType(enum.IntEnum):
    NONE = 0
    GROUND = 1
    STICKY = 2
    Invalid = 2147483647


construct_ENavigablePathType = StrictEnum(ENavigablePathType)


class ECutPathMode(enum.IntEnum):
    ALWAYS = 0
    ONLY_IN_CLOSE_CORNERS = 1
    Invalid = 2147483647


construct_ECutPathMode = StrictEnum(ECutPathMode)

std_unique_ptr_CEnemyPreset_ = Pointer_CEnemyPreset.create_construct()

base_global_CRntVector_std_unique_ptr_CEnemyPreset__ = common_types.make_vector(std_unique_ptr_CEnemyPreset_)

CStartDetectionPerceptionRuleSet = Object({
    **CPerceptionRuleSetFields,
    "eOverridedInFrustumMode": construct_EInFrustumMode,
    "fInstantDetectionFrontDistance": common_types.Float,
    "fInstantDetectionBackDistance": common_types.Float,
})

CExtendDetectionPerceptionRuleSet = Object({
    **CPerceptionRuleSetFields,
    "eOverridedInFrustumMode": construct_EInFrustumMode,
    "fInstantDetectionFrontDistance": common_types.Float,
    "fInstantDetectionBackDistance": common_types.Float,
})


class EXpawnAngPolicy(enum.IntEnum):
    SPAWNPOINT = 0
    TARGET_SIDE = 1
    TARGET_DIR = 2
    TARGET_OPPOSITE_SIDE = 3
    TARGET_OPPOSITE_DIR = 4
    Invalid = 2147483647


construct_EXpawnAngPolicy = StrictEnum(EXpawnAngPolicy)

SDeathImpactDisplacement = Object({
    "fInitialSpeed": common_types.Float,
    "fMidSpeed": common_types.Float,
    "fTimeToMidSpeed": common_types.Float,
    "fEndSpeed": common_types.Float,
})

CCharClassAIComponent = Object(CCharClassAIComponentFields := {
    **CCharClassComponentFields,
    "sDefeatedEnemyClass": common_types.StrId,
    "fChaseReachedDistance": common_types.Float,
    "fChaseMinDistance": common_types.Float,
    "fChaseMaxDistance": common_types.Float,
    "fChaseCenterDistance": common_types.Float,
    "fChaseMaxLaunchAngleDegs": common_types.Float,
    "fChaseProjectileRadius": common_types.Float,
    "fChaseDistanceToFreePoint": common_types.Float,
    "fMinSeparationFromPreviousRandomChaseCenter": common_types.Float,
    "bUseElectricAreaAttackFX": construct.Flag,
    "fElectricAreaAttackMaxDist": common_types.Float,
    "fShortDistance": common_types.Float,
    "fLongDistance": common_types.Float,
    "bUseTargetPos": construct.Flag,
    "bSuspendIfNotInFrustum": construct.Flag,
    "eInFrustumMode": construct_EInFrustumMode,
    "bWantsAdjustHeightOnMelee": construct.Flag,
    "bWantsMeleeCamera": construct.Flag,
    "fMeleeCameraMinExtraZDist": common_types.Float,
    "fMeleeCameraTime": common_types.Float,
    "fMeleeCounterCameraMinExtraZDist": common_types.Float,
    "sAutoLockOnColliderID": common_types.StrId,
    "bAutoLockOnColliderMissilesPredictEndPos": construct.Flag,
    "bWantsCoordinateAttacks": construct.Flag,
    "sCrazyEndAnim": common_types.StrId,
    "sCrazyFXNode": common_types.StrId,
    "vCrazyFXPositionOffset": common_types.CVector3D,
    "vCrazyFXRotationOffset": common_types.CVector3D,
    "fTargetReachableWidth": common_types.Float,
    "fTargetReachableHeight": common_types.Float,
    "fTargetReachableRadius": common_types.Float,
    "bTargetReachableRadiusIgnoreSegmentNormal": construct.Flag,
    "bReachableUseRadius": construct.Flag,
    "bCheckWeaponReachable": construct.Flag,
    "fReachableMaxSegmentDotToCut": common_types.Float,
    "fReachableSegmentCutDistance": common_types.Float,
    "sNavMeshSmartLinksGroup": common_types.StrId,
    "sDynamicSmartLinkRulesFile": common_types.StrId,
    "sDynamicNavigationRulesFile": common_types.StrId,
    "sNavMeshNavigationModes": common_types.StrId,
    "sNavMeshEnvironmentTypes": common_types.StrId,
    "sForbiddenNavigateOverNavMeshPolygonLogicTypeFlags": common_types.StrId,
    "sForbiddenNavigateInsideNavMeshPolygonLogicTypeFlags": common_types.StrId,
    "bAwaitOnTargetTunnelEntrances": construct.Flag,
    "sNavMeshGlobalSmartLinkTypes": common_types.StrId,
    "fVisitedNavMeshEdgesDistance": common_types.Float,
    "vNavMeshAStarExtraSize": common_types.CVector2D,
    "eNavigablePathType": construct_ENavigablePathType,
    "fMinYNormalInPath": common_types.Float,
    "fNavigablePathCutDistance": common_types.Float,
    "fNavigablePathCutDistanceInPathLimits": common_types.Float,
    "fNavigablePathCutDistanceWithWalls": common_types.Float,
    "vNavigablePathCharacterSize": common_types.CVector3D,
    "bNavigablePathCanStitchEdges": construct.Flag,
    "bCanApplyMeleeReactionKinematicMovementModifier": construct.Flag,
    "bWantsRotateOnMeleeCrazy": construct.Flag,
    "bGeneratePathInOpenDoors": construct.Flag,
    "eCutPathMode": construct_ECutPathMode,
    "tPresets": base_global_CRntVector_std_unique_ptr_CEnemyPreset__,
    "bAlwaysTargetDetected": construct.Flag,
    "bRequiresActivationPerception": construct.Flag,
    "oActivationPerceptionRuleSet": CActivationPerceptionRuleSet,
    "oStartDetectionPerceptionRuleSet": CStartDetectionPerceptionRuleSet,
    "oExtendDetectionPerceptionRuleSet": CExtendDetectionPerceptionRuleSet,
    "bStartDetectionRequiresLOS": construct.Flag,
    "bEndDetectionRequiresLOS": construct.Flag,
    "eDetectionLOSMode": construct_ELOSMode,
    "bStartDetectionRequiresTargetInFront": construct.Flag,
    "bEndDetectionRequiresTargetInFront": construct.Flag,
    "fStartMaxDistForTargetDetection": common_types.Float,
    "fEndMaxDistForTargetDetection": common_types.Float,
    "fTimeForTargetDetection": common_types.Float,
    "fTimeForTargetDetectionEnd": common_types.Float,
    "bStartShouldBeInFrustrumForTargetDetection": construct.Flag,
    "bEndShouldBeInFrustrumForTargetDetection": construct.Flag,
    "bStartShouldCheckIfTargetIsInAreaOfInterest": construct.Flag,
    "bEndShouldCheckIfTargetIsInAreaOfInterest": construct.Flag,
    "bUseStartAOIWhenEndAOIIsEmpty": construct.Flag,
    "bUseAlwaysEndAreaOfInterestAfterFirstDetection": construct.Flag,
    "bIsAreaOfInterestOptional": construct.Flag,
    "bStartShouldTargetBeReachableForDetection": construct.Flag,
    "bEndShouldTargetBeReachableForDetection": construct.Flag,
    "bStartCanSeeThroughOpticCamo": construct.Flag,
    "bEndCanSeeThroughOpticCamo": construct.Flag,
    "bForceTargetDetectionByOtherSpawnGroupMember": construct.Flag,
    "bResumeOtherSpawnGroupMembersOnTargetDetection": construct.Flag,
    "bAllowsTrespass": construct.Flag,
    "bForceOnCollisionStayProcess": construct.Flag,
    "tTrespassCollidersIds": base_global_CRntVector_base_global_CStrId_,
    "tTrespassCollidersTags": base_global_CRntVector_base_global_CStrId_,
    "bMeleeBigAIReaction": construct.Flag,
    "bAllowMultipleMeleeHits": construct.Flag,
    "bUsingDCCenter": construct.Flag,
    "fTargetOnGroundDist": common_types.Float,
    "fMinFlyingDistToFloor": common_types.Float,
    "fMotionSpeed": common_types.Float,
    "bIsReskin": construct.Flag,
    "bUpdatePathToTarget": construct.Flag,
    "bTweakWalkCyclesBeforeSmartLink": construct.Flag,
    "fMinNumWalkCyclesToTweak": common_types.Float,
    "fMaxNumWalkCyclesToTweak": common_types.Float,
    "fMinWalkKinematicDeltaFactor": common_types.Float,
    "fMaxWalkKinematicDeltaFactor": common_types.Float,
    "bPlayerCanJump": construct.Flag,
    "bUseNavmeshPath": construct.Flag,
    "bMeleeCameraFinishIfNotForcedCharge": construct.Flag,
    "fBlockableAttackWarningNoticeTime": common_types.Float,
    "fBlockableAttackWarningRadius": common_types.Float,
    "fBlockableAttackWarningVolume": common_types.Float,
    "sDefaultInvulnerableDamageMask": common_types.StrId,
    "sArmoredInvulnerableDamageMask": common_types.StrId,
    "sMorphingNode": common_types.StrId,
    "v3MorphingOffset": common_types.CVector3D,
    "eXpawnAngPolicy": construct_EXpawnAngPolicy,
    "fXCellMorphingEffectScale": common_types.Float,
    "sPushAnim": common_types.StrId,
    "sPushBackAnim": common_types.StrId,
    "bIgnoreRotateOnPush": construct.Flag,
    "bInvertRotateOnPush": construct.Flag,
    "fIgnoreShootsTime": common_types.Float,
    "fBackToNormalityTime": common_types.Float,
    "fBackToNormalityInMoreShootsTime": common_types.Float,
    "fDistanceToPathLimitInFlee": common_types.Float,
    "fDashMeleeLimitToAdd": common_types.Float,
    "oDeathImpactDisplacementDefault": SDeathImpactDisplacement,
    "oDeathImpactDisplacementStrong": SDeathImpactDisplacement,
    "bWantsForceBarelyFrozenDeath": construct.Flag,
    "bWantsForceScrewBounceOnDead": construct.Flag,
    "bIgnoreFleeTime": construct.Flag,
    "bSetNewParamsOnFlee": construct.Flag,
    "fFleeSpeed": common_types.Float,
    "fFleeAcceleration": common_types.Float,
    "fPatrolSpeed": common_types.Float,
    "fPatrolAcceleration": common_types.Float,
    "bWantsCauseBumpFXByDefault": construct.Flag,
    "bCheckSLWhenAttackEnds": construct.Flag,
    "fDistToDestroyProjectile": common_types.Float,
    "bAllowBlindAttackOnPush": construct.Flag,
    "sBlindAttackName": common_types.StrId,
    "bComputeSupportOnPath": construct.Flag,
    "fMinBackSpaceToOverrideMeleeAction": common_types.Float,
    "fMinDist2TargetToOverrideMeleeAction": common_types.Float,
})

CCharClassGrapplePointComponent = Object(CCharClassGrapplePointComponentFields := {
    **CCharClassComponentFields,
    "bAutoEnableGlow": construct.Flag,
    "sGrappleDragWide": common_types.StrId,
})

CCharClassPullableGrapplePointComponent = Object(CCharClassPullableGrapplePointComponentFields := {
    **CCharClassGrapplePointComponentFields,
    "sOnDestructionLeftTimeline": common_types.StrId,
    "sOnDestructionRightTimeline": common_types.StrId,
})

CCharClassAIGrapplePointComponent = Object({
    **CCharClassPullableGrapplePointComponentFields,
    "sGrappleCollider": common_types.StrId,
})


class EFollowPathRotationMode(enum.IntEnum):
    NONE = 0
    VerticalRotationToMovement = 1
    InvertVerticalRotationToMovement = 2
    PositiveVerticalRotationToMovement = 3
    NegativeVerticalRotationToMovement = 4
    HorizontalRotationToMovement = 5
    Invalid = 2147483647


construct_EFollowPathRotationMode = StrictEnum(EFollowPathRotationMode)

CCharClassAINavigationComponent = Object({
    **CCharClassComponentFields,
    "eFollowPathRotationMode": construct_EFollowPathRotationMode,
    "fFollowPathVerticalRotationDist": common_types.Float,
    "fFollowPathVerticalRotationFactor": common_types.Float,
    "fFollowPathTargetReachedDistance": common_types.Float,
    "fFollowPathLookAhead": common_types.Float,
    "bFollowPathUpdateDirWhenNotLookingAtDesiredViewDir": construct.Flag,
    "fGotoPointReachedDistance": common_types.Float,
    "fTurnWeightPenalization": common_types.Float,
})

CCharClassAINotificationEvent = Object(base_global_timeline_CEventFields)

CCharClassAISmartObjectComponent = Object({
    **CCharClassComponentFields,
    "fUseOffset": common_types.Float,
})

CCharClassAbilityComponent = Object(CCharClassComponentFields)

base_global_timeline_CTrack = Object(base_global_timeline_CTrackFields := {})

CCharClassAbortAttackOnSubareaChangeTrack = Object(base_global_timeline_CTrackFields)

CCharClassAbortTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassAbsorbTrack = Object(base_global_timeline_CTrackFields)

CCharClassUsableComponent = Object(CCharClassUsableComponentFields := {
    **CCharClassComponentFields,
    "fGrabInterpTime": common_types.Float,
    "fUseTime": common_types.Float,
    "sUseQuestionID": common_types.StrId,
    "sCanNotUseID": common_types.StrId,
    "sUseSuccessMessage": common_types.StrId,
    "sUsePrepareLeftAction": common_types.StrId,
    "sUsePrepareRightAction": common_types.StrId,
    "sUseInitAction": common_types.StrId,
    "sUseAction": common_types.StrId,
    "sUseLevelChangeAction": common_types.StrId,
    "sUseEndAction": common_types.StrId,
    "sUseIdleAction": common_types.StrId,
    "sUsablePrepareToUseAction": common_types.StrId,
    "sUsableInitAction": common_types.StrId,
    "sUsableAction": common_types.StrId,
    "sUsableLevelChangeAction": common_types.StrId,
    "sUsableEndAction": common_types.StrId,
    "sUsableIdleAction": common_types.StrId,
    "sUseDiscoverRightAction": common_types.StrId,
    "sUseDiscoverLeftAction": common_types.StrId,
    "sUsableDiscoverAction": common_types.StrId,
    "sUsableUndiscoverAction": common_types.StrId,
    "sUsePrepareLeftAfterDiscoverAction": common_types.StrId,
    "sUsePrepareRightAfterDiscoverAction": common_types.StrId,
    "sUseReadyToSaveBackgroundAction": common_types.StrId,
    "fDiscoverInterpTime": common_types.Float,
    "fStationUseInterpTime": common_types.Float,
    "fStationNotUsedInterpTime": common_types.Float,
    "sStartLevelMusicID": common_types.StrId,
    "sSaveSoundID": common_types.StrId,
    "fPostponeFadeInTime": common_types.Float,
    "fFadeInTime": common_types.Float,
})

CCharClassAccessPointComponent = Object({
    **CCharClassUsableComponentFields,
    "sUsePrepareLeftAPNoUsedAction": common_types.StrId,
    "sUsePrepareRightAPNoUsedAction": common_types.StrId,
    "sUseInitAPUsedAction": common_types.StrId,
    "sUseAPUsedAction": common_types.StrId,
    "sUsableInitAPUsedAction": common_types.StrId,
    "sSaveRingsOpenAction": common_types.StrId,
    "sSaveRingsCloseAction": common_types.StrId,
    "sSaveRingLoopAction": common_types.StrId,
    "sUsePrepareLeftAfterDiscoverNoDialogueAction": common_types.StrId,
    "sUsePrepareRightAfterDiscoverNoDialogueAction": common_types.StrId,
})

CCharClassActivatableComponent = Object(CCharClassActivatableComponentFields := CCharClassComponentFields)

CCharClassActionSwitcherComponent = Object({
    **CCharClassActivatableComponentFields,
    "sActivateAction": common_types.StrId,
    "sDeactivateAction": common_types.StrId,
    "bScalePlayRate": construct.Flag,
    "bDisableOnActivatedOnDeattachActor": construct.Flag,
})

CCharClassActionSwitcherOnPullGrapplePointComponent = Object({
    **CCharClassPullableGrapplePointComponentFields,
    "sGrappleCollider": common_types.StrId,
    "fGrappleMinAlignmentX": common_types.Float,
    "sActionOnGrappleAttach": common_types.StrId,
    "sActionOnPullStart": common_types.StrId,
    "sActionOnPullAbort": common_types.StrId,
    "sActionOnGrappleDetach": common_types.StrId,
})

CCharClassActivatableEntitiesEvent = Object({
    **base_global_timeline_CEventFields,
    "sIdActivation": common_types.StrId,
})

CCharClassActivateAutsharpEvent = Object({
    **base_global_timeline_CEventFields,
    "bRotateAutsharp": construct.Flag,
})

CCharClassActivateCaterzillaMovementEvent = Object(base_global_timeline_CEventFields)

CCharClassActivateHecathonFXEvent = Object(base_global_timeline_CEventFields)

CCharClassActivateTrainPortalEvent = Object({
    **base_global_timeline_CEventFields,
    "bIsleaving": construct.Flag,
})

CCharClassActiveMeleeIgnorePeacefulEnemyTrack = Object(base_global_timeline_CTrackFields)

CCharClassActiveRumbleOnMagnetSurfaceTrack = Object(base_global_timeline_CTrackFields)

CCharClassAddWeaponTimelineSuffixTrack = Object({
    **base_global_timeline_CTrackFields,
    "sSuffix": common_types.StrId,
})

CCharClassAffectsScrewAttackDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassAimCameraEnabledVisibleOnlyComponent = Object(CCharClassComponentFields)

CCharClassAimComponent = Object({
    **CCharClassComponentFields,
    "fAutoAimWidth": common_types.Float,
    "fAutoAimLength": common_types.Float,
    "fAutoAimConeLength": common_types.Float,
    "fAutoAimInterp": common_types.Float,
    "fAutoAimLockOnInterp": common_types.Float,
    "fAutoAimLockOnPredictionTime": common_types.Float,
    "fAutoAimLockAfterDeadTime": common_types.Float,
    "fMaxTimeMaintainingFront": common_types.Float,
    "fLaserDeactivationTime": common_types.Float,
    "fAnalogModeDefaultInterp": common_types.Float,
    "fForcedFrontTimeAfterFire": common_types.Float,
    "fForcedFrontTimeAfterFireOnAir": common_types.Float,
    "fForcedFrontTimeAfterDiagonal": common_types.Float,
    "fForcedFrontTimeAfterSecondaryWeapon": common_types.Float,
    "fForcedFrontTimeAfterStealthRun": common_types.Float,
    "fForcedFrontTimeAfterParkour": common_types.Float,
    "fForcedFrontTimeAfterFloorSlide45End": common_types.Float,
})

CCharClassAllowAlternativeActionsTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowAttackTrack = Object(base_global_timeline_CTrackFields)


class EActionInsertFlags(enum.IntEnum):
    IGNORE_PRIORITY = 0
    FORCE = 1
    LOCAL_TRANSFORM = 2
    CLEAR_ROOT_MOTION = 3
    CLEAR_ROOT_MOTION_IF_NO_ADVANCE = 4
    ACTIONSET_UPDATED = 5
    REPLACE_LOOPED = 6
    UPDATE_MODEL = 7
    USE_LAST_REMAINING_TIME = 8
    NEXT_ACTION = 9
    LAUNCH_EVENTS_ON_SYNC = 10
    RESET_STORED_ENTITY_TRANSFORM = 11
    RESET_STORED_ENTITY_TRANSFORM_TRANSLATION = 12
    START_EVENTS_ON_TICK = 13
    LAUNCH_NON_DISCARDABLES = 14
    NO_SET_SAME_ACTION_WITH_DIFFERENT_PREFIX = 15


construct_EActionInsertFlags = StrictEnum(EActionInsertFlags)

TActionInsertFlagset = construct.FlagsEnum(construct.Int32ul, construct_EActionInsertFlags.enum_class)

CCharClassTweakActionBaseTrack = Object(CCharClassTweakActionBaseTrackFields := {
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "bMaintainFrameUsePercentage": construct.Flag,
    "fToFrame": common_types.Float,
    "fBlendTime": common_types.Float,
    "oAditionalActionInsertFlags": TActionInsertFlagset,
})

CCharClassAllowChaseTransitionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassAllowConvertFromMorphBallDisplacementTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowCrazyEndTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassAllowCrazyTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowCrouchRepositionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sActionForward": common_types.StrId,
    "sActionBackward": common_types.StrId,
})

CCharClassAllowEarlyJumpOverHangTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowEndTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowFallendRepositionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sActionForward": common_types.StrId,
    "sActionBackward": common_types.StrId,
})

CCharClassAllowFleeWalkTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowGrazeTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowInterpolationTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowMeleeLimitsTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowNavigationRotationTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowParkourTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowPushTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowRootMotionInStoppedTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowSPBShotTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowShinesparkTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowSlowDownDutingGrabTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowSmartLinkCorrectionTrack = Object(base_global_timeline_CTrackFields)

CCharClassAllowSpeedBoosterTrack = Object({
    **base_global_timeline_CTrackFields,
    "bCanIncreaseTime": construct.Flag,
})

CCharClassAlternativeActionInitializeEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
    "fMinimumTimeToBeConsidered": common_types.Float,
    "fMinimumChanceToPlay": common_types.Float,
})

CCharClassAlternativeActionPlayEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
    "fChanceIncrementOnFail": common_types.Float,
    "fMaximumChanceIncrementOnFail": common_types.Float,
})


class CCharClassToStateTrack_EMaintainFrameMode(enum.IntEnum):
    Pct = 0
    Frame = 1
    Invalid = 2147483647


construct_CCharClassToStateTrack_EMaintainFrameMode = StrictEnum(CCharClassToStateTrack_EMaintainFrameMode)

CCharClassToStateTrack = Object(CCharClassToStateTrackFields := {
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "eMaintainFrameMode": construct_CCharClassToStateTrack_EMaintainFrameMode,
    "iFrame": common_types.Int,
    "bForce": construct.Flag,
    "fBlendTime": common_types.Float,
})

CCharClassAnalogAimActionTrack = Object(CCharClassToStateTrackFields)


class CCharClassAnalogAimTrack_EAbortAnalogAimInput(enum.IntEnum):
    NONE = 0
    Back = 1
    Any = 2
    Invalid = 2147483647


construct_CCharClassAnalogAimTrack_EAbortAnalogAimInput = StrictEnum(CCharClassAnalogAimTrack_EAbortAnalogAimInput)

CCharClassAnalogAimTrack = Object({
    **base_global_timeline_CTrackFields,
    "eAbortAnalogAimInput": construct_CCharClassAnalogAimTrack_EAbortAnalogAimInput,
})

CCharClassAnimSpeedTrack = Object({
    **base_global_timeline_CTrackFields,
    "fSpeedMultiplier": common_types.Float,
})

CCharClassAnimationComponent = Object({
    **CCharClassComponentFields,
    "bOverrideDisableInEditor": construct.Flag,
    "sInitialAction": common_types.StrId,
    "sDefaultLoop": common_types.StrId,
    "sAnimTree": common_types.StrId,
    "sInitialPrefix": construct_CAnimationPrefix_SPrefix_Enum,
    "iDebugLine": common_types.Int,
    "fInitialFrame": common_types.Float,
})


class ENavMeshItemType(enum.IntEnum):
    Static = 0
    Dynamic = 1
    Destructible = 2
    Invalid = 2147483647


construct_ENavMeshItemType = StrictEnum(ENavMeshItemType)

CCharClassNavMeshItemComponent = Object(CCharClassNavMeshItemComponentFields := {
    **CCharClassComponentFields,
    "sInitialStage": common_types.StrId,
    "eType": construct_ENavMeshItemType,
    "bConnectSubareas": construct.Flag,
})

CCharClassAnimationNavMeshItemComponent = Object({
    **CCharClassNavMeshItemComponentFields,
    "sAnimationId": common_types.StrId,
})

CCharClassApplyDC_ShinesparkLogicTrack = Object(base_global_timeline_CTrackFields)

CCharClassApplyGhostDashModelOffsetTrack = Object({
    **base_global_timeline_CTrackFields,
    "fDistance": common_types.Float,
})

CCharClassApplyGrabPositionOffsetTrack = Object(base_global_timeline_CTrackFields)

CCharClassApplyMeleeLimitsTrack = Object(base_global_timeline_CTrackFields)

CCharClassApplyMeleeMovementToEnemyTrack = Object(base_global_timeline_CTrackFields)

CCharClassApplyNoJumpingGravityFactorTrack = Object(base_global_timeline_CTrackFields)

CCharClassApplyShootReactionTrack = Object(base_global_timeline_CTrackFields)

CCharClassBehaviorTreeAIComponent = Object(CCharClassBehaviorTreeAIComponentFields := {
    **CCharClassAIComponentFields,
    "sBehaviorTreePath": common_types.StrId,
    "fMaxCrazyTime": common_types.Float,
})

CCharClassArachnusAIComponent = Object(CCharClassBehaviorTreeAIComponentFields)

CCharClassAreaFXComponent = Object({
    **CCharClassComponentFields,
    "sModelResPath": common_types.StrId,
    "fScale": common_types.Float,
    "fScaleRandom": common_types.Float,
    "vRotation": common_types.CVector3D,
    "vRotationRandom": common_types.CVector3D,
    "fFXAttackLenght": common_types.Float,
    "bUseInstances": construct.Flag,
})

CCharClassAreaMusicComponent = Object(CCharClassComponentFields)

CCharClassBaseTriggerComponent = Object(CCharClassBaseTriggerComponentFields := CCharClassActivatableComponentFields)

CCharClassSoundTriggerComponent = Object(CCharClassSoundTriggerComponentFields := CCharClassBaseTriggerComponentFields)

CCharClassAreaSoundComponent = Object({
    **CCharClassSoundTriggerComponentFields,
    "bOverrideDisableInEditor": construct.Flag,
})

CCharClassAreaSoundEffectsComponent = Object(CCharClassComponentFields)

std_unique_ptr_CAttackPreset_ = Pointer_CAttackPreset.create_construct()

base_global_CRntVector_std_unique_ptr_CAttackPreset__ = common_types.make_vector(std_unique_ptr_CAttackPreset_)

CCharClassAttack = Object(CCharClassAttackFields := {
    "tPresets": base_global_CRntVector_std_unique_ptr_CAttackPreset__,
    "sAttackAnim": common_types.StrId,
    "sName": common_types.StrId,
    "bCheckInFrustum": construct.Flag,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
    "bCheckTargetReachable": construct.Flag,
    "bCheckTargetDetected": construct.Flag,
    "bCheckTargetNotInvulnerable": construct.Flag,
    "bCheckViewDirection": construct.Flag,
    "bCheckNotViewDirection": construct.Flag,
    "bUpdateAttackWhileFrozen": construct.Flag,
    "bFreezeEndsAttack": construct.Flag,
    "sCancelAttackAnim": common_types.StrId,
    "sAttackOnEndTimeline": common_types.StrId,
    "fMinTimeBossInCombatToAttack": common_types.Float,
    "iMaxToRepeat": common_types.Int,
    "iMaxWithoutLaunch": common_types.Int,
    "fMinTimeToReachDesiredAttackPos": common_types.Float,
    "fChaseCenterDistance": common_types.Float,
    "fMinTimeSinceLastGrab": common_types.Float,
    "bCheckTargetOnFloor": construct.Flag,
    "bCheckNotTurning": construct.Flag,
    "fTimeSinceLastFrozen": common_types.Float,
    "bCheckInSubarea": construct.Flag,
})

CCharClassAttackCanBeAbortedTrack = Object(base_global_timeline_CTrackFields)

CCharClassAttackComponent_CTunableCharClassAttackComponent = Object({
    **base_tunable_CTunableFields,
    "fDamageArmadiggerDashAttack": common_types.Float,
    "fDamageArmadiggerDefault": common_types.Float,
    "fDamageAutclastDefault": common_types.Float,
    "fDamageAutclastExplosion": common_types.Float,
    "fDamageAutectorDefault": common_types.Float,
    "fDamageAutectorExplosion": common_types.Float,
    "fDamageAutomperAutomaticIrradiation": common_types.Float,
    "fDamageAutomperDefault": common_types.Float,
    "fDamageAutoolDefault": common_types.Float,
    "fDamageAutsharpDefault": common_types.Float,
    "fDamageAutsharpExplosionDefault": common_types.Float,
    "fDamageAutsniperDefault": common_types.Float,
    "fDamageAutsniperLaserDefault": common_types.Float,
    "fDamageBatalloonDefault": common_types.Float,
    "fDamageBigfistDefault": common_types.Float,
    "fDamageBigfistMelee": common_types.Float,
    "fDamageBigkranXDefault": common_types.Float,
    "fDamageBigkranXMagmaBall": common_types.Float,
    "fDamageBlindFlyAttack": common_types.Float,
    "fDamageBlindFlyDefault": common_types.Float,
    "fDamageCaterzillaDefault": common_types.Float,
    "fDamageCentralUnitCannonBeamCaves": common_types.Float,
    "fDamageCentralUnitCannonBeamForest": common_types.Float,
    "fDamageCentralUnitCannonBeamLab": common_types.Float,
    "fDamageCentralUnitCannonBeamMagma": common_types.Float,
    "fDamageCentralUnitCannonBeamSanc": common_types.Float,
    "fDamageCentralUnitCannonDefault": common_types.Float,
    "fDamageCentralUnitDefault": common_types.Float,
    "fDamageChozoCommanderAirCharge": common_types.Float,
    "fDamageChozoCommanderAuraScratch": common_types.Float,
    "fDamageChozoCommanderDefault": common_types.Float,
    "fDamageChozoCommanderEnergyShardsFragment": common_types.Float,
    "fDamageChozoCommanderEnergyShardsSphere": common_types.Float,
    "fDamageChozoCommanderHyperspark": common_types.Float,
    "fDamageChozoCommanderKiStrike": common_types.Float,
    "fDamageChozoCommanderLandingSlam": common_types.Float,
    "fDamageChozoCommanderLaserZero": common_types.Float,
    "fDamageChozoCommanderLaserZeroGrounded": common_types.Float,
    "fDamageChozoCommanderPowerPulse": common_types.Float,
    "fDamageChozoCommanderSentenceSphere": common_types.Float,
    "fDamageChozoCommanderTriCombo": common_types.Float,
    "fDamageChozoCommanderTriComboNoDamage": common_types.Float,
    "fDamageChozoRobotSoldierCannonShot": common_types.Float,
    "fDamageChozoRobotSoldierCannonShotCharged": common_types.Float,
    "fDamageChozoRobotSoldierCannonShotChargedElite": common_types.Float,
    "fDamageChozoRobotSoldierCannonShotElite": common_types.Float,
    "fDamageChozoRobotSoldierDashSlash": common_types.Float,
    "fDamageChozoRobotSoldierDashSlashElite": common_types.Float,
    "fDamageChozoRobotSoldierDefault": common_types.Float,
    "fDamageChozoRobotSoldierDefaultElite": common_types.Float,
    "fDamageChozoRobotSoldierDisruptionField": common_types.Float,
    "fDamageChozoRobotSoldierDisruptionFieldElite": common_types.Float,
    "fDamageChozoRobotSoldierExplosion": common_types.Float,
    "fDamageChozoRobotSoldierExplosionElite": common_types.Float,
    "fDamageChozoRobotSoldierUppercut": common_types.Float,
    "fDamageChozoRobotSoldierUppercutElite": common_types.Float,
    "fDamageChozoWarriorDefault": common_types.Float,
    "fDamageChozoWarriorEliteDefault": common_types.Float,
    "fDamageChozoWarriorEliteGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorEliteGlaiveWalljump": common_types.Float,
    "fDamageChozoWarriorEliteShieldPush": common_types.Float,
    "fDamageChozoWarriorGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorGlaiveWalljump": common_types.Float,
    "fDamageChozoWarriorShieldPush": common_types.Float,
    "fDamageChozoWarriorWeakDefault": common_types.Float,
    "fDamageChozoWarriorWeakGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorWeakGlaiveWalljump": common_types.Float,
    "fDamageChozoWarriorWeakShieldPush": common_types.Float,
    "fDamageChozoWarriorXChangeWall": common_types.Float,
    "fDamageChozoWarriorXDefault": common_types.Float,
    "fDamageChozoWarriorXEliteChangeWall": common_types.Float,
    "fDamageChozoWarriorXEliteDefault": common_types.Float,
    "fDamageChozoWarriorXEliteGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorXEliteLandSplat": common_types.Float,
    "fDamageChozoWarriorXEliteLandSplatWaves": common_types.Float,
    "fDamageChozoWarriorXEliteSpit": common_types.Float,
    "fDamageChozoWarriorXEliteWallclimb": common_types.Float,
    "fDamageChozoWarriorXGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorXLandSplat": common_types.Float,
    "fDamageChozoWarriorXLandSplatWaves": common_types.Float,
    "fDamageChozoWarriorXSpit": common_types.Float,
    "fDamageChozoWarriorXWallclimb": common_types.Float,
    "fDamageChozoWarriorXWeakChangeWall": common_types.Float,
    "fDamageChozoWarriorXWeakDefault": common_types.Float,
    "fDamageChozoWarriorXWeakGlaiveSpin": common_types.Float,
    "fDamageChozoWarriorXWeakLandSplat": common_types.Float,
    "fDamageChozoWarriorXWeakLandSplatWaves": common_types.Float,
    "fDamageChozoWarriorXWeakSpit": common_types.Float,
    "fDamageChozoWarriorXWeakWallclimb": common_types.Float,
    "fDamageChozoZombieXDefault": common_types.Float,
    "fDamageChozoZombieXPoisonClaws": common_types.Float,
    "fDamageCooldownXBossDefault": common_types.Float,
    "fDamageCooldownXBossFireBall": common_types.Float,
    "fDamageCooldownXBossLaser": common_types.Float,
    "fDamageCooldownXBossLaserBite": common_types.Float,
    "fDamageCooldownXBossLavaCarpet": common_types.Float,
    "fDamageCooldownXBossLavaCarpetPuddles": common_types.Float,
    "fDamageCooldownXBossLavaDrop": common_types.Float,
    "fDamageCooldownXBossReaper": common_types.Float,
    "fDamageCooldownXBossStrongWhip": common_types.Float,
    "fDamageCooldownXBossWindTunnelWall": common_types.Float,
    "fDamageCoreXDefault": common_types.Float,
    "fDamageCoreXSuperQuetzoaDefault": common_types.Float,
    "fDamageDaivoDefault": common_types.Float,
    "fDamageDaivoSwarmIndividual": common_types.Float,
    "fDamageDaivoSwarmMax": common_types.Float,
    "fDamageDaivoSwarmMin": common_types.Float,
    "fDamageDaivoSwarmRadius": common_types.Float,
    "fDamageDepthornBall": common_types.Float,
    "fDamageDepthornDefault": common_types.Float,
    "fDamageDizzeanIndividual": common_types.Float,
    "fDamageDizzeanMax": common_types.Float,
    "fDamageDizzeanMin": common_types.Float,
    "fDamageDizzeanRadius": common_types.Float,
    "fDamageDredhedDefault": common_types.Float,
    "fDamageDredhedDiveAttack": common_types.Float,
    "fDamageDropterDefault": common_types.Float,
    "fDamageDropterDiveAttack": common_types.Float,
    "fDamageEmmyDefault": common_types.Float,
    "fDamageEmmyIce": common_types.Float,
    "fDamageEmmyWave": common_types.Float,
    "fDamageFingIndividual": common_types.Float,
    "fDamageFingMax": common_types.Float,
    "fDamageFingMin": common_types.Float,
    "fDamageFingRadius": common_types.Float,
    "fDamageFulmiteBellyMineDefault": common_types.Float,
    "fDamageFulmiteBellyMineExplosionDefault": common_types.Float,
    "fDamageFulmiteDefault": common_types.Float,
    "fDamageGobblerBite": common_types.Float,
    "fDamageGobblerChozoWarriorXBite": common_types.Float,
    "fDamageGobblerChozoWarriorXDefault": common_types.Float,
    "fDamageGobblerCooldownXBite": common_types.Float,
    "fDamageGobblerCooldownXDefault": common_types.Float,
    "fDamageGobblerDefault": common_types.Float,
    "fDamageGobblerHydrogigaBite": common_types.Float,
    "fDamageGobblerHydrogigaDefault": common_types.Float,
    "fDamageGobblerKraidBite": common_types.Float,
    "fDamageGobblerKraidDefault": common_types.Float,
    "fDamageGobblerScorpiusBite": common_types.Float,
    "fDamageGobblerScorpiusDefault": common_types.Float,
    "fDamageGobblerSuperGoliathBite": common_types.Float,
    "fDamageGobblerSuperGoliathDefault": common_types.Float,
    "fDamageGobblerSuperQuetzoaBite": common_types.Float,
    "fDamageGobblerSuperQuetzoaDefault": common_types.Float,
    "fDamageGoliathDefault": common_types.Float,
    "fDamageGoliathMelee": common_types.Float,
    "fDamageGoliathShockWave": common_types.Float,
    "fDamageGooplotDefault": common_types.Float,
    "fDamageGooplotJump": common_types.Float,
    "fDamageGooshockerDefault": common_types.Float,
    "fDamageGooshockerShock": common_types.Float,
    "fDamageGroundShockerDefault": common_types.Float,
    "fDamageGroundShockerElectric": common_types.Float,
    "fDamageHecathonDefault": common_types.Float,
    "fDamageHecathonPlanktonDefault": common_types.Float,
    "fDamageHydrogigaBraid": common_types.Float,
    "fDamageHydrogigaDefault": common_types.Float,
    "fDamageHydrogigaMaelstorm": common_types.Float,
    "fDamageHydrogigaPolyps": common_types.Float,
    "fDamageHydrogigaTongueSwirl": common_types.Float,
    "fDamageIcefleaDefault": common_types.Float,
    "fDamageIcefleaDiveAttack": common_types.Float,
    "fDamageIcefleaFreezeTick": common_types.Float,
    "fDamageInfesterBallDefault": common_types.Float,
    "fDamageInfesterBallExplosionDefault": common_types.Float,
    "fDamageInfesterDefault": common_types.Float,
    "fDamageKlaidaDefault": common_types.Float,
    "fDamageKraidAcidBlobs": common_types.Float,
    "fDamageKraidBackSlap": common_types.Float,
    "fDamageKraidBouncingCreatures": common_types.Float,
    "fDamageKraidDefault": common_types.Float,
    "fDamageKraidFierceSwipe": common_types.Float,
    "fDamageKraidInsideBelly": common_types.Float,
    "fDamageKraidShockerSplash": common_types.Float,
    "fDamageKraidSpikes": common_types.Float,
    "fDamageKraidSpinningNails": common_types.Float,
    "fDamageKreepDefault": common_types.Float,
    "fDamageNailongDefault": common_types.Float,
    "fDamageNailongThorn": common_types.Float,
    "fDamageNailuggerDefault": common_types.Float,
    "fDamageNailuggerSpit": common_types.Float,
    "fDamageObsydomithonAttack": common_types.Float,
    "fDamageObsydomithonDefault": common_types.Float,
    "fDamageOmnithonDefault": common_types.Float,
    "fDamageOmnithonPlanktonDefault": common_types.Float,
    "fDamagePoisonFlyAttack": common_types.Float,
    "fDamagePoisonFlyDefault": common_types.Float,
    "fDamageQuetshockerCharge": common_types.Float,
    "fDamageQuetshockerDefault": common_types.Float,
    "fDamageQuetshockerEnergyWave": common_types.Float,
    "fDamageQuetshockerEnergyWaveElectrify": common_types.Float,
    "fDamageQuetzoaCharge": common_types.Float,
    "fDamageQuetzoaDefault": common_types.Float,
    "fDamageRedenkiIndividual": common_types.Float,
    "fDamageRedenkiMax": common_types.Float,
    "fDamageRedenkiMin": common_types.Float,
    "fDamageRedenkiRadius": common_types.Float,
    "fDamageRinkaCaves": common_types.Float,
    "fDamageRinkaDefault": common_types.Float,
    "fDamageRinkaForest": common_types.Float,
    "fDamageRinkaLab": common_types.Float,
    "fDamageRinkaMagma": common_types.Float,
    "fDamageRinkaSanc": common_types.Float,
    "fDamageRockDiverDefault": common_types.Float,
    "fDamageRodomithonXDefault": common_types.Float,
    "fDamageRodomithonXFireCone": common_types.Float,
    "fDamageRodotukDefault": common_types.Float,
    "fDamageSabotoruDefault": common_types.Float,
    "fDamageSakaiDefault": common_types.Float,
    "fDamageSakaiDiveAttack": common_types.Float,
    "fDamageSclawkDefault": common_types.Float,
    "fDamageScorpiusDefault": common_types.Float,
    "fDamageScorpiusDefensiveSpikeBallPrick": common_types.Float,
    "fDamageScorpiusDragSpikeBall": common_types.Float,
    "fDamageScorpiusPoisonousGas": common_types.Float,
    "fDamageScorpiusPoisonousSpit": common_types.Float,
    "fDamageScorpiusSpikeBallPrick": common_types.Float,
    "fDamageScorpiusTailSmash": common_types.Float,
    "fDamageScorpiusWhiplash": common_types.Float,
    "fDamageScourgeDefault": common_types.Float,
    "fDamageScourgeTongueSlash": common_types.Float,
    "fDamageShakernautDefault": common_types.Float,
    "fDamageShakernautGroundshockDefault": common_types.Float,
    "fDamageShakernautLaserDefault": common_types.Float,
    "fDamageSharpawDefault": common_types.Float,
    "fDamageSharpawDiveAttack": common_types.Float,
    "fDamageShelmitDefault": common_types.Float,
    "fDamageShelmitExplosion": common_types.Float,
    "fDamageShelmitNakedDefault": common_types.Float,
    "fDamageShelmitNakedExplosion": common_types.Float,
    "fDamageShelmitPlasmaRay": common_types.Float,
    "fDamageShineonDefault": common_types.Float,
    "fDamageSlidleDefault": common_types.Float,
    "fDamageSluggerAcidBall": common_types.Float,
    "fDamageSluggerDefault": common_types.Float,
    "fDamageSpitclawkAcid": common_types.Float,
    "fDamageSpitclawkDefault": common_types.Float,
    "fDamageSpittailAcid": common_types.Float,
    "fDamageSpittailAcidBall": common_types.Float,
    "fDamageSpittailDefault": common_types.Float,
    "fDamageSunnapDefault": common_types.Float,
    "fDamageSuperGoliathBurstProjectionBomb": common_types.Float,
    "fDamageSuperGoliathBurstProjectionTracker": common_types.Float,
    "fDamageSuperGoliathDefault": common_types.Float,
    "fDamageSuperGoliathMelee": common_types.Float,
    "fDamageSuperGoliathShockWave": common_types.Float,
    "fDamageSuperQuetzoaCharge": common_types.Float,
    "fDamageSuperQuetzoaDefault": common_types.Float,
    "fDamageSuperQuetzoaEnergyWave": common_types.Float,
    "fDamageSuperQuetzoaEnergyWaveElectrify": common_types.Float,
    "fDamageSuperQuetzoaMultiTarget": common_types.Float,
    "fDamageSwifterDefault": common_types.Float,
    "fDamageTakumakuDashAttack": common_types.Float,
    "fDamageTakumakuDefault": common_types.Float,
    "fDamageVulkranDefault": common_types.Float,
    "fDamageVulkranMagmaBall": common_types.Float,
    "fDamageWarLotusDefault": common_types.Float,
    "fDamageYampaBite": common_types.Float,
    "fDamageYampaDefault": common_types.Float,
    "fDamageYampaStep": common_types.Float,
    "fDamageYamplotXBite": common_types.Float,
    "fDamageYamplotXDefault": common_types.Float,
    "fDamageYamplotXStep": common_types.Float,
})

CCharClassAttackFailActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "fSyncBlockWindowTime": common_types.Float,
    "sSyncBlockAction": common_types.StrId,
    "sSyncBlockNoGrabAction": common_types.StrId,
    "sCollider": common_types.StrId,
})

CCharClassAttackFailTrack = Object(base_global_timeline_CTrackFields)

CCharClassAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassAudioComponent = Object({
    **CCharClassComponentFields,
    "bDimSounds": construct.Flag,
    "bMuteOutsideCamera": construct.Flag,
})

CCharClassRobotAIComponent = Object(CCharClassRobotAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "sBumpedFX": common_types.StrId,
    "sDeathTimeline": common_types.StrId,
})

CCharClassAutclastChargeAttack = Object(CCharClassAttackFields)

CCharClassAutclastAIComponent = Object({
    **CCharClassRobotAIComponentFields,
    "oAutclastChargeAttackDef": CCharClassAutclastChargeAttack,
})

CCharClassAutclastAIComponent_CTunableCharClassAutclastAIComponent = Object({
    **base_tunable_CTunableFields,
    "iMaxExplosions": common_types.Int,
    "fTimeBetweenExplosions": common_types.Float,
    "fExplosionWidth": common_types.Float,
    "fMaxExplosionHeightOnGround": common_types.Float,
    "fMaxExplosionHeightOnWall": common_types.Float,
    "fMaxExplosionHeightOnCeilling": common_types.Float,
    "fExplosionHeightStartAttackOffset": common_types.Float,
    "fMinExplosionHeight": common_types.Float,
    "fAttackRecoveryTime": common_types.Float,
    "fExplosionDamage": common_types.Float,
    "fExplosionDuration": common_types.Float,
    "fMaxDistToAttack": common_types.Float,
    "fMaxPropagationHeight": common_types.Float,
    "fMinDistToSlope": common_types.Float,
    "fBaseRotationEffectFactor": common_types.Float,
})

CCharClassAutectorAIComponent = Object(CCharClassRobotAIComponentFields)

CCharClassAutectorAIComponent_CTunableCharClassAutectorAIComponent = Object({
    **base_tunable_CTunableFields,
    "fExplosionRadius": common_types.Float,
    "fTimeToExplosion": common_types.Float,
    "fTimeAtMaxRadiusExplosion": common_types.Float,
    "bCanBeSpawned": construct.Flag,
})

CCharClassAutectorChangeColliderEvent = Object(base_global_timeline_CEventFields)

CCharClassAutectorExplosionEvent = Object(base_global_timeline_CEventFields)

CCharClassLifeComponent = Object(CCharClassLifeComponentFields := {
    **CCharClassComponentFields,
    "sLife": common_types.StrId,
    "sImpactAnim": common_types.StrId,
    "sImpactBackAnim": common_types.StrId,
    "sDeadAnim": common_types.StrId,
    "sDeadBackAnim": common_types.StrId,
    "sDeadAirAnim": common_types.StrId,
    "sDeadAirBackAnim": common_types.StrId,
    "sDeadMeleeAnim": common_types.StrId,
    "sDeadNoInstigatorAnim": common_types.StrId,
    "bDisableCollidersOnDead": construct.Flag,
})

CDamageSourceFactor = Object({
    "fPowerBeamFactor": common_types.Float,
    "fWideBeamFactor": common_types.Float,
    "fPlasmaBeamFactor": common_types.Float,
    "fWaveBeamFactor": common_types.Float,
    "fGrappleBeamFactor": common_types.Float,
    "fHyperBeamFactor": common_types.Float,
    "fChargePowerBeamFactor": common_types.Float,
    "fChargeWideBeamFactor": common_types.Float,
    "fChargePlasmaBeamFactor": common_types.Float,
    "fChargeWaveBeamFactor": common_types.Float,
    "fMeleeChargePowerBeamFactor": common_types.Float,
    "fMeleeChargeWideBeamFactor": common_types.Float,
    "fMeleeChargePlasmaBeamFactor": common_types.Float,
    "fMeleeChargeWaveBeamFactor": common_types.Float,
    "fMissileFactor": common_types.Float,
    "fSuperMissileFactor": common_types.Float,
    "fIceMissileFactor": common_types.Float,
    "fMultiLockonMissileFactor": common_types.Float,
    "fBombFactor": common_types.Float,
    "fLineBombFactor": common_types.Float,
    "fPowerBombFactor": common_types.Float,
    "fScrewAttackFactor": common_types.Float,
    "fDashMeleeFactor": common_types.Float,
    "fSpeedBoosterFactor": common_types.Float,
    "fShineSparkFactor": common_types.Float,
})

CCharClassEnemyLifeComponent = Object(CCharClassEnemyLifeComponentFields := {
    **CCharClassLifeComponentFields,
    "oDamageSourceFactor": CDamageSourceFactor,
    "bShouldDieWithPowerBomb": construct.Flag,
    "fDamageFXTime": common_types.Float,
    "fMinTimeBetweenDamageSoundCallback": common_types.Float,
    "fMaxTimeBetweenDamageSoundCallback": common_types.Float,
    "bIgnoreRotateToInstigator": construct.Flag,
    "bShowLifeBar": construct.Flag,
    "vLifeBarOffset": common_types.CVector3D,
    "sDamageTimeline": common_types.StrId,
    "sDamageSFXTimeline": common_types.StrId,
    "bDashMeleeAppliesNonLethalDamage": construct.Flag,
})

CCharClassAutectorLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassAutoLockOnForbiddenTrack = Object(base_global_timeline_CTrackFields)

CCharClassAutoaimProjectile3DTrack = Object(base_global_timeline_CTrackFields)

CCharClassAutoexplodeProjectile3DTrack = Object(base_global_timeline_CTrackFields)

CCharClassAutomperAutomaticIrradiationAttack = Object({
    **CCharClassAttackFields,
    "fAttackDuration": common_types.Float,
    "fChargeDuration": common_types.Float,
})

CCharClassAutomperAIComponent = Object({
    **CCharClassRobotAIComponentFields,
    "oAutomperAutomaticIrradiationAttackDef": CCharClassAutomperAutomaticIrradiationAttack,
})

CCharClassAutoolAIComponent = Object(CCharClassRobotAIComponentFields)

CCharClassAutoolAIComponent_CTunableCharClassAutoolAIComponent = Object({
    **base_tunable_CTunableFields,
    "bRepairEnabled": construct.Flag,
    "fExtraTimeAfterKill": common_types.Float,
    "fRandTimeFirstSpawnMin": common_types.Float,
    "fRandTimeFirstSpawnMax": common_types.Float,
    "fBrakeDistance": common_types.Float,
    "fMinSpeed": common_types.Float,
    "fMaxInclination": common_types.Float,
    "fReachedDistance": common_types.Float,
    "fMaxAcceleration": common_types.Float,
    "fMinAcceleration": common_types.Float,
    "fMotionSpeed": common_types.Float,
})

CCharClassAutoolBottomThrusterFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "eThrusterMode": construct_CAutoolAIComponent_EThrusterMode,
})

CCharClassAutoolLeftThrusterFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "eThrusterMode": construct_CAutoolAIComponent_EThrusterMode,
})

CCharClassAutoolRightThrusterFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "eThrusterMode": construct_CAutoolAIComponent_EThrusterMode,
})

CCharClassAutsharpAIComponent = Object({
    **CCharClassRobotAIComponentFields,
    "fExplosionRadius": common_types.Float,
    "fTimeToExplosion": common_types.Float,
    "fTimeAtMaxRadiusExplosion": common_types.Float,
    "fDamageAutsharpExplosion": common_types.Float,
    "fTimeToPrepareExplosion": common_types.Float,
    "fRotationAccelTime": common_types.Float,
    "fRotationMultiplier": common_types.Float,
    "fAccelIncrementation": common_types.Float,
    "fTimeToDecelerate": common_types.Float,
    "fJumpUpImpulse": common_types.Float,
    "fJumpFrontImpulse": common_types.Float,
    "bIncrementRotationInJump": construct.Flag,
})

CCharClassAutsharpAIComponent_CTunableCharClassAutsharpAIComponent = Object({
    **base_tunable_CTunableFields,
    "bCanBeSpawned": construct.Flag,
    "fDistanceToDetectMagnet": common_types.Float,
    "fTimeToPrepareExplosion": common_types.Float,
    "fRotationInc": common_types.Float,
    "fRotationMultiplier": common_types.Float,
})

CCharClassAutsharpLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassAutsharpSPInitMovementEvent = Object(base_global_timeline_CEventFields)

CCharClassAutsniperShootAttack = Object({
    **CCharClassAttackFields,
    "fTimeToReload": common_types.Float,
    "fTimeToChargeRay": common_types.Float,
    "fTimeToUnchargeRay": common_types.Float,
    "fTimeToRelocateCannon": common_types.Float,
    "fTimeBeforeShoot": common_types.Float,
    "fTimeAfterShoot": common_types.Float,
    "fMaxPitch": common_types.Float,
    "fMinPitch": common_types.Float,
    "fMaxVolume": common_types.Float,
    "fMinVolume": common_types.Float,
    "fTimeCannonLocked": common_types.Float,
    "fTimeToGoPatrol": common_types.Float,
    "fTimeToLoseTarget": common_types.Float,
    "fDistToStopCloseToTarget": common_types.Float,
    "fTimeBeforeBlockeableWarning": common_types.Float,
    "fTimeAfterBlockeableWarning": common_types.Float,
})

CCharClassAutsniperAIComponent = Object({
    **CCharClassRobotAIComponentFields,
    "oAutsniperShootAttackDef": CCharClassAutsniperShootAttack,
    "fTimeToChangeLayer": common_types.Float,
    "fMovementFactor": common_types.Float,
})

CCharClassAutsniperChangeDirectionEvent = Object(base_global_timeline_CEventFields)

CCharClassAutsniperInvertAngleEvent = Object(base_global_timeline_CEventFields)

CCharClassBackAimSnapsToVerticalAxisTrack = Object(base_global_timeline_CTrackFields)

CCharClassBossAIComponent = Object(CCharClassBossAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "bUseIsInFrustumForBossCamera": construct.Flag,
    "bUseAngry": construct.Flag,
    "bManuallyRemoveFromTeamManager": construct.Flag,
    "bWantsLifeFeedback": construct.Flag,
    "bRemovePlayerInputOnDeath": construct.Flag,
    "bSetPlayerInvulnerableWithReactionOnDeath": construct.Flag,
    "bOpenDoorWhenDie": construct.Flag,
    "sBossBattleLabel": common_types.StrId,
    "sInventoryItemOnKilled": common_types.StrId,
    "bCheckOrientationInGrab": construct.Flag,
    "bPersistenBossDefeatedPushSetup": construct.Flag,
    "bGiveInventoryItemOnDead": construct.Flag,
})

CCharClassBaseBigFistAIComponent = Object(CCharClassBaseBigFistAIComponentFields := {
    **CCharClassBossAIComponentFields,
    "fMaxHeightAttackBehindDist": common_types.Float,
    "fMaxHeightAttackFrontalDist": common_types.Float,
})

CCharClassBaseDamageTriggerComponent = Object(CCharClassBaseDamageTriggerComponentFields := CCharClassBaseTriggerComponentFields)

CCharClassBaseFadeInEvent = Object(CCharClassBaseFadeInEventFields := {
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
    "fDelay": common_types.Float,
    "fR": common_types.Float,
    "fG": common_types.Float,
    "fB": common_types.Float,
})

CCharClassBaseGroundShockerAIComponent = Object(CCharClassBaseGroundShockerAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "fDefaultMotionSpeed": common_types.Float,
    "fCombatMotionSpeed": common_types.Float,
    "fFleeMotionSpeed": common_types.Float,
})

CCharClassBasicLifeComponent = Object(CCharClassBasicLifeComponentFields := {
    **CCharClassLifeComponentFields,
    "oDamageSourceFactor": CDamageSourceFactor,
    "bDestroyOnDead": construct.Flag,
    "fInitialDamageFactor": common_types.Float,
    "fInitialDamageFactorTime": common_types.Float,
})

CCharClassBatalloonAIComponent = Object({
    **CCharClassBaseGroundShockerAIComponentFields,
    "fCallDistMaxDelayTime": common_types.Float,
    "fCallDistLimit": common_types.Float,
    "fCallRandMinDelayTime": common_types.Float,
    "fCallRandMaxDelayTime": common_types.Float,
    "fRandMinTimeForPathUpdate": common_types.Float,
    "fRandMaxTimeForPathUpdate": common_types.Float,
    "fDotNegativeMaxTimeForPathUpdate": common_types.Float,
    "fMovementShakeRadius": common_types.Float,
    "fMovementShakeInterpolationSpeed": common_types.Float,
    "fBrothersDist2Stop": common_types.Float,
})

CCharClassItemLifeComponent = Object(CCharClassItemLifeComponentFields := {
    **CCharClassLifeComponentFields,
    "oDamageSourceFactor": CDamageSourceFactor,
    "iHitCount": common_types.Int,
})

CCharClassBeamBoxComponent = Object(CCharClassItemLifeComponentFields)

CCharClassBeamDoorDestroyedEvent = Object(base_global_timeline_CEventFields)

CCharClassBigFistAttack = Object(CCharClassAttackFields)

CCharClassBigFistAIComponent = Object({
    **CCharClassBaseBigFistAIComponentFields,
    "oBigFistAttackDef": CCharClassBigFistAttack,
})

CCharClassBigFistAIComponent_CTunableCharClassBigFistAIComponent = Object({
    **base_tunable_CTunableFields,
    "fFleeTimeToReturnToPatrol": common_types.Float,
    "fChaseMinDist": common_types.Float,
    "fChaseMaxDist": common_types.Float,
})

CCharClassBigFistAttack_CTunableCharClassBigFistAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fPostAttackLoopDuration": common_types.Float,
    "fFrontSpaceToForbidAttack": common_types.Float,
})

CCharClassBigkranXMagmaRainAttack = Object({
    **CCharClassAttackFields,
    "fTimeAttacking": common_types.Float,
    "fTargetBehindMaxTime": common_types.Float,
    "fTargetAheadMaxDistance": common_types.Float,
    "fTargetBehindMaxDistance": common_types.Float,
    "fChargeLoopFarDistance": common_types.Float,
    "fChargeLoopFarDistance2": common_types.Float,
})

SBigkranXSpitLaunchPatternStep = Object({
    "fHorizontalOffset": common_types.Float,
    "fVerticalOffset": common_types.Float,
    "fTimeForNextBall": common_types.Float,
})

base_global_CRntVector_SBigkranXSpitLaunchPatternStep_ = common_types.make_vector(SBigkranXSpitLaunchPatternStep)

TBigkranXSpitLaunchPattern = base_global_CRntVector_SBigkranXSpitLaunchPatternStep_

SBigkranXSpitLaunchConfig = Object({
    "tPattern": TBigkranXSpitLaunchPattern,
    "sName": common_types.StrId,
})

CCharClassBigkranXSpitAttack = Object({
    **CCharClassAttackFields,
    "fTimeAttacking": common_types.Float,
    "fTargetBehindMaxTime": common_types.Float,
    "fTargetAheadMaxDistance": common_types.Float,
    "fTargetBehindMaxDistance": common_types.Float,
    "fTimeOutOfFrustumToAbortAttack": common_types.Float,
    "fBallGravity": common_types.Float,
    "fBallTrajectoryCheckRadius": common_types.Float,
    "fTrajectorySampleTimeInterval": common_types.Float,
    "fMaxHitVerticalSpeed": common_types.Float,
    "fBallDefaultLaunchAngleDegs": common_types.Float,
    "fBallLaunchSpeed": common_types.Float,
    "fBallMinLaunchAngleDegs": common_types.Float,
    "fBallMaxLaunchAngleDegs": common_types.Float,
    "fHighLaunchFixedAngleDegs": common_types.Float,
    "fHighLaunchMinSpeed": common_types.Float,
    "fHighLaunchMaxSpeed": common_types.Float,
    "fMediumLaunchFixedAngleDegs": common_types.Float,
    "fMediumLaunchMinSpeed": common_types.Float,
    "fMediumLaunchMaxSpeed": common_types.Float,
    "fLowLaunchFixedAngleDegs": common_types.Float,
    "fLowLaunchMinSpeed": common_types.Float,
    "fLowLaunchMaxSpeed": common_types.Float,
    "oOffsetPatternConfig": SBigkranXSpitLaunchConfig,
})

SLaunchPatternStep = Object({
    "fAngleOffsetDegs": common_types.Float,
    "fSpeed": common_types.Float,
    "fGravity": common_types.Float,
    "fTimeForNextBall": common_types.Float,
})

base_global_CRntVector_SLaunchPatternStep_ = common_types.make_vector(SLaunchPatternStep)

TLaunchPattern = base_global_CRntVector_SLaunchPatternStep_

SLaunchConfig = Object({
    "fCombatMinTimeBetweenBalls": common_types.Float,
    "fCombatMaxTimeBetweenBalls": common_types.Float,
    "tPattern": TLaunchPattern,
    "sName": common_types.StrId,
    "fFloorMinAngleDegs": common_types.Float,
    "fFloorMaxAngleDegs": common_types.Float,
    "fFloorMinAngleDegs2": common_types.Float,
    "fFloorMaxAngleDegs2": common_types.Float,
})

CCharClassBigkranXAIComponent = Object({
    **CCharClassBaseBigFistAIComponentFields,
    "oBigkranXMagmaRainAttackDef": CCharClassBigkranXMagmaRainAttack,
    "oBigkranXSpitAttackDef": CCharClassBigkranXSpitAttack,
    "sLaunchConfig": SLaunchConfig,
    "sLaunchConfig2": SLaunchConfig,
    "sLaunchConfig3": SLaunchConfig,
    "fMaxDistance1": common_types.Float,
    "fMaxDistance2": common_types.Float,
    "sMagmaBallCharClass": common_types.StrId,
    "fShotHeightOffset": common_types.Float,
    "fReachableHeightBeforeAttack": common_types.Float,
    "fReachableHeightOnAttack": common_types.Float,
    "fTimeBeforeWarningAttack": common_types.Float,
})

CCharClassBillboardComponent = Object({
    **CCharClassComponentFields,
    "fGroupRadius": common_types.Float,
    "fBillboardRadius": common_types.Float,
    "sPath": common_types.StrId,
    "sBgPath": common_types.StrId,
    "iTextureWidth": common_types.Int,
    "iTextureHeight": common_types.Int,
    "vInitialColor": common_types.CVector3D,
    "fUniformColorOffset": common_types.Float,
    "vColorOffset": common_types.CVector3D,
    "fInitialAlpha": common_types.Float,
    "fAlphaOffset": common_types.Float,
    "sBillboardDefaultLoop": common_types.StrId,
    "sBillboardMotionDefaultLoop": common_types.StrId,
    "sGroupMotionDefaultLoop": common_types.StrId,
    "bUseRotation": construct.Flag,
    "fBillboardMotionDefaultScale": common_types.Float,
    "fGroupMotionDefaultScale": common_types.Float,
    "sSoundLoopLot": common_types.StrId,
    "sSoundLoopLit": common_types.StrId,
    "fSoundLoopLotAmountPct": common_types.Float,
    "fSoundLoopAttMinDist": common_types.Float,
    "fSoundLoopAttMaxDist": common_types.Float,
    "sSoundImpactBase": common_types.StrId,
    "iSoundImpactCount": common_types.Int,
    "fSoundImpactRadiusMinAtt": common_types.Float,
    "fSoundImpactRadiusMaxAtt": common_types.Float,
    "iPoolSize": common_types.UInt,
})

CCharClassBindLightToConstantAlphaEvent = Object({
    **base_global_timeline_CEventFields,
    "sMaterial": common_types.StrId,
    "sLight": common_types.StrId,
    "iConstant": common_types.Int,
})

CCharClassBlockTrack = Object(base_global_timeline_CTrackFields)

CCharClassBlockableWarningRadius = Object(CCharClassComponentFields)

CCharClassBlockableWarningRadius_CTunableCharClassBlockableWarningRadius = Object({
    **base_tunable_CTunableFields,
    "fBlockableAttackWarningRadiusGooplot": common_types.Float,
    "fBlockableAttackWarningRadiusChozoCommanderKiCounter": common_types.Float,
    "fBlockableAttackWarningRadiusChozoCommanderKiStrike": common_types.Float,
    "fBlockableAttackWarningRadiusPoisonfly": common_types.Float,
    "fBlockableAttackWarningRadiusQuetzoa": common_types.Float,
    "fBlockableAttackWarningRadiusIceflea": common_types.Float,
    "fBlockableAttackWarningRadiusTakumaku": common_types.Float,
    "fBlockableAttackWarningRadiusDredhed": common_types.Float,
    "fBlockableAttackWarningRadiusBlindfly": common_types.Float,
    "fBlockableAttackWarningRadiusKlaida": common_types.Float,
    "fBlockableAttackWarningRadiusArmadigger": common_types.Float,
    "fBlockableAttackWarningRadiusShelmit": common_types.Float,
    "fBlockableAttackWarningRadiusDropter": common_types.Float,
    "fBlockableAttackWarningRadiusSakai": common_types.Float,
    "fBlockableAttackWarningRadiusSharpaw": common_types.Float,
    "fBlockableAttackWarningRadiusQuetshockerX": common_types.Float,
})


class engine_utils_EMaterialConstantColor(enum.IntEnum):
    MATERIAL_CONSTANT_COLOR_0 = 0
    MATERIAL_CONSTANT_COLOR_1 = 1
    MATERIAL_CONSTANT_COLOR_2 = 2
    MATERIAL_CONSTANT_COLOR_3 = 3
    MATERIAL_CONSTANT_COLOR_4 = 4
    MATERIAL_CONSTANT_COLOR_5 = 5
    MATERIAL_CONSTANT_COLOR_6 = 6
    MATERIAL_CONSTANT_COLOR_7 = 7
    MATERIAL_CONSTANT_COLOR_8 = 8
    MATERIAL_CONSTANT_COLOR_9 = 9
    EMATERIALCONSTANTCOLOR_COUNT = 10
    Invalid = 2147483647


construct_engine_utils_EMaterialConstantColor = StrictEnum(engine_utils_EMaterialConstantColor)


class msapi_api_shdr_EShaderType(enum.IntEnum):
    E_VERTEX = 0
    E_PIXEL = 1
    E_GEOMETRY = 2
    Invalid = 2147483647


construct_msapi_api_shdr_EShaderType = StrictEnum(msapi_api_shdr_EShaderType)

CCharClassBoneToConstantComponent = Object({
    **CCharClassComponentFields,
    "sNode": PropertyEnum,
    "sMaterialName": PropertyEnum,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
})

CCharClassBorderUpTrack = Object(base_global_timeline_CTrackFields)

CCharClassBreakableScenarioComponent = Object({
    **CCharClassComponentFields,
    "vColliderIds": base_global_CRntVector_base_global_CStrId_,
})

CCharClassBumpedTrack = Object(base_global_timeline_CTrackFields)

CCharClassBuriedTrack = Object(base_global_timeline_CTrackFields)

CCharClassCallEmmyEvent = Object({
    **base_global_timeline_CEventFields,
    "fMinTimeSinceLastTargetPerception": common_types.Float,
})

CCharClassCameraFXPresetEvent = Object({
    **base_global_timeline_CEventFields,
    "sPreset": common_types.StrId,
    "fDirX": common_types.Float,
    "fDirY": common_types.Float,
    "fDirZ": common_types.Float,
})

CCharClassCameraIgnoreDC_FloorOffsetUpdateTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanBeAbortedTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanBeGrabbedTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanBeStaggeredBySpiderImpulseTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanBeStaggeredTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanFallTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanRetractTrack = Object(CCharClassToStateTrackFields)

CCharClassCanReverseTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassCanStartLavaStreamAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassCantBeBlockedWithMeleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassCantBeGrappledTrack = Object(base_global_timeline_CTrackFields)

CCharClassCantChargeTrack = Object(base_global_timeline_CTrackFields)

CCharClassCantFireTrack = Object({
    **base_global_timeline_CTrackFields,
    "bBufferInput": construct.Flag,
    "sBufferInputAction": common_types.StrId,
    "bBufferInputActionSynchronized": construct.Flag,
})

CCharClassCantFloorSlideTrack = Object({
    **base_global_timeline_CTrackFields,
    "bBufferInput": construct.Flag,
    "sBufferInputAction": common_types.StrId,
})

CCharClassElevatorUsableComponent = Object(CCharClassElevatorUsableComponentFields := {
    **CCharClassUsableComponentFields,
    "sUsableUpAction": common_types.StrId,
    "sUsableDownAction": common_types.StrId,
    "sUsableLevelChangeUpAction": common_types.StrId,
    "sUsableLevelChangeDownAction": common_types.StrId,
})

CCharClassCapsuleUsableComponent = Object({
    **CCharClassElevatorUsableComponentFields,
    "sCapsuleLeaveAction": common_types.StrId,
    "sCapsuleArriveAction": common_types.StrId,
    "sSkybaseAction": common_types.StrId,
})

CCharClassCaterzillaAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "iNumOfCreatures": common_types.Int,
})

CCharClassCentralUnitAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "bPlaceholder": construct.Flag,
    "sArmorLifeTunableId": common_types.StrId,
})

CCharClassCentralUnitAIComponent_CTunableCharClassCentralUnitAIComponent = Object({
    **base_tunable_CTunableFields,
    "bAllowSimultaneousRinkas": construct.Flag,
})

CCharClassCentralUnitCannonAIComponent = Object(CCharClassAIComponentFields)

CCharClassCentralUnitCannonAIComponent_CTunableCharClassCentralUnitCannonAIComponent = Object({
    **base_tunable_CTunableFields,
    "fAimAngleInterpolationSpeed": common_types.Float,
    "fAimAngleTolerance": common_types.Float,
    "fAttackPreparationTime": common_types.Float,
    "fAttackCooldownTime": common_types.Float,
})

CCharClassMovementComponent = Object(CCharClassMovementComponentFields := {
    **CCharClassComponentFields,
    "fPhysicsVelocityFriction": common_types.Float,
    "fGravityScalar": common_types.Float,
    "bWantsCheckViewDirInComputeKinematicRotationDelta": construct.Flag,
})


class EForcedDamageMode(enum.IntEnum):
    NOT_FORCED = 0
    ONLY_REACTION = 1
    FORCED = 2
    Invalid = 2147483647


construct_EForcedDamageMode = StrictEnum(EForcedDamageMode)

CCharClassWeaponMovement = Object(CCharClassWeaponMovementFields := {
    **CCharClassMovementComponentFields,
    "sDamageID": common_types.StrId,
    "sDamageSource": common_types.StrId,
    "eDamageType": construct_EDamageType,
    "eDamageStrength": construct_EDamageStrength,
    "fSpeed": common_types.Float,
    "sCollisionMask": common_types.StrId,
    "bWantsProcessBreakableTileHit": construct.Flag,
    "eForcedDamageMode": construct_EForcedDamageMode,
    "bSetHitPosOnCollisionProcessed": construct.Flag,
    "bAllowMultipleHitsToSameEntity": construct.Flag,
    "bIgnoreSamusCannonImpactDuringMelee": construct.Flag,
})


class CCharClassProjectileMovement_EProjectileMeleeHitReaction(enum.IntEnum):
    IMPACT = 0
    IMPACT_ATTACKER = 1
    NONE = 2
    Invalid = 2147483647


construct_CCharClassProjectileMovement_EProjectileMeleeHitReaction = StrictEnum(CCharClassProjectileMovement_EProjectileMeleeHitReaction)

CCharClassProjectileMovement = Object(CCharClassProjectileMovementFields := {
    **CCharClassWeaponMovementFields,
    "sCameraFXPresetOnImpact": common_types.StrId,
    "bUseCheckBeforeCast": construct.Flag,
    "fGravity": common_types.Float,
    "bApplyGravityOnInitialSpeed": construct.Flag,
    "sColliderToCheckCollisions": common_types.StrId,
    "sColliderToCheckDamage": common_types.StrId,
    "bDeleteAfterCollisionProcessed": construct.Flag,
    "bAddOwnerVelocityOnBeginPlay": construct.Flag,
    "fOwnerVelocityFactor": common_types.Float,
    "fVelocityHorizontalFriction": common_types.Float,
    "fVelocityVerticalFriction": common_types.Float,
    "bDestroyOnImpactSpeedBooster": construct.Flag,
    "bIgnoreInvulnerableEntities": construct.Flag,
    "eDefaultProjectileMeleeHitReaction": construct_CCharClassProjectileMovement_EProjectileMeleeHitReaction,
    "bAutoCalculateSpeedForParabola": construct.Flag,
    "bIgnoreMovementOnCollision": construct.Flag,
})

CCharClassCentralUnitCannonBeamMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassChangeAIAnimationStateEvent = Object({
    **base_global_timeline_CEventFields,
    "sState": common_types.StrId,
})

CCharClassChangeCharacterColliderTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCollider": common_types.StrId,
})

CCharClassChangeStageNavMeshItemComponent = Object({
    **CCharClassComponentFields,
    "sStage": common_types.StrId,
    "sRemovedStage": common_types.StrId,
})

CCharClassCharacterMovement = Object(CCharClassCharacterMovementFields := {
    **CCharClassMovementComponentFields,
    "fMaxYCollisionNormalToBeFloor": common_types.Float,
    "bStopOnWallMovementCollision": construct.Flag,
})

CCharClassCheckEndAutoLockOnEvent = Object(base_global_timeline_CEventFields)

CCharClassCheckFloorHitExtraDistanceTrack = Object({
    **base_global_timeline_CTrackFields,
    "fExtraDistance": common_types.Float,
})

CCharClassCheckFrontAimEndEvent = Object(base_global_timeline_CEventFields)

CCharClassCheckHangShotEndEvent = Object({
    **base_global_timeline_CEventFields,
    "bCheckStealth": construct.Flag,
})

CCharClassCheckMagnetShotEndEvent = Object(base_global_timeline_CEventFields)

CCharClassCheckSegmentDirToMoveTrack = Object(base_global_timeline_CTrackFields)

CCharClassCheckShinesparkAllowingActivationTrack = Object(base_global_timeline_CTrackFields)

CCharClassCheckShotEndEvent = Object({
    **base_global_timeline_CEventFields,
    "bCheckStealth": construct.Flag,
})

CCharClassChozoCommanderAttack = Object(CCharClassChozoCommanderAttackFields := {
    **CCharClassAttackFields,
    "bCheckAuraNotCharged": construct.Flag,
    "bSyncCapeActionOnStart": construct.Flag,
})

CCharClassChozoCommanderGroundAttack = Object(CCharClassChozoCommanderGroundAttackFields := {
    **CCharClassChozoCommanderAttackFields,
    "fDesiredDistanceToAttack": common_types.Float,
    "fMinHyperDashDistance": common_types.Float,
    "fMaxHyperDashDistance": common_types.Float,
})

CCharClassChozoCommanderTriComboAttack = Object(CCharClassChozoCommanderGroundAttackFields)

CCharClassChozoCommanderKiStrikeAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fNoReactionTimeCharging": common_types.Float,
    "fMinTimeCharging": common_types.Float,
    "fMaxTimeCharging": common_types.Float,
    "fSlomo": common_types.Float,
    "fSlomotime": common_types.Float,
    "sSlomoFunction": common_types.StrId,
    "fDistanceToEndCharge": common_types.Float,
})

CCharClassChozoCommanderSentenceSphereAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fMinDistanceInSpaceJump": common_types.Float,
})

CCharClassChozoCommanderPowerPulseAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fFinalAngleDeg": common_types.Float,
    "fTimeAtFinalAngle": common_types.Float,
    "fTimeToReachFinalAngle": common_types.Float,
    "fMinDistToWall": common_types.Float,
    "sAngleIncrementCurve": common_types.StrId,
})

CCharClassChozoCommanderAuraScratchAttack = Object(CCharClassChozoCommanderGroundAttackFields)

CCharClassChozoCommanderKiCounterAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fTimeToLaunchEnd": common_types.Float,
    "fDistToForceMelee": common_types.Float,
    "fDistToLaunchInit": common_types.Float,
    "fBlockableAttackWarningTimeout": common_types.Float,
    "fMinCameraBoundingWidth": common_types.Float,
})

CCharClassChozoCommanderAirAttack = Object(CCharClassChozoCommanderAirAttackFields := CCharClassChozoCommanderAttackFields)

CCharClassChozoCommanderLandingSlamAttack = Object({
    **CCharClassChozoCommanderAirAttackFields,
    "fHeightToSamus": common_types.Float,
    "fTimeTracking": common_types.Float,
    "fMinSpeed": common_types.Float,
    "fMaxSpeed": common_types.Float,
    "fDistToClampMaxSpeed": common_types.Float,
})

CCharClassChozoCommanderAirChargeAttack = Object(CCharClassChozoCommanderAirAttackFields)

CCharClassChozoCommanderZeroLaserAttack = Object({
    **CCharClassChozoCommanderAirAttackFields,
    "fHeight": common_types.Float,
    "fAimingAngle": common_types.Float,
    "fMinTrackingTime": common_types.Float,
    "fMaxTrackingTime": common_types.Float,
    "fChargingTime": common_types.Float,
    "fShootingTime": common_types.Float,
    "fMinXDistToAttack": common_types.Float,
    "fMinYDistToAttack": common_types.Float,
    "fMinXDistToShot": common_types.Float,
})

CCharClassChozoCommanderBeamBurstAttack = Object(CCharClassChozoCommanderAirAttackFields)

CCharClassChozoCommanderHypersparkAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fPreparationTime": common_types.Float,
    "fVerticalPreparationTime": common_types.Float,
    "fChangeDirProb": common_types.Float,
})

CCharClassChozoCommanderEnergyShardsAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fMinDistanceToWall": common_types.Float,
    "fSphereHeight": common_types.Float,
})

CCharClassChozoCommanderZeroLaserGroundedAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fAimingTime": common_types.Float,
    "fChargingTime": common_types.Float,
    "fFiringTime": common_types.Float,
    "fAimAngleInterpSpeedMin": common_types.Float,
    "fAimAngleInterpSpeedMax": common_types.Float,
})

CCharClassChozoCommanderHyperDashAttack = Object({
    **CCharClassChozoCommanderGroundAttackFields,
    "fHeightOverSamus": common_types.Float,
    "fDistanceBehindSamus": common_types.Float,
})

CCharClassChozoCommanderUltimateGrabAttack = Object(CCharClassChozoCommanderAttackFields)

CCharClassChozoCommanderKiGrabAttack = Object(CCharClassChozoCommanderAttackFields)

CCharClassChozoCommanderAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "oChozoCommanderTriComboAttackDef": CCharClassChozoCommanderTriComboAttack,
    "oChozoCommanderKiStrikeAttackDef": CCharClassChozoCommanderKiStrikeAttack,
    "oChozoCommanderSentenceSphereAttackDef": CCharClassChozoCommanderSentenceSphereAttack,
    "oChozoCommanderPowerPulseAttackDef": CCharClassChozoCommanderPowerPulseAttack,
    "oChozoCommanderAuraScratchAttackDef": CCharClassChozoCommanderAuraScratchAttack,
    "oChozoCommanderKiCounterAttackDef": CCharClassChozoCommanderKiCounterAttack,
    "oChozoCommanderLandingSlamAttackDef": CCharClassChozoCommanderLandingSlamAttack,
    "oChozoCommanderAirChargeAttackDef": CCharClassChozoCommanderAirChargeAttack,
    "oChozoCommanderZeroLaserAttackDef": CCharClassChozoCommanderZeroLaserAttack,
    "oChozoCommanderBeamBurstAttackDef": CCharClassChozoCommanderBeamBurstAttack,
    "oChozoCommanderHypersparkAttackDef": CCharClassChozoCommanderHypersparkAttack,
    "oChozoCommanderEnergyShardsAttackDef": CCharClassChozoCommanderEnergyShardsAttack,
    "oChozoCommanderZeroLaserGroundedAttackDef": CCharClassChozoCommanderZeroLaserGroundedAttack,
    "oChozoCommanderHyperDashAttackDef": CCharClassChozoCommanderHyperDashAttack,
    "oChozoCommanderUltimateGrabAttackDef": CCharClassChozoCommanderUltimateGrabAttack,
    "oChozoCommanderKiGrabAttackDef": CCharClassChozoCommanderKiGrabAttack,
    "fAuraLife": common_types.Float,
    "fLifeToRecoverAfterUltimateGrabStage1": common_types.Float,
    "fLifeToRecoverAfterUltimateGrabStage3": common_types.Float,
    "fUltimateGrabDamage": common_types.Float,
    "fTimeBetweenKiStrikeAttacks": common_types.Float,
    "fAttackWaitTimeBetweenPhases": common_types.Float,
    "fMinDistToHyperDash": common_types.Float,
    "fMaxVerticalDiffToAboveHyperDash": common_types.Float,
    "oDamageSourceFactorShortShootingGrab": CDamageSourceFactor,
    "oDamageSourceFactorLongShootingGrab": CDamageSourceFactor,
})

CCharClassChozoCommanderAIComponent_CTunableCharClassChozoCommanderAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMotionSpeed": common_types.Float,
    "bKiCounterDeactivateAura": construct.Flag,
    "bKiCounterShowMeleableFX": construct.Flag,
    "bKiCounterUseZoomCamera": construct.Flag,
    "iInitialStage": common_types.Int,
    "fSentenceSphereSpeed": common_types.Float,
    "TRI_COMBO": construct.Flag,
    "KI_STRIKE": construct.Flag,
    "SENTENCE_SPHERE": construct.Flag,
    "POWER_PULSE": construct.Flag,
    "AURA_SCRATCH": construct.Flag,
    "KI_COUNTER": construct.Flag,
    "LANDING_SLAM": construct.Flag,
    "AIR_CHARGE": construct.Flag,
    "ZERO_LASER": construct.Flag,
    "BEAM_BURST": construct.Flag,
    "HYPER_SPARK": construct.Flag,
    "ENERGY_SHARDS": construct.Flag,
    "ZERO_LASER_GROUNDED": construct.Flag,
    "HYPER_DASH": construct.Flag,
    "ULTIMATE_GRAB": construct.Flag,
    "KI_GRAB": construct.Flag,
})

CCharClassChozoCommanderAirChargeAttack_CTunableCharClassChozoCommanderAirAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinDistanceBetweenPlayerAndWall": common_types.Float,
    "fMaxDistanceToDashBack": common_types.Float,
    "fDistanceToEndCharge": common_types.Float,
})

CCharClassChozoCommanderBeamBurstAttack_CTunableCharClassChozoCommanderBeamBurstAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fHeihtToStartAttack": common_types.Float,
    "fClosestDistToStartAttack": common_types.Float,
    "fAimAngleInterpSpeed": common_types.Float,
    "fShotAngleInterpSpeedMin": common_types.Float,
    "fShotAngleInterpSpeedMax": common_types.Float,
    "fTimeAiming": common_types.Float,
    "fTimeShootingInit": common_types.Float,
    "fTimeShooting": common_types.Float,
    "fTimeShootingLong": common_types.Float,
    "fTimeToImpact": common_types.Float,
    "fTimeToResetHittingPlayer": common_types.Float,
    "fContinuosDamage": common_types.Float,
    "fImpactDamage": common_types.Float,
})

CCharClassChozoCommanderDestroySentenceSpheresEvent = Object(base_global_timeline_CEventFields)

CCharClassChozoCommanderEnergyShardsFragmentMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassChozoCommanderEnergyShardsSphereMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fAngleDispersion": common_types.Float,
    "fPositionDispersion": common_types.Float,
    "iNumExplosions": common_types.Int,
    "fTimeBetweenExplosions": common_types.Float,
    "fInitialTimeBetweenExplosions": common_types.Float,
    "fMaxLifeTime": common_types.Float,
})

CCharClassChozoCommanderLaunchKiCounterCutsceneEvent = Object(base_global_timeline_CEventFields)

CCharClassChozoCommanderSentenceSphereLifeComponent = Object(CCharClassBasicLifeComponentFields)

CCharClassChozoCommanderSentenceSphereMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fRotationSpeedDeg": common_types.Float,
    "fInitialRadius": common_types.Float,
    "fMinRadius": common_types.Float,
    "fMaxRadius": common_types.Float,
    "fTimeToReachMinRadius": common_types.Float,
    "fTimeToReachMaxRadius": common_types.Float,
})

CCharClassChozoCommanderSetAuraStateEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassChozoCommanderXCheckWinEvent = Object(base_global_timeline_CEventFields)

CCharClassChozoCommanderXLifeComponent = Object({
    **CCharClassLifeComponentFields,
    "fTimeToWin": common_types.Float,
    "fImpactedPlayRate": common_types.Float,
})

CCharClassChozoCommanderZeroLaserBaseAttack = Object(CCharClassChozoCommanderAttackFields)

std_unique_ptr_CChozoRobotSoldierCannonShotPattern_ = Pointer_CChozoRobotSoldierCannonShotPattern.create_construct()

base_global_CRntVector_std_unique_ptr_CChozoRobotSoldierCannonShotPattern__ = common_types.make_vector(std_unique_ptr_CChozoRobotSoldierCannonShotPattern_)

CCharClassChozoRobotSoldierCannonShotAttack = Object({
    **CCharClassAttackFields,
    "tPatterns": base_global_CRntVector_std_unique_ptr_CChozoRobotSoldierCannonShotPattern__,
})

CCharClassChozoRobotSoldierDashSlashAttack = Object(CCharClassAttackFields)

CCharClassChozoRobotSoldierDisruptionFieldAttack = Object(CCharClassAttackFields)

CCharClassChozoRobotSoldierUppercutAttack = Object({
    **CCharClassAttackFields,
    "fTraveledMaxDistanceToAddToMaxDistance": common_types.Float,
    "fDistanceToReachableTarget": common_types.Float,
    "fDistanceToReachableTargetMB": common_types.Float,
    "fDistanceToNonReachableTarget": common_types.Float,
    "fDistanceToLaunchEnd4m": common_types.Float,
})

CEnemyMovementWalkingAnims = Object({
    "sRelaxAnim": common_types.StrId,
    "sFrontAnim": common_types.StrId,
    "sBackAnim": common_types.StrId,
    "sFrontInitAnim": common_types.StrId,
    "sBackInitAnim": common_types.StrId,
    "sFrontEndAnim": common_types.StrId,
    "sBackEndAnim": common_types.StrId,
})

std_unique_ptr_querysystem_CFilter_ = Pointer_querysystem_CFilter.create_construct()

base_global_CRntVector_std_unique_ptr_querysystem_CFilter__ = common_types.make_vector(std_unique_ptr_querysystem_CFilter_)

std_unique_ptr_querysystem_CEvaluator_ = Pointer_querysystem_CEvaluator.create_construct()

base_global_CRntVector_std_unique_ptr_querysystem_CEvaluator__ = common_types.make_vector(std_unique_ptr_querysystem_CEvaluator_)

querysystem_CQuerySystemDef = Object({
    "tFilters": base_global_CRntVector_std_unique_ptr_querysystem_CFilter__,
    "tEvaluators": base_global_CRntVector_std_unique_ptr_querysystem_CEvaluator__,
})

CCharClassChozoRobotSoldierAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "oChozoRobotSoldierCannonShotAttackDef": CCharClassChozoRobotSoldierCannonShotAttack,
    "oChozoRobotSoldierDashSlashAttackDef": CCharClassChozoRobotSoldierDashSlashAttack,
    "oChozoRobotSoldierDisruptionFieldAttackDef": CCharClassChozoRobotSoldierDisruptionFieldAttack,
    "oChozoRobotSoldierUppercutAttackDef": CCharClassChozoRobotSoldierUppercutAttack,
    "oRunningAnims": CEnemyMovementWalkingAnims,
    "oShootingPositionQuerySystemDef": querysystem_CQuerySystemDef,
    "oSelectedShootingPositionQuerySystemDef": querysystem_CQuerySystemDef,
    "oNoPathFoundShootingPositionQuerySystemDef": querysystem_CQuerySystemDef,
    "oDamageSourceFactorElite": CDamageSourceFactor,
    "oDamageSourceFactorCrazy": CDamageSourceFactor,
    "oDamageSourceFactorCrazyElite": CDamageSourceFactor,
})

CCharClassChozoRobotSoldierAIComponent_CTunableCharClassChozoRobotSoldierAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMinTimeToStartChargeBeam": common_types.Float,
    "fMaxTimeToStartChargeBeam": common_types.Float,
    "fTimeToChargeBeam": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fExplosionTimeToReachRadius": common_types.Float,
    "fExplosionTimeAtMaxRadius": common_types.Float,
    "fCoreDamageFactor": common_types.Float,
    "fTimeBetweenAttackGoingToShootingPosition": common_types.Float,
    "fTimeBetweenAttackInShootingPosition": common_types.Float,
    "fRangedAttackAfterMeleeAttackProbability": common_types.Float,
    "fMeleeAttackAfterRangedAttackProbability": common_types.Float,
    "fChangeToRangedAttackOnSamePlatformProbability": common_types.Float,
    "bAllCanUseChargeBeam": construct.Flag,
})

CCharClassChozoRobotSoldierAllowForcedDashSlashTrack = Object(base_global_timeline_CTrackFields)

CCharClassChozoRobotSoldierBeamMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fChargedSpeed": common_types.Float,
})

CCharClassChozoRobotSoldierCannonShotAttack_CTunableCharClassChozoRobotSoldierCannonShotAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fTimeToFinishAttack": common_types.Float,
    "fTimeToWaitAfterBeamCharged": common_types.Float,
})

CCharClassChozoRobotSoldierDashSlashAttack_CTunableCharClassChozoRobotSoldierDashSlashAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fMaxTraveledDistance": common_types.Float,
    "fTimeToDisableAttackAfterMeleeSuccess": common_types.Float,
})

CCharClassChozoRobotSoldierDisruptionFieldAttack_CTunableCharClassChozoRobotSoldierDisruptionFieldAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fExplosionTimeToReachRadius": common_types.Float,
    "fExplosionTimeAtMaxRadius": common_types.Float,
    "fSpecialEnergyConsume": common_types.Float,
})

CCharClassChozoRobotSoldierExplosionEvent = Object(base_global_timeline_CEventFields)

CCharClassChozoRobotSoldierSpinAttackTransitionTrack = Object(base_global_timeline_CTrackFields)

CCharClassChozoRobotSoldierUppercutAttack_CTunableCharClassChozoRobotSoldierUppercutAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoWarriorAttack = Object(CCharClassChozoWarriorAttackFields := CCharClassAttackFields)

CCharClassChozoWarriorGlaiveSpinAttack = Object(CCharClassChozoWarriorGlaiveSpinAttackFields := CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorGlaiveWalljumpAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorDeflectorShieldAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorAIComponent = Object(CCharClassChozoWarriorAIComponentFields := {
    **CCharClassBossAIComponentFields,
    "oChozoWarriorGlaiveSpinAttackDef": CCharClassChozoWarriorGlaiveSpinAttack,
    "oChozoWarriorGlaiveWalljumpAttackDef": CCharClassChozoWarriorGlaiveWalljumpAttack,
    "oChozoWarriorDeflectorShieldAttackDef": CCharClassChozoWarriorDeflectorShieldAttack,
    "bUsesShield": construct.Flag,
    "fTargetMinDistanceToFloorToForceGlaiveSpinAttack": common_types.Float,
    "fGlaiveSpinAttackOffsetDistanceIfTargetOnAir": common_types.Float,
})

CCharClassChozoWarriorAIComponent_CTunableCharClassChozoWarriorAIComponent = Object({
    **base_tunable_CTunableFields,
    "fGrappleTime": common_types.Float,
    "fShieldLife": common_types.Float,
    "fShieldDamagePerMissile": common_types.Float,
    "fShieldDamagePerMelee": common_types.Float,
    "bAllowShieldImpactAnim": construct.Flag,
    "fMinTimeBetweenShieldImpactAnim": common_types.Float,
})

CCharClassChozoWarriorDeflectorShieldAttack_CTunableCharClassChozoWarriorShieldAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoWarriorEliteAIComponent = Object(CCharClassChozoWarriorAIComponentFields)

CCharClassChozoWarriorEnableGlaiveTrack = Object({
    **base_global_timeline_CTrackFields,
    "fTipOffset": common_types.Float,
})

CCharClassChozoWarriorGlaiveSpinAttack_CTunableCharClassChozoWarriorGlaiveSpinAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoWarriorGlaiveWalljumpAttack_CTunableCharClassChozoWarriorGlaiveWalljumpAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fSkipAttackProb": common_types.Float,
})

CCharClassChozoWarriorSetInvulnerableEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassChozoWarriorSetShieldEnabledEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassChozoWarriorXGlaiveSpinAttack = Object(CCharClassChozoWarriorGlaiveSpinAttackFields)

CCharClassChozoWarriorXWallClimbAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorXLandAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorXChangeWallAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorXSpitAttack = Object(CCharClassChozoWarriorAttackFields)

CCharClassChozoWarriorXUltimateGrabAttack = Object({
    **CCharClassChozoWarriorAttackFields,
    "fUltimateGrabDamage": common_types.Float,
})

CCharClassChozoWarriorXAIComponent = Object(CCharClassChozoWarriorXAIComponentFields := {
    **CCharClassChozoWarriorAIComponentFields,
    "oChozoWarriorXGlaiveSpinAttackDef": CCharClassChozoWarriorXGlaiveSpinAttack,
    "oChozoWarriorXWallClimbAttackDef": CCharClassChozoWarriorXWallClimbAttack,
    "oChozoWarriorXLandAttackDef": CCharClassChozoWarriorXLandAttack,
    "oChozoWarriorXChangeWallAttackDef": CCharClassChozoWarriorXChangeWallAttack,
    "oChozoWarriorXSpitAttackDef": CCharClassChozoWarriorXSpitAttack,
    "oChozoWarriorXUltimateGrabAttackDef": CCharClassChozoWarriorXUltimateGrabAttack,
})

CCharClassChozoWarriorXChangeWallAttack_CTunableCharClassChozoWarriorXChangeWallAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoWarriorXEliteAIComponent = Object(CCharClassChozoWarriorXAIComponentFields)

CCharClassChozoWarriorXGlaiveSpinAttack_CTunableCharClassChozoWarriorXGlaiveSpinAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoWarriorXLandAttack_CTunableCharClassChozoWarriorXLandAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fWaveSpeed": common_types.Float,
    "fWaveProjectileRadius": common_types.Float,
    "fWaveHeight": common_types.Float,
    "fWaveInitialOffset": common_types.Float,
    "fWaveOffset": common_types.Float,
    "fWaveParticlesOffset": common_types.Float,
    "sWaveOffsetFactorizerFunction": common_types.StrId,
})

CCharClassChozoWarriorXSpitAttack_CTunableCharClassChozoWarriorXSpitAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fSplashRadius": common_types.Float,
})

CCharClassChozoWarriorXSpitMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassChozoWarriorXUltimateGrabAttack_CTunableCharClassChozoWarriorXUltimateGrabAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fLifeRecoveredOnGrab": common_types.Float,
    "fDistanceFromWallToGrab": common_types.Float,
})

CCharClassChozoWarriorXWallClimbAttack_CTunableCharClassChozoWarriorXWallClimbAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassChozoZombieXPoisonClawsAttack = Object(CCharClassAttackFields)

CCharClassChozoZombieXAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oChozoZombieXPoisonClawsAttackDef": CCharClassChozoZombieXPoisonClawsAttack,
})

CCharClassChozombieFXComponent = Object({
    **CCharClassComponentFields,
    "sModelResPath": common_types.StrId,
    "fScale": common_types.Float,
    "vRotation": common_types.CVector3D,
    "fInstanceLifeTime": common_types.Float,
})

CCharClassClimbingTrack = Object(base_global_timeline_CTrackFields)

CCharClassCollideAgainstIgnoredCollidersTrack = Object(base_global_timeline_CTrackFields)

base_global_CRntSmallDictionary_base_global_CStrId__game_logic_collision_EColMat_ = common_types.make_dict(construct_game_logic_collision_EColMat, key=common_types.StrId)

CCharClassCollisionComponent = Object({
    **CCharClassComponentFields,
    "v3SpawnPointCollisionSizeInc": common_types.CVector3D,
    "eDefaultCollisionMaterial": construct_game_logic_collision_EColMat,
    "bShouldIgnoreSlopeSupport": construct.Flag,
    "bForceSlopeDirectionOnFloorHit": construct.Flag,
    "mExplicitCollisionMaterials": base_global_CRntSmallDictionary_base_global_CStrId__game_logic_collision_EColMat_,
})


class EFXType(enum.IntEnum):
    FXTYPE_PARTICLESYSTEM = 0
    FXTYPE_RAGDOLL = 1
    FXTYPE_LIGHT = 2
    FXTYPE_MODEL = 3
    FXTYPE_CUSTOMMATERIAL = 4
    FXTYPE_LIGHTNING = 5
    FXTYPE_CURVEMODELS = 6
    FXTYPE_CURVEPARTICLES = 7
    FXTYPE_TRAIL = 8


construct_EFXType = StrictEnum(EFXType)


class ELinkType(enum.IntEnum):
    FXLINK_POSITION_FIXED = 0
    FXLINK_POSITION_ENTITY = 1
    FXLINK_POSITION_MODEL = 2
    FXLINK_POSITION_MODEL_NODE = 3
    FXLINK_ATTACH_ENTITY = 4
    FXLINK_ATTACH_MODEL = 5
    FXLINK_ATTACH_MODEL_NODE = 6
    FXLINK_ATTACH_POSITION_ENTITY = 7
    FXLINK_ATTACH_POSITION_MODEL_NODE = 8
    FXLINK_ATTACH_POSITION_MODEL_NODE_LOCAL = 9
    FXLINK_POSITION_LAST_DAMAGE_DONE_HIT = 10
    FXLINK_POSITION_AI_CUSTOM = 11
    FXLINK_MOVEMENT_CUSTOM = 12
    FXLINK_POSITION_CAMERA = 13
    FXLINK_ATTACH_CAMERA = 14
    FXLINK_ATTACH_POSITION_CAMERA = 15


construct_ELinkType = StrictEnum(ELinkType)

ICharClassFXCreateAndLinkEvent = Object(ICharClassFXCreateAndLinkEventFields := {
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "eType": construct_EFXType,
    "sPath": common_types.StrId,
    "eLinkType": construct_ELinkType,
    "sTarget": common_types.StrId,
    "fPositionOffsetX": common_types.Float,
    "fPositionOffsetY": common_types.Float,
    "fPositionOffsetZ": common_types.Float,
    "fAngleOffsetX": common_types.Float,
    "fAngleOffsetY": common_types.Float,
    "fAngleOffsetZ": common_types.Float,
    "fScaleX": common_types.Float,
    "fScaleY": common_types.Float,
    "fScaleZ": common_types.Float,
    "sAdditional": common_types.StrId,
    "bDropToFloor": construct.Flag,
    "fLifeTime": common_types.Float,
})

CCharClassCollisionMaterialFXCreateAndLinkEvent = Object(ICharClassFXCreateAndLinkEventFields)

ICharClassFXDeleteEvent = Object(ICharClassFXDeleteEventFields := {
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "fTimeToDelete": common_types.Float,
})

CCharClassCollisionMaterialFXDeleteEvent = Object(ICharClassFXDeleteEventFields)

ICharClassFXSetActiveEvent = Object(ICharClassFXSetActiveEventFields := {
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "bActive": construct.Flag,
    "bDisableOnEmpty": construct.Flag,
    "bDeleteOnEmpty": construct.Flag,
})

CCharClassCollisionMaterialFXSetActiveEvent = Object(ICharClassFXSetActiveEventFields)

ICharClassFXSetAutoManagedEvent = Object(ICharClassFXSetAutoManagedEventFields := {
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassCollisionMaterialFXSetAutoManagedEvent = Object(ICharClassFXSetAutoManagedEventFields)

ICharClassFXSetEnabledEvent = Object(ICharClassFXSetEnabledEventFields := {
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "bEnable": construct.Flag,
    "bReset": construct.Flag,
})

CCharClassCollisionMaterialFXSetEnabledEvent = Object(ICharClassFXSetEnabledEventFields)

CCharClassCombatTrack = Object(base_global_timeline_CTrackFields)

CCharClassCommanderAuraDisabledTrack = Object(base_global_timeline_CTrackFields)

CCharClassCommanderGroundStageChangeTrack = Object(base_global_timeline_CTrackFields)


class EWings(enum.IntEnum):
    low = 0
    high = 1
    Invalid = 2147483647


construct_EWings = StrictEnum(EWings)

CCharClassCommanderWingsTrack = Object({
    **base_global_timeline_CTrackFields,
    "eWings": construct_EWings,
})

CCharClassConvertToMbOnDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassConvertToMorphBallEvent = Object(base_global_timeline_CEventFields)

CCharClassConvertingToMorphBallTrack = Object(base_global_timeline_CTrackFields)

CCharClassCooldownXBossAttack = Object(CCharClassCooldownXBossAttackFields := {
    **CCharClassAttackFields,
    "fLaserWidth": common_types.Float,
    "sStartLavaTL": common_types.StrId,
    "sEndLavaTL": common_types.StrId,
})

std_unique_ptr_CCooldownXBossLavaCarpetDef_ = Pointer_CCooldownXBossLavaCarpetDef.create_construct()

base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaCarpetDef__ = common_types.make_vector(std_unique_ptr_CCooldownXBossLavaCarpetDef_)

base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaCarpetDef___ = common_types.make_vector(base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaCarpetDef__)

CCharClassCooldownXBossLavaCarpetAttack = Object({
    **CCharClassCooldownXBossAttackFields,
    "tPatterns": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaCarpetDef___,
    "fBreatheSpeedFactor": common_types.Float,
    "fTimeToPuddleDamage": common_types.Float,
})


class ELavaDropArmPos(enum.IntEnum):
    A = 0
    B = 1
    Invalid = 2147483647


construct_ELavaDropArmPos = StrictEnum(ELavaDropArmPos)


class ELavaDropArm(enum.IntEnum):
    LeftUp = 0
    LeftDown = 1
    RightUp = 2
    RightDown = 3
    Invalid = 2147483647


construct_ELavaDropArm = StrictEnum(ELavaDropArm)

CCooldownXBossLavaDropsMovementDef = Object({
    "eArmToChange": construct_ELavaDropArm,
    "fDelay": common_types.Float,
    "fAnimSpeed": common_types.Float,
})

base_global_CRntVector_CCooldownXBossLavaDropsMovementDef_ = common_types.make_vector(CCooldownXBossLavaDropsMovementDef)

CCooldownXBossLavaDropsDef = Object({
    "eLeftUpArmPos": construct_ELavaDropArmPos,
    "eLeftDownArmPos": construct_ELavaDropArmPos,
    "eRightUpArmPos": construct_ELavaDropArmPos,
    "eRightDownArmPos": construct_ELavaDropArmPos,
    "tActions": base_global_CRntVector_CCooldownXBossLavaDropsMovementDef_,
})

std_unique_ptr_CCooldownXBossLavaDropsDef_ = Pointer_CCooldownXBossLavaDropsDef.create_construct()

base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaDropsDef__ = common_types.make_vector(std_unique_ptr_CCooldownXBossLavaDropsDef_)

CCharClassCooldownXBossLavaDropsAttack = Object({
    **CCharClassCooldownXBossAttackFields,
    "fTimeInit": common_types.Float,
    "fTimeBetweenShots": common_types.Float,
    "fTimeLocked": common_types.Float,
    "fShotPreparationTime": common_types.Float,
    "fShotTime": common_types.Float,
    "fDamageRadius": common_types.Float,
    "fAimSpeed": common_types.Float,
    "fAimMinSpeed": common_types.Float,
    "fAimMaxSpeed": common_types.Float,
    "fAimMaxSpeedMaxDistance": common_types.Float,
    "tInitialState": CCooldownXBossLavaDropsDef,
    "tPatterns": base_global_CRntVector_std_unique_ptr_CCooldownXBossLavaDropsDef__,
})

CCharClassCooldownXBossReaperAttack = Object(CCharClassCooldownXBossAttackFields)

CCharClassCooldownXBossStrongWhipAttack = Object({
    **CCharClassCooldownXBossAttackFields,
    "fLoopTimeout": common_types.Float,
})

std_unique_ptr_CCooldownXBossFireWallDef_ = Pointer_CCooldownXBossFireWallDef.create_construct()

base_global_CRntVector_std_unique_ptr_CCooldownXBossFireWallDef__ = common_types.make_vector(std_unique_ptr_CCooldownXBossFireWallDef_)

base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CCooldownXBossFireWallDef___ = common_types.make_vector(base_global_CRntVector_std_unique_ptr_CCooldownXBossFireWallDef__)

CCharClassCooldownXBossWindTunnelAttack = Object({
    **CCharClassCooldownXBossAttackFields,
    "sEndAttackAnim": common_types.StrId,
    "sShotAttackAnim": common_types.StrId,
    "sStunAttackAnim": common_types.StrId,
    "iNumShots": common_types.Int,
    "fTimeToEndAttack": common_types.Float,
    "tLaunchPatterns": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CCooldownXBossFireWallDef___,
})

CCharClassCooldownXBossLaserBiteAttack = Object({
    **CCharClassCooldownXBossAttackFields,
    "fLoopTimeout": common_types.Float,
    "fDistanceToLaunchAttackIfImpacted": common_types.Float,
})

std_unique_ptr_CTentacle_ = Pointer_CTentacle.create_construct()

base_global_CRntVector_std_unique_ptr_CTentacle__ = common_types.make_vector(std_unique_ptr_CTentacle_)

CCharClassCooldownXBossAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "oCooldownXBossLavaCarpetAttackDef": CCharClassCooldownXBossLavaCarpetAttack,
    "oCooldownXBossLavaDropsAttackDef": CCharClassCooldownXBossLavaDropsAttack,
    "oCooldownXBossReaperAttackDef": CCharClassCooldownXBossReaperAttack,
    "oCooldownXBossStrongWhipAttackDef": CCharClassCooldownXBossStrongWhipAttack,
    "oCooldownXBossWindTunnelAttackDef": CCharClassCooldownXBossWindTunnelAttack,
    "oCooldownXBossLaserBiteAttackDef": CCharClassCooldownXBossLaserBiteAttack,
    "tTentacles": base_global_CRntVector_std_unique_ptr_CTentacle__,
    "fMinTimeToRelaxAction": common_types.Float,
    "fMaxTimeToRelaxAction": common_types.Float,
    "fTimeToGoToPhase3After4WPDestroyed": common_types.Float,
    "oGrabDamageSourceFactor": CDamageSourceFactor,
})

CCharClassCooldownXBossAIComponent_CTunableCharClassCooldownXBossAIComponent = Object({
    **base_tunable_CTunableFields,
    "iInitialStage": common_types.Int,
    "LAVA_CARPET": construct.Flag,
    "WIND_TUNNEL": construct.Flag,
    "STRONG_WHIP": construct.Flag,
    "REAPER": construct.Flag,
    "LAVA_DROPS": construct.Flag,
    "LASER_BITE": construct.Flag,
    "fMinLifeRestored4Arms": common_types.Float,
    "fMaxLifeRestored4Arms": common_types.Float,
    "fMinLifeRestored3Arms": common_types.Float,
    "fMaxLifeRestored3Arms": common_types.Float,
    "fMinLifeRestored2Arms": common_types.Float,
    "fMaxLifeRestored2Arms": common_types.Float,
    "fMinLifeRestored1Arms": common_types.Float,
    "fMaxLifeRestored1Arms": common_types.Float,
    "fPhase2Timeout": common_types.Float,
})

CCharClassCooldownXBossCanFireTrack = Object(base_global_timeline_CTrackFields)

CCharClassCooldownXBossCheckDeadInGrabEvent = Object(base_global_timeline_CEventFields)

CCharClassCooldownXBossDamageShapesTrack = Object({
    **base_global_timeline_CTrackFields,
    "sLogicShapesEnabled": common_types.StrId,
    "sDamageID": common_types.StrId,
    "eDamageStrength": construct_EDamageStrength,
})

CCharClassCooldownXBossDeathActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassCooldownXBossEnableCoolShinesparkTriggerEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnable": construct.Flag,
})

CCharClassCooldownXBossFireBallMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fPreparationTime": common_types.Float,
    "fMovingSpeed": common_types.Float,
})

CCharClassCooldownXBossHideDeathArmsInDeathCutsceneEvent = Object(base_global_timeline_CEventFields)

CCharClassCooldownXBossLaserBiteAttack_CTunableCharClassCooldownXBossLaserBiteAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassCooldownXBossLaunchDeathCutsceneEvent = Object(base_global_timeline_CEventFields)

CCharClassCooldownXBossLavaCarpetAttack_CTunableCharClassCooldownXBossLavaCarpetAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "iPattern": common_types.Int,
})

CCharClassCooldownXBossLavaDropsAttack_CTunableCharClassCooldownXBossLavaDropsAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "iForcedPattern": common_types.Int,
})

CCharClassCooldownXBossLavaTrack = Object(base_global_timeline_CTrackFields)

CCharClassCooldownXBossPhase2ActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassCooldownXBossReaperAttack_CTunableCharClassCooldownXBossReaperAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassCooldownXBossStrongWhipAttack_CTunableCharClassCooldownXBossStrongWhipAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassCooldownXBossWeakPointLifeComponent = Object(CCharClassBasicLifeComponentFields)

CCharClassCooldownXBossWindTunnelAttack_CTunableCharClassCooldownXBossWindTunnelAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "iForcedPattern": common_types.Int,
    "fShinesparkChargeExtensionWindTunnelPlayRate": common_types.Float,
})

CCharClassCoreXAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "fAcceleration": common_types.Float,
    "fTurningAcceleration": common_types.Float,
    "fMaxTurningAngle": common_types.Float,
    "fBrakeDistance": common_types.Float,
    "fMinBrakeSpeed": common_types.Float,
    "sBrakeCurve": common_types.StrId,
    "fImpactSpeed": common_types.Float,
    "fImpactTime": common_types.Float,
    "fImpactInvulnerableTime": common_types.Float,
    "fXParasiteDropCooldownTime": common_types.Float,
    "iXParasiteMinDrop": common_types.Int,
    "iXParasiteMaxDrop": common_types.Int,
    "sInventoryItemOnBigXAbsorbed": common_types.StrId,
})

CCharClassCoreXAIComponent_CTunableCharClassCoreXAIComponent = Object(base_tunable_CTunableFields)

CCharClassCrazyTrack = Object(base_global_timeline_CTrackFields)

CCharClassCrouchTrack = Object(base_global_timeline_CTrackFields)

CCharClassCutsceneActorTrack = Object(base_global_timeline_CTrackFields)

CCharClassCutsceneInGameEntityTrack = Object(base_global_timeline_CTrackFields)


class EInputAction(enum.IntEnum):
    NONE = 0
    MoveX = 1
    MoveY = 2
    Fire = 4
    SwitchGunMode = 16
    Jump = 32
    Aim = 64
    Melee = 128
    ActivateAbility = 256
    SelectAbilityLeftRight = 512
    SelectAbilityUpDown = 1024
    SwitchGun = 2048
    RawMove = 4096
    RawLook = 8192
    LoosingInputs = 16384
    Convert = 32768
    LookX = 65536
    LookY = 131072
    Walk = 262144
    WalkToggle = 524288
    OpticCamouflage = 1048576
    Sonar = 2097152
    MinimapEx = 4194304
    All = 65535


construct_EInputAction = StrictEnum(EInputAction)

CCharClassCutsceneOnInputCallbackEvent = Object({
    **base_global_timeline_CEventFields,
    "eInputAction": construct_EInputAction,
    "sLuaCallback": common_types.StrId,
})

CCharClassCutsceneReevaluateMultiModelEvent = Object(base_global_timeline_CEventFields)

CCharClassSluggerSpitAttack = Object({
    **CCharClassAttackFields,
    "fBallGravity": common_types.Float,
    "fMaxHitVerticalSpeed": common_types.Float,
    "fTrajectorySampleTimeInterval": common_types.Float,
    "fTimeOutOfFrustumToAbortAttack": common_types.Float,
    "fBallDefaultLaunchAngleDegs": common_types.Float,
    "fBallLaunchSpeed": common_types.Float,
    "fBallMinLaunchAngleDegs": common_types.Float,
    "fBallMaxLaunchAngleDegs": common_types.Float,
    "fHighLaunchFixedAngleDegs": common_types.Float,
    "fHighLaunchMinSpeed": common_types.Float,
    "fHighLaunchMaxSpeed": common_types.Float,
    "fMediumLaunchFixedAngleDegs": common_types.Float,
    "fMediumLaunchMinSpeed": common_types.Float,
    "fMediumLaunchMaxSpeed": common_types.Float,
    "fLowLaunchFixedAngleDegs": common_types.Float,
    "fLowLaunchMinSpeed": common_types.Float,
    "fLowLaunchMaxSpeed": common_types.Float,
})

CCharClassSluggerAIComponent = Object(CCharClassSluggerAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "oSluggerSpitAttackDef": CCharClassSluggerSpitAttack,
    "sAcidBallCharClass": common_types.StrId,
    "fAttackReachableHeight": common_types.Float,
    "fBallTrajectoryCheckRadius": common_types.Float,
})

CCharClassDaivoSpitAttack = Object({
    **CCharClassAttackFields,
    "fAttackCoolDown": common_types.Float,
})

CCharClassDaivoAIComponent = Object({
    **CCharClassSluggerAIComponentFields,
    "oDaivoSpitAttackDef": CCharClassDaivoSpitAttack,
})

CCharClassSwarmControllerComponent = Object(CCharClassSwarmControllerComponentFields := {
    **CCharClassComponentFields,
    "fMinTimeInNode": common_types.Float,
    "fTimeInNodeRandomness": common_types.Float,
    "fTargetChangeProbability": common_types.Float,
    "sIndividualLife": common_types.StrId,
    "fAttackPathOffset": common_types.Float,
    "iMaxChangingTargetSimul": common_types.Int,
    "bWantsSpiraling": construct.Flag,
    "bWantsJellyfishMovement": construct.Flag,
    "bWantsFishMovement": construct.Flag,
    "bWantsInternalFlocking": construct.Flag,
    "bWantsMigration": construct.Flag,
    "fMaxDistToMigrate": common_types.Float,
    "bWantsBumpReaction": construct.Flag,
    "iTotalDrops": common_types.Int,
    "fShakeAmplitude": common_types.Float,
    "fShakeSpeed": common_types.Float,
    "iMinHitsForMediumImpact": common_types.Int,
    "iMinHitsForLargeImpact": common_types.Int,
    "sImpactSoundSmallGroup": common_types.StrId,
    "sImpactSoundMediumGroup": common_types.StrId,
    "sImpactSoundLargeGroup": common_types.StrId,
    "sMoveSoundSmallGroup": common_types.StrId,
    "sMoveSoundMediumGroup": common_types.StrId,
    "sMoveSoundLargeGroup": common_types.StrId,
    "iMaxPopulationForSmallGroup": common_types.UInt,
    "iMaxPopulationForMediumGroup": common_types.UInt,
    "fMaxTimeAlive": common_types.Float,
    "fMinTimeAlive": common_types.Float,
    "fMaxDistToLinkNodes": common_types.Float,
    "fMeleeRepelRadius": common_types.Float,
    "fMeleeKillRatio": common_types.Float,
    "iMeleeMinKills": common_types.Int,
    "iMeleeMaxKills": common_types.Int,
    "fMeleeMinRepelDistance": common_types.Float,
    "fMeleeMaxRepelDistance": common_types.Float,
    "fMissileRepelRadius": common_types.Float,
    "fMissileKillRatio": common_types.Float,
    "iMissileMinKills": common_types.Int,
    "iMissileMaxKills": common_types.Int,
    "fMissileMinRepelDistance": common_types.Float,
    "fMissileMaxRepelDistance": common_types.Float,
    "fMigrationCheckMinTime": common_types.Float,
    "fMigrationCheckMaxTime": common_types.Float,
    "fDefaultDiversionTimer": common_types.Float,
    "fMinStunTime": common_types.Float,
    "fMaxStunTime": common_types.Float,
    "fDefaultBeamsRadiusIncrement": common_types.Float,
    "fWideBeamRadiusIncrement": common_types.Float,
    "fPlasmaBeamRadiusIncrement": common_types.Float,
    "oDamageSourceFactor": CDamageSourceFactor,
    "bDiesOfLoneliness": construct.Flag,
    "iLonelinessGroupSize": common_types.Int,
    "bApplyLonelinessToEachGroup": construct.Flag,
    "bWeakToSpinAttack": construct.Flag,
    "bIsWater": construct.Flag,
})


class CCharClassFlockingSwarmControllerComponent_SRotationMode(enum.IntEnum):
    Raw = 0
    Inclinate = 1
    Invalid = 2147483647


construct_CCharClassFlockingSwarmControllerComponent_SRotationMode = StrictEnum(CCharClassFlockingSwarmControllerComponent_SRotationMode)

CCharClassFlockingSwarmControllerComponent = Object(CCharClassFlockingSwarmControllerComponentFields := {
    **CCharClassSwarmControllerComponentFields,
    "fContaimentDist": common_types.Float,
    "eRotationMode": construct_CCharClassFlockingSwarmControllerComponent_SRotationMode,
    "fMaxAngularSpeed": common_types.Float,
    "fCohesion": common_types.Float,
    "fSeparationFactor": common_types.Float,
    "fSeparation": common_types.Float,
    "fToTarget": common_types.Float,
    "fContainment": common_types.Float,
    "bAllowSharpTurns": construct.Flag,
    "bCanFollowTarget": construct.Flag,
    "fPreferredRadius": common_types.Float,
    "fMinRadius": common_types.Float,
    "fPursuitSpeed": common_types.Float,
    "fRecoverySpeed": common_types.Float,
    "fAttackSpeed": common_types.Float,
    "fBillboardScale": common_types.Float,
    "bForceAllowTurn": construct.Flag,
    "fHareDistance": common_types.Float,
    "fMaxQueueSize": common_types.Float,
})

CCharClassRedenkiSwarmControllerComponent = Object(CCharClassRedenkiSwarmControllerComponentFields := {
    **CCharClassFlockingSwarmControllerComponentFields,
    "fDistToStartCharge": common_types.Float,
    "fDistToEndRecovery": common_types.Float,
    "bAlwaysForceRailMovement": construct.Flag,
    "fPathRecalculationTime": common_types.Float,
    "fAttackPathLength": common_types.Float,
    "fDistToForceAttack": common_types.Float,
    "fMinChaos": common_types.Float,
    "fMaxChaos": common_types.Float,
    "fMinMovementAnimSpeed": common_types.Float,
    "fMaxMovementAnimSpeed": common_types.Float,
    "fWallChargeStunDuration": common_types.Float,
    "sCombatSoundSmallGroup": common_types.StrId,
    "sCombatSoundMediumGroup": common_types.StrId,
    "sCombatSoundLargeGroup": common_types.StrId,
    "sPreparationSoundSmallGroup": common_types.StrId,
    "sPreparationSoundMediumGroup": common_types.StrId,
    "sPreparationSoundLargeGroup": common_types.StrId,
    "sStartChargeSoundSmallGroup": common_types.StrId,
    "sStartChargeSoundMediumGroup": common_types.StrId,
    "sStartChargeSoundLargeGroup": common_types.StrId,
    "sCollisionWithWallSoundSmallGroup": common_types.StrId,
    "sCollisionWithWallSoundMediumGroup": common_types.StrId,
    "sCollisionWithWallSoundLargeGroup": common_types.StrId,
    "bPreparationBackAllowed": construct.Flag,
    "fMinPreparationTime": common_types.Float,
    "fBackDistanceLength": common_types.Float,
    "fBackDistanceWidth": common_types.Float,
    "fAttackCooldown": common_types.Float,
    "fAngleLimitDeg": common_types.Float,
    "fMinDistForAngleLimit": common_types.Float,
})

CCharClassDaivoSwarmControllerComponent = Object({
    **CCharClassRedenkiSwarmControllerComponentFields,
    "fVomitSpeed": common_types.Float,
})

CCharClassDamageSourcesTrack = Object({
    **base_global_timeline_CTrackFields,
    "sDamageSourcesMask": common_types.StrId,
})

CCharClassDamageTriggerComponent = Object({
    **CCharClassBaseDamageTriggerComponentFields,
    "fDamagePerTime": common_types.Float,
    "sDamagePerTime": common_types.StrId,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "sDamageSource": common_types.StrId,
    "sDamageID": common_types.StrId,
    "bIgnoreReaction": construct.Flag,
    "bContinuousDamageHit": construct.Flag,
    "eForceDamageModeHit": construct_EForcedDamageMode,
})

CCharClassDashMeleeDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassDashMeleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassDeactivateCaterzillaEvent = Object(base_global_timeline_CEventFields)

CCharClassDeactivateHecathonConeFXEvent = Object(base_global_timeline_CEventFields)

CCharClassDeathAnimTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassDeleteEntityEvent = Object({
    **base_global_timeline_CEventFields,
    "fTimeToDelete": common_types.Float,
})


class EDemolitionPhase(enum.IntEnum):
    NONE = 0
    Idle = 1
    StartSwelling = 2
    HeartBeat = 3
    Explosion = 4
    Invalid = 2147483647


construct_EDemolitionPhase = StrictEnum(EDemolitionPhase)

CCharClassDemolitionBlockLifeComponent = Object(CCharClassDemolitionBlockLifeComponentFields := {
    **CCharClassLifeComponentFields,
    "oDamageSourceFactor": CDamageSourceFactor,
    "iHitCount": common_types.Int,
    "fTimeAfterHuskDestroyed": common_types.Float,
    "fTimeAfterFirstHit": common_types.Float,
    "fTimeMaterialExplosive": common_types.Float,
    "fTimeAfterDiffuseHuskDestroyed": common_types.Float,
    "eDemolitionPhase": construct_EDemolitionPhase,
    "bHuskInitiallyRemoved": construct.Flag,
    "sCameraFXPresetHusk": common_types.StrId,
    "sCameraFXPresetOnImpact": common_types.StrId,
    "sCameraFXPresetOnDead": common_types.StrId,
})

CCharClassDemolitionBlockActivatableActorLifeComponent = Object({
    **CCharClassDemolitionBlockLifeComponentFields,
    "sActivatableObjAnim": common_types.StrId,
    "sActivatableObjAnimRelax": common_types.StrId,
})

CCharClassDetachFromMovingPlatformEvent = Object({
    **base_global_timeline_CEventFields,
    "bApplyPlatformImpulse": construct.Flag,
})

CCharClassDigTrack = Object(base_global_timeline_CTrackFields)

CCharClassDisableCollidersEvent = Object(base_global_timeline_CEventFields)

CCharClassDisableCollidersTrack = Object(base_global_timeline_CTrackFields)

CCharClassDisableEntityEvent = Object(base_global_timeline_CEventFields)

CCharClassDissipateChargeBeamOnCantFireTrack = Object(base_global_timeline_CTrackFields)

CCharClassDissolveFanMudEvent = Object(base_global_timeline_CEventFields)

CCharClassDizzeanSwarmControllerComponent = Object(CCharClassFlockingSwarmControllerComponentFields)

CCharClassDoorLifeComponent = Object(CCharClassDoorLifeComponentFields := {
    **CCharClassItemLifeComponentFields,
    "fMinTimeClosed": common_types.Float,
    "fMaxDistanceOpened": common_types.Float,
    "bUsesPresenceDetection": construct.Flag,
    "bPresenceOpenEnabled": construct.Flag,
    "bUseDoorLockOnLocked": construct.Flag,
    "vDefaultLightColor": common_types.CVector4D,
    "vBlockLightColor": common_types.CVector4D,
    "bVerticalDimensionInFrustum": construct.Flag,
    "bHorizontalDimensionInFrustum": construct.Flag,
    "bUseHeatDeviceActivation": construct.Flag,
    "bStartOpened": construct.Flag,
})

CCharClassDoorCentralUnitLifeComponent = Object(CCharClassDoorLifeComponentFields)

CCharClassDoorEmmyFXComponent = Object({
    **CCharClassComponentFields,
    "fLockedTime": common_types.Float,
})

CCharClassDoorGrapplePointComponent = Object({
    **CCharClassPullableGrapplePointComponentFields,
    "sGrappleColliderNames": base_global_CRntVector_base_global_CStrId_,
})


class CDoorShieldLifeComponent_EDoorsShieldType(enum.IntEnum):
    MISSILE = 0
    SUPERMISSILE = 1
    POWERBOOM = 2
    PLASMA = 3
    WAVE = 4
    WIDE = 5
    Invalid = 2147483647


construct_CDoorShieldLifeComponent_EDoorsShieldType = StrictEnum(CDoorShieldLifeComponent_EDoorsShieldType)

CCharClassDoorShieldLifeComponent = Object({
    **CCharClassItemLifeComponentFields,
    "bDisolveByMaterial": construct.Flag,
    "fTimeToStartDisolve": common_types.Float,
    "eDoorShieldType": construct_CDoorShieldLifeComponent_EDoorsShieldType,
})

CCharClassDoorShieldUnBlockEvent = Object(base_global_timeline_CEventFields)

CCharClassDoubleJumpEvent = Object(base_global_timeline_CEventFields)


class CCharClassDredhedAIComponent_ESubspecies(enum.IntEnum):
    Dredhed = 0
    Sakai = 1
    Invalid = 2147483647


construct_CCharClassDredhedAIComponent_ESubspecies = StrictEnum(CCharClassDredhedAIComponent_ESubspecies)

CCharClassDredhedDiveAttack = Object({
    **CCharClassAttackFields,
    "fHightBlendSpeed": common_types.Float,
})

CCharClassDredhedAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "eSubspecies": construct_CCharClassDredhedAIComponent_ESubspecies,
    "fTimeBetweenCharges": common_types.Float,
    "oDredhedDiveAttackDef": CCharClassDredhedDiveAttack,
})

CCharClassDredhedAttackComponent = Object(CCharClassAIAttackComponentFields)


class SDropProbabilities_SDir(enum.IntEnum):
    NONE = 0
    Front = 1
    Back = 2
    Up = 3
    Down = 4
    FrontUp = 5
    FrontDown = 6
    BackUp = 7
    BackDown = 8
    Player = 9
    Invalid = 2147483647


construct_SDropProbabilities_SDir = StrictEnum(SDropProbabilities_SDir)


class SDropProbabilities_SType(enum.IntEnum):
    NONE = 0
    Default = 1
    Melee = 2
    Invalid = 2147483647


construct_SDropProbabilities_SType = StrictEnum(SDropProbabilities_SType)

SDropProbabilities = Object({
    "iMinNumOfDroppedItems": common_types.Int,
    "iMaxNumOfDroppedItems": common_types.Int,
    "iMaxItemTypeMin": common_types.Int,
    "iMaxItemTypeMax": common_types.Int,
    "fNothingProbability": common_types.Float,
    "fLifeProbability": common_types.Float,
    "fLifeBigProbability": common_types.Float,
    "fMissileProbability": common_types.Float,
    "fMissileBigProbability": common_types.Float,
    "fPowerBombProbability": common_types.Float,
    "fPowerBombBigProbability": common_types.Float,
    "fXParasiteYellowTypeProbability": common_types.Float,
    "fXParasiteGreenTypeProbability": common_types.Float,
    "fXParasiteRedTypeProbability": common_types.Float,
    "fXParasiteOrangeTypeProbability": common_types.Float,
    "fXParasiteMiniNothingProbability": common_types.Float,
    "fXParasiteMiniYellowTypeProbability": common_types.Float,
    "fXParasiteMiniGreenTypeProbability": common_types.Float,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
    "fMaxZDisp": common_types.Float,
    "sNodeToDrop": common_types.StrId,
    "vNodeOffset": common_types.CVector3D,
    "vRawOffset": common_types.CVector3D,
    "eDirToDrop": construct_SDropProbabilities_SDir,
    "eType": construct_SDropProbabilities_SType,
    "bStrictDir": construct.Flag,
    "bForceAttract": construct.Flag,
    "bAutomaticGrab": construct.Flag,
    "iXCellsToDrop": common_types.Int,
    "iNumOfItemsToDropWithXCells": common_types.Int,
})

CCharClassDropComponent = Object({
    **CCharClassComponentFields,
    "bDropOnDeath": construct.Flag,
    "bDropItemOnDeath": construct.Flag,
    "bDropItemOnDeathByMelee": construct.Flag,
    "bRestrictFloorSectors": construct.Flag,
    "vDropOffset": common_types.CVector3D,
    "bCanDropXParasite": construct.Flag,
    "fXCellDropInitialSpeed": common_types.Float,
    "fXCellDropEndSpeed": common_types.Float,
    "fXCellDropTime": common_types.Float,
    "fXCellDropRotationAngSpeed": common_types.Float,
    "sXParasiteTypeMask": common_types.StrId,
    "oDropProbabilities": SDropProbabilities,
    "oMeleeChargeShotDropProbabilities": SDropProbabilities,
    "bSkipUsefulItemsRule": construct.Flag,
})

CCharClassDropItemCrazyEvent = Object({
    **base_global_timeline_CEventFields,
    "bForce": construct.Flag,
    "iMinNumOfDroppedItems": common_types.Int,
    "iMaxNumOfDroppedItems": common_types.Int,
    "iMaxItemTypeMin": common_types.Int,
    "iMaxItemTypeMax": common_types.Int,
    "fNothingProbability": common_types.Float,
    "fLifeProbability": common_types.Float,
    "fLifeBigProbability": common_types.Float,
    "fMissileProbability": common_types.Float,
    "fMissileBigProbability": common_types.Float,
    "fPowerBombProbability": common_types.Float,
    "fPowerBombBigProbability": common_types.Float,
    "fXParasiteYellowTypeProbability": common_types.Float,
    "fXParasiteGreenTypeProbability": common_types.Float,
    "fXParasiteRedTypeProbability": common_types.Float,
    "fXParasiteOrangeTypeProbability": common_types.Float,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
    "fMaxZDisp": common_types.Float,
    "sNode": common_types.StrId,
    "fOffsetX": common_types.Float,
    "fOffsetY": common_types.Float,
    "fOffsetZ": common_types.Float,
    "fRawOffsetX": common_types.Float,
    "fRawOffsetY": common_types.Float,
    "fRawOffsetZ": common_types.Float,
    "sDirection": common_types.StrId,
    "bStrictDirection": construct.Flag,
    "bForceAttract": construct.Flag,
    "bIgnoreAttractionRadius": construct.Flag,
    "bDoNotDropWithNormalMelee": construct.Flag,
})

CCharClassDropItemEvent = Object(base_global_timeline_CEventFields)

CCharClassDropItemOverwriteProbabilitiesEvent = Object({
    **base_global_timeline_CEventFields,
    "iMinNumOfDroppedItems": common_types.Int,
    "iMaxNumOfDroppedItems": common_types.Int,
    "iMaxItemTypeMin": common_types.Int,
    "iMaxItemTypeMax": common_types.Int,
    "fNothingProbability": common_types.Float,
    "fLifeProbability": common_types.Float,
    "fLifeBigProbability": common_types.Float,
    "fMissileProbability": common_types.Float,
    "fMissileBigProbability": common_types.Float,
    "fPowerBombProbability": common_types.Float,
    "fPowerBombBigProbability": common_types.Float,
    "fXParasiteYellowTypeProbability": common_types.Float,
    "fXParasiteGreenTypeProbability": common_types.Float,
    "fXParasiteRedTypeProbability": common_types.Float,
    "fXParasiteOrangeTypeProbability": common_types.Float,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
    "fMaxZDisp": common_types.Float,
    "sNode": common_types.StrId,
    "fOffsetX": common_types.Float,
    "fOffsetY": common_types.Float,
    "fOffsetZ": common_types.Float,
    "fRawOffsetX": common_types.Float,
    "fRawOffsetY": common_types.Float,
    "fRawOffsetZ": common_types.Float,
    "sDirection": common_types.StrId,
    "bStrictDirection": construct.Flag,
    "bForceAttract": construct.Flag,
    "bIgnoreAttractionRadius": construct.Flag,
    "bDoNotDropWithNormalMelee": construct.Flag,
    "eType": construct_SDropProbabilities_SType,
    "sNodes": common_types.StrId,
})

CCharClassDropXParasiteEvent = Object(base_global_timeline_CEventFields)


class CCharClassDropterAIComponent_ESubspecies(enum.IntEnum):
    Dropter = 0
    Sharpaw = 1
    Iceflea = 2
    Invalid = 2147483647


construct_CCharClassDropterAIComponent_ESubspecies = StrictEnum(CCharClassDropterAIComponent_ESubspecies)

CCharClassDropterDiveAttack = Object({
    **CCharClassAttackFields,
    "fStartAttackDistance": common_types.Float,
    "fMaxAttackTravelDistance": common_types.Float,
})

CCharClassDropterAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "bWantsIceExplosion": construct.Flag,
    "fMaxFreezeTime": common_types.Float,
    "fMinFreezeTime": common_types.Float,
    "fFreezeExplosionPreparationTime": common_types.Float,
    "fFreezeExplosionRadius": common_types.Float,
    "fFreezeExplosionDuration": common_types.Float,
    "fFreezeExplosionRemanentDuration": common_types.Float,
    "eSubspecies": construct_CCharClassDropterAIComponent_ESubspecies,
    "oDropterDiveAttackDef": CCharClassDropterDiveAttack,
})

CCharClassDummyAIComponent = Object({
    **CCharClassAIComponentFields,
    "bWantsDrawModelPrimitiveSet": construct.Flag,
})

CCharClassDummyMovement = Object({
    **CCharClassMovementComponentFields,
    "bCanFall": construct.Flag,
})

CCharClassElectrifyingAreaComponent = Object({
    **CCharClassComponentFields,
    "bShouldUpdateAreaOnStart": construct.Flag,
    "bShouldCoverPlatformsCompletely": construct.Flag,
    "fMinValidYNormal": common_types.Float,
    "fClockwiseDistance": common_types.Float,
    "fCounterClockwiseDistance": common_types.Float,
    "fTriggerHeight": common_types.Float,
    "fTriggerDownwardHeight": common_types.Float,
    "fFXHeight": common_types.Float,
    "fHeightTolerance": common_types.Float,
})

CCharClassEmmyAIComponent = Object(CCharClassEmmyAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "bControlsEmmyZoneLight": construct.Flag,
    "bCanUseTunnels": construct.Flag,
    "sInventoryItemOnKilled": common_types.StrId,
})

CCharClassEmmyAllowCheckTargetReachableInSmartLinkTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyAttackComponent = Object(CCharClassAIAttackComponentFields)

CCharClassEmmyCaveAIComponent = Object(CCharClassEmmyAIComponentFields)

CEmmyConfiguration = Object({
    "bEmmy1CanUseTunnels": construct.Flag,
    "bEmmy2CanUseTunnels": construct.Flag,
    "bEmmyGrabBeepSoundEnabled": construct.Flag,
    "bEmmyMovementSoundEnabled": construct.Flag,
    "bFasterChaseTunnelTransitionEnabledPhase1": construct.Flag,
    "bFasterChaseTunnelTransitionEnabledPhase2": construct.Flag,
    "bLocationRumbleEnabled": construct.Flag,
    "bOutOfCameraSpeedDeactivateInMiniMap": construct.Flag,
    "bPerceptionFeedbackEnabled": construct.Flag,
    "bPerceptionPhase1Search2InfiniteRadius": construct.Flag,
    "bPerceptionVisionConeVisible": construct.Flag,
    "bPhase1ChaseSpeedModulation": construct.Flag,
    "bPlayerNoiseEnabled": construct.Flag,
    "bPulseVisible": construct.Flag,
    "bRangeVisibleOnlyInPlayerFocusMode": construct.Flag,
    "bRumbleDemoMode": construct.Flag,
    "bSearchLoopSoundEnabled": construct.Flag,
    "bSearchUsesPatrolColorWhenTargetLost": construct.Flag,
    "bSetStopAndSearchAnimInLastPerception": construct.Flag,
    "bShowBehaviorDebug": construct.Flag,
    "bShowPulseBackground": construct.Flag,
    "bShowPulseGradient": construct.Flag,
    "bShowSearchPointDebug": construct.Flag,
    "bStallingDetectionEnabled": construct.Flag,
    "bStallingSpeedIncreaseEnabled": construct.Flag,
    "bTunnelStallingPreventionEnabled": construct.Flag,
    "bVisionConeThroughScenario": construct.Flag,
    "fChaseUnspawnEnemyCulledCount": common_types.Float,
    "fDetectDoorOpenedDistance": common_types.Float,
    "fDetectionRangeFadeIn": common_types.Float,
    "fDetectionRangeFadeOut": common_types.Float,
    "fDistanceToStartSwitchingTo3mInGrabPreparation": common_types.Float,
    "fDistanceToSwitchTo3mInGrabPreparation": common_types.Float,
    "fEmmyMovementSoundMaxAttDistance": common_types.Float,
    "fEmmyMovementSoundMinAttDistance": common_types.Float,
    "fEmmyMovementSoundVolume": common_types.Float,
    "fEmmySoundDistZoomWalkCamMaxAttDistance": common_types.Float,
    "fEmmySoundDistZoomWalkCamMinAttDistance": common_types.Float,
    "fEmmySoundDistZoomWalkCamVolumeMultiplier": common_types.Float,
    "fEmmySoundMaxAttDistance": common_types.Float,
    "fEmmySoundMinAttDistance": common_types.Float,
    "fEmmySoundPerceptionVolume": common_types.Float,
    "fEmmySoundVolume": common_types.Float,
    "fEmmySpeedIncreasedPerSecond": common_types.Float,
    "fGrabPreparationGraceTime": common_types.Float,
    "fGrabPreparationGraceTimeProbability": common_types.Float,
    "fGrabPreparationTime1": common_types.Float,
    "fGrabPreparationTime2": common_types.Float,
    "fGrabPreparationTime3": common_types.Float,
    "fGrabQTEFailTime": common_types.Float,
    "fGrabQTETime": common_types.Float,
    "fGrabSecondPreparationGraceTime": common_types.Float,
    "fGrabSecondPreparationGraceTimeProbability": common_types.Float,
    "fGrabSecondPreparationTime1": common_types.Float,
    "fGrabSecondPreparationTime2": common_types.Float,
    "fGrabSecondPreparationTime3": common_types.Float,
    "fGrabSecondQTETime": common_types.Float,
    "fGrabZoomOffset": common_types.Float,
    "fGrabZoomTime": common_types.Float,
    "fMaxEmmySmartLinkSpeedIncreased": common_types.Float,
    "fMaxEmmyWalkSpeedIncreased": common_types.Float,
    "fMinTimeToStayStretched": common_types.Float,
    "fPatrolSearchMaxTime": common_types.Float,
    "fPerceptionCentralVisionConeMinTimeToTrigger": common_types.Float,
    "fPerceptionVisionConeIntensity": common_types.Float,
    "fPhase1ChaseSpeed": common_types.Float,
    "fPhase1CloseChaseSpeed": common_types.Float,
    "fPhase1CloseDistChaseSpeed": common_types.Float,
    "fPhase1FarDistChaseSpeed": common_types.Float,
    "fPhase1OutOfCameraSpeed": common_types.Float,
    "fPhase1OutOfCameraSpeedDeactivateDistance": common_types.Float,
    "fPhase1PatrolSearch2Speed": common_types.Float,
    "fPhase1PatrolSearchSpeed": common_types.Float,
    "fPhase1PatrolSpeed": common_types.Float,
    "fPhase1PerceptionCentralVisionConeAperture": common_types.Float,
    "fPhase1PerceptionCentralVisionConeRadius": common_types.Float,
    "fPhase1PerceptionChaseRangeRadius": common_types.Float,
    "fPhase1PerceptionPatrolRangeRadius": common_types.Float,
    "fPhase1PerceptionPatrolSearchRangeRadius": common_types.Float,
    "fPhase1PerceptionSearch2RangeRadius": common_types.Float,
    "fPhase1PerceptionSearchRangeRadius": common_types.Float,
    "fPhase1Search2Speed": common_types.Float,
    "fPhase1SearchSpeed": common_types.Float,
    "fPhase2Chase2FeetAnticipationMaxDistance": common_types.Float,
    "fPhase2Chase2FeetAnticipationMinDistance": common_types.Float,
    "fPhase2Chase2FeetSoundMaxFrequency": common_types.Float,
    "fPhase2Chase2FeetSoundMedFrequency": common_types.Float,
    "fPhase2Chase2FeetSoundMinFrequency": common_types.Float,
    "fPhase2GrabDistance": common_types.Float,
    "fPhase2HeadProtectorLife": common_types.Float,
    "fPhase2HeadProtectorLifeRecoveredPerSecond": common_types.Float,
    "fPhase2OutOfCameraSpeedDeactivateDistance": common_types.Float,
    "fPhase2ProtectionHeadImpactedSpeedFactor": common_types.Float,
    "fPhase2ProtectionHeadImpactedSpeedFactorTime": common_types.Float,
    "fPhase2ProtectorDestroyedChase2FeetCloseSpeed": common_types.Float,
    "fPhase2ProtectorDestroyedChase2FeetFarSpeed": common_types.Float,
    "fPhase2ProtectorDestroyedChaseCloseSpeed": common_types.Float,
    "fPhase2ProtectorDestroyedChaseFarSpeed": common_types.Float,
    "fPhase2ProtectorDestroyedFarDistance": common_types.Float,
    "fPhase2ProtectorDestroyedOutOfCameraCloseSpeed": common_types.Float,
    "fPhase2ProtectorDestroyedOutOfCameraFarSpeed": common_types.Float,
    "fPhase2ProtectorOnChaseSpeed": common_types.Float,
    "fPhase2ProtectorOnOutOfCameraSpeed": common_types.Float,
    "fPhaseDisplacementFactor": common_types.Float,
    "fRumbleBaseGain": common_types.Float,
    "fRumbleDemoSpinSpeed": common_types.Float,
    "fRumbleDemoVibrationSpeed": common_types.Float,
    "fStallDetectionBigRadius": common_types.Float,
    "fStallDetectionSmallRadius": common_types.Float,
    "fStallDetectionTimeOnBigRadius": common_types.Float,
    "fStallDetectionTimeOnSmallRadius": common_types.Float,
    "fTargetLostLowLifeRareAnimProb": common_types.Float,
    "fTargetLostLowLifeVeryRareAnimProb": common_types.Float,
    "fTargetLostNavMeshFindProbability": common_types.Float,
    "fTargetLostNavMeshFindRadius": common_types.Float,
    "fTargetLostNavMeshNoFindPathMaxDistance": common_types.Float,
    "fTargetLostNavMeshNoFindPathMinDistance": common_types.Float,
    "fTargetLostNavMeshNoFindRadius": common_types.Float,
    "fTargetLostRouteFindInternalNodeProbability": common_types.Float,
    "fTargetLostRouteFindLastNodeProbability": common_types.Float,
    "fTimeGrowingDetectionRange": common_types.Float,
    "fTimeOutOfCameraToEndChase": common_types.Float,
    "fTimeToShowCurrentDetectionRange": common_types.Float,
    "fTimeToShowOnlyCurrentDetectionRange": common_types.Float,
    "fTimeToShowPreviousDetectionRange": common_types.Float,
    "fTwoFeetChaseDistanceToAnticipateCrouchAnim": common_types.Float,
    "fTwoFeetChaseDistanceToAnticipateStretchAnim": common_types.Float,
    "fTwoFeetChaseMinSpaceToStretch": common_types.Float,
    "fWaterSpeedFactor": common_types.Float,
    "iDetectDoorOpenedMode": common_types.Int,
    "iEmmyKeyAmount": common_types.Int,
    "iEmmyKeyCollectionMode": common_types.Int,
    "iGrabEmmySamusQTEMode": common_types.Int,
    "iRumbleWave": common_types.Int,
    "iStatesInRumble": common_types.Int,
    "iTargetLostLowLife": common_types.Int,
})

CCharClassEmmyCaveAIComponent_CTunableEmmyCaveAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fHeadHeatIncrementFactor": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeadHeatRecoveredPerSecond": common_types.Float,
})

CCharClassEmmyCheckReachableAndSetActionEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
})

CCharClassEmmyCheckSetSuccessActionEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
})

CCharClassEmmyClampPhaseDisplacementFactorTrack = Object({
    **base_global_timeline_CTrackFields,
    "fmin": common_types.Float,
    "fmax": common_types.Float,
})

CCharClassEmmyDeathRemoveCUEnergyEvent = Object(base_global_timeline_CEventFields)

CCharClassEmmyDeathShowMessageEvent = Object({
    **base_global_timeline_CEventFields,
    "sOnMessageSkippedLuaCallback": common_types.StrId,
})

CCharClassEmmyFloorSlideAllowedTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyForestAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmyForestAIComponent_CTunableEmmyForestAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fHeadHeatIncrementFactor": common_types.Float,
    "fHeadHeatIncrementFactorForGround": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeadHeatRecoveredPerSecond": common_types.Float,
})

CCharClassEmmyGrabOnlyImpactTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyGrabSamusAttack = Object(CCharClassAttackFields)

CCharClassEmmyIgnoreChaseModeReachableTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyIgnoreFocus = Object(base_global_timeline_CTrackFields)

CCharClassEmmyIgnoreStaggerTimeTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyLabAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmyLabAIComponent_CTunableEmmyLabAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fHeadHeatIncrementFactor": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeadHeatRecoveredPerSecond": common_types.Float,
    "fSpeedBoosterPhase1PatrolSpeed": common_types.Float,
    "fSpeedBoosterPhase1PatrolSearchSpeed": common_types.Float,
    "fSpeedBoosterPhase1PatrolSearch2Speed": common_types.Float,
    "fSpeedBoosterPhase1SearchSpeed": common_types.Float,
    "bSpeedBoosterPhase1ChaseSpeedModulation": construct.Flag,
    "fSpeedBoosterPhase1ChaseSpeed": common_types.Float,
    "fSpeedBoosterPhase1CloseChaseSpeed": common_types.Float,
    "fSpeedBoosterPhase1FarDistChaseSpeed": common_types.Float,
    "fSpeedBoosterPhase1CloseDistChaseSpeed": common_types.Float,
    "fSpeedBoosterPhase1OutOfCameraSpeed": common_types.Float,
    "fSpeedBoosterPhase1Search2Speed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorOnChaseSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorOnOutOfCameraSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedChaseFarSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedChaseCloseSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedChase2FeetFarSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedChase2FeetCloseSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedOutOfCameraFarSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectorDestroyedOutOfCameraCloseSpeed": common_types.Float,
    "fSpeedBoosterPhase2ProtectionHeadImpactedSpeedFactor": common_types.Float,
    "fSpeedBoosterAudioVolumeIncrease": common_types.Float,
})

CCharClassEmmyLaunchQTEVFXEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
})

CCharClassEmmyMagmaAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmyMagmaAIComponent_CTunableEmmyMagmaAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fHeadHeatIncrementFactor": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeadHeatRecoveredPerSecond": common_types.Float,
})

CCharClassEmmyMaintainChaseReachableTrack = Object(base_global_timeline_CTrackFields)


class EAIAnimationStates(enum.IntEnum):
    NONE = 0
    Idle = 1
    Walking = 2
    WalkingWall = 3
    WalkingCeil = 4
    Flying = 5
    Side = 6
    Invalid = 2147483647


construct_EAIAnimationStates = StrictEnum(EAIAnimationStates)


class CCharClassEnemyMovement_ETurn180Mode(enum.IntEnum):
    AxisX = 0
    AxisY = 1
    Dot = 2
    Invalid = 2147483647


construct_CCharClassEnemyMovement_ETurn180Mode = StrictEnum(CCharClassEnemyMovement_ETurn180Mode)


class EAnimationTag(enum.IntEnum):
    slope = 0
    stealth = 1
    left = 2
    right = 3
    shield = 4
    hiddenshield = 5
    attack = 6
    stage2 = 7
    super = 8
    low = 9
    preseta = 10
    presetb = 11
    presetc = 12
    chozowarriorx_powerbomb = 13
    slope26up = 14


construct_EAnimationTag = StrictEnum(EAnimationTag)

CCharClassEnemyMovement = Object(CCharClassEnemyMovementFields := {
    **CCharClassCharacterMovementFields,
    "bCanFall": construct.Flag,
    "bShouldMakeExtraMove": construct.Flag,
    "eInitialState": construct_EAIAnimationStates,
    "eTurn180Mode": construct_CCharClassEnemyMovement_ETurn180Mode,
    "sIdleAnim": common_types.StrId,
    "sWalkingRelaxAnim": common_types.StrId,
    "sWalkingFrontAnim": common_types.StrId,
    "sWalkingBackAnim": common_types.StrId,
    "sWalkingFrontInitAnim": common_types.StrId,
    "sWalkingBackInitAnim": common_types.StrId,
    "sWalkingFrontEndAnim": common_types.StrId,
    "sWalkingBackEndAnim": common_types.StrId,
    "sFlyingRelaxAnim": common_types.StrId,
    "sFlyingFrontAnim": common_types.StrId,
    "sFlyingBackAnim": common_types.StrId,
    "sFlyingUpAnim": common_types.StrId,
    "sFlyingDownAnim": common_types.StrId,
    "sFlyingFrontInitAnim": common_types.StrId,
    "sFlyingBackInitAnim": common_types.StrId,
    "sFlyingUpInitAnim": common_types.StrId,
    "sFlyingDownInitAnim": common_types.StrId,
    "sFlyingFrontEndAnim": common_types.StrId,
    "sFlyingBackEndAnim": common_types.StrId,
    "sFlyingUpEndAnim": common_types.StrId,
    "sFlyingDownEndAnim": common_types.StrId,
    "fFlyingStateChangeBlendTime": common_types.Float,
    "fFlyingUpStartAng": common_types.Float,
    "fFlyingDownStartAng": common_types.Float,
    "sSideRelaxAnim": common_types.StrId,
    "sSideWalkAnim": common_types.StrId,
    "sSideWalkInitAnim": common_types.StrId,
    "eSideLeftTag": construct_EAnimationTag,
    "eSideRightTag": construct_EAnimationTag,
    "iNumScenarioCollisionSteps": common_types.Int,
    "bOnLastCollisionStepHitResetTickVelocities": construct.Flag,
    "bUseCurrentScenarioCollisionScene": construct.Flag,
    "bRotateWhenMoving": construct.Flag,
    "fMinSpeedToRotate": common_types.Float,
    "fMaxSpeedToRotate": common_types.Float,
    "fMaxAngleRotationY": common_types.Float,
    "fDefaultAngleRotationY": common_types.Float,
    "fMaxAngleRotationZ": common_types.Float,
    "fDefaultAngleRotationZ": common_types.Float,
    "fSpeedToRotateFallingFromPath": common_types.Float,
    "sWalkUpAnim": common_types.StrId,
    "fWalkUpExitBlend": common_types.Float,
    "sWalkDownAnim": common_types.StrId,
    "fWalkDownExitBlend": common_types.Float,
    "fStickyDistanceToAnticipateCornerAnim": common_types.Float,
    "fStickyDistanceToQuitCornerAnim": common_types.Float,
    "bUseDistanceModeToChangeCornerAnim": construct.Flag,
    "bSynchronizeUpAnim": construct.Flag,
    "bSynchronizeDownAnim": construct.Flag,
    "fFlyingAngleAccumulativeInterpolationSpeedFactor": common_types.Float,
    "bUseFlyingAngleAccumulativeInterpolationSpeedFactor": construct.Flag,
    "bInPathMode": construct.Flag,
    "fMaxDistanceToExecuteRule": common_types.Float,
    "bUseBreakableTileBlockerCollidersOnSmartLink": construct.Flag,
    "fSupportedOnFloorTolerance": common_types.Float,
    "bBipedMode": construct.Flag,
    "bIgnoreOpenCorner": construct.Flag,
    "bRelocateOnFrozen": construct.Flag,
    "bForceNextTransformCharClassScale": construct.Flag,
    "fAngularSpeed": common_types.Float,
    "fSteeringAcceleration": common_types.Float,
    "fMaxTargetDistanceToAccelerateCloseToTarget": common_types.Float,
    "fCloseToTargetAcceleration": common_types.Float,
    "bLookAtHorizontalDir": construct.Flag,
})

CCharClassEmmyMovement = Object({
    **CCharClassEnemyMovementFields,
    "sWalkingWallUpRelaxAnim": common_types.StrId,
    "sWalkingWallUpFrontAnim": common_types.StrId,
    "sWalkingWallUpBackAnim": common_types.StrId,
    "sWalkingWallUpFrontInitAnim": common_types.StrId,
    "sWalkingWallUpBackInitAnim": common_types.StrId,
    "sWalkingWallUpFrontEndAnim": common_types.StrId,
    "sWalkingWallUpBackEndAnim": common_types.StrId,
    "sWalkingWallDownRelaxAnim": common_types.StrId,
    "sWalkingWallDownFrontAnim": common_types.StrId,
    "sWalkingWallDownBackAnim": common_types.StrId,
    "sWalkingWallDownFrontInitAnim": common_types.StrId,
    "sWalkingWallDownBackInitAnim": common_types.StrId,
    "sWalkingWallDownFrontEndAnim": common_types.StrId,
    "sWalkingWallDownBackEndAnim": common_types.StrId,
    "sWalkingCeilRelaxAnim": common_types.StrId,
    "sWalkingCeilFrontAnim": common_types.StrId,
    "sWalkingCeilBackAnim": common_types.StrId,
    "sWalkingCeilFrontInitAnim": common_types.StrId,
    "sWalkingCeilBackInitAnim": common_types.StrId,
    "sWalkingCeilFrontEndAnim": common_types.StrId,
    "sWalkingCeilBackEndAnim": common_types.StrId,
    "sWalkingPatrolRelaxAnim": common_types.StrId,
    "sWalkingPatrolFrontAnim": common_types.StrId,
    "sWalkingPatrolBackAnim": common_types.StrId,
    "sWalkingPatrolFrontInitAnim": common_types.StrId,
    "sWalkingPatrolBackInitAnim": common_types.StrId,
    "sWalkingPatrolFrontEndAnim": common_types.StrId,
    "sWalkingPatrolBackEndAnim": common_types.StrId,
    "sWalkingWallUpPatrolRelaxAnim": common_types.StrId,
    "sWalkingWallUpPatrolFrontAnim": common_types.StrId,
    "sWalkingWallUpPatrolBackAnim": common_types.StrId,
    "sWalkingWallUpPatrolFrontInitAnim": common_types.StrId,
    "sWalkingWallUpPatrolBackInitAnim": common_types.StrId,
    "sWalkingWallUpPatrolFrontEndAnim": common_types.StrId,
    "sWalkingWallUpPatrolBackEndAnim": common_types.StrId,
    "sWalkingWallDownPatrolRelaxAnim": common_types.StrId,
    "sWalkingWallDownPatrolFrontAnim": common_types.StrId,
    "sWalkingWallDownPatrolBackAnim": common_types.StrId,
    "sWalkingWallDownPatrolFrontInitAnim": common_types.StrId,
    "sWalkingWallDownPatrolBackInitAnim": common_types.StrId,
    "sWalkingWallDownPatrolFrontEndAnim": common_types.StrId,
    "sWalkingWallDownPatrolBackEndAnim": common_types.StrId,
    "sWalkingCeilPatrolRelaxAnim": common_types.StrId,
    "sWalkingCeilPatrolFrontAnim": common_types.StrId,
    "sWalkingCeilPatrolBackAnim": common_types.StrId,
    "sWalkingCeilPatrolFrontInitAnim": common_types.StrId,
    "sWalkingCeilPatrolBackInitAnim": common_types.StrId,
    "sWalkingCeilPatrolFrontEndAnim": common_types.StrId,
    "sWalkingCeilPatrolBackEndAnim": common_types.StrId,
    "sWalkingTunnelRelaxAnim": common_types.StrId,
    "sWalkingTunnelFrontAnim": common_types.StrId,
    "sWalkingTunnelBackAnim": common_types.StrId,
    "sWalkingTunnelFrontInitAnim": common_types.StrId,
    "sWalkingTunnelBackInitAnim": common_types.StrId,
    "sWalkingTunnelFrontEndAnim": common_types.StrId,
    "sWalkingTunnelBackEndAnim": common_types.StrId,
})

CCharClassEmmyProtoAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmyProtoAIComponent_CTunableEmmyProtoAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fGrabTutoCameraDistance": common_types.Float,
})

CCharClassEmmySancAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmySancAIComponent_CTunableEmmySancAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
    "fHeadHeatIncrementFactor": common_types.Float,
    "fHeadHeatIncrementFactorDuringPursuit": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeadHeatRecoveredPerSecond": common_types.Float,
})

CCharClassEmmyShipyardAIComponent = Object(CCharClassEmmyAIComponentFields)

CCharClassEmmyShipyardAIComponent_CTunableEmmyShipyardAIComponent = Object({
    **base_tunable_CTunableFields,
    "rConfig": CEmmyConfiguration,
})

CCharClassEmmySmartLinkInvalidZoneTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassEmmyStopAndSearchTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyTunnelTransitionTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyValveComponent = Object(CCharClassComponentFields)

CCharClassEmmyVisionConeOffTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyVisionConeOnTrack = Object(base_global_timeline_CTrackFields)

CCharClassEmmyWaveMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassEnableCollidersEvent = Object(base_global_timeline_CEventFields)

CCharClassEnableCullingEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassEnableScenarioItemByNameEvent = Object({
    **base_global_timeline_CEventFields,
    "sItemName": common_types.StrId,
    "bEnable": construct.Flag,
})

CCharClassEndGrabEvent = Object(base_global_timeline_CEventFields)

CCharClassEnhanceWeakSpotComponent = Object(CCharClassEnhanceWeakSpotComponentFields := {
    **CCharClassComponentFields,
    "sOnWeakSpotAimed": PropertyEnum,
    "sOnWeakSpotNotAimed": PropertyEnum,
})


class CEscapeSequenceExplosionComponent_EExplosionType(enum.IntEnum):
    SMALL = 0
    MEDIUM = 1
    BIG = 2
    Invalid = 2147483647


construct_CEscapeSequenceExplosionComponent_EExplosionType = StrictEnum(CEscapeSequenceExplosionComponent_EExplosionType)

CCharClassEscapeSequenceExplosionComponent = Object({
    **CCharClassComponentFields,
    "eExplosionType": construct_CEscapeSequenceExplosionComponent_EExplosionType,
})

CCharClassEventPropComponent = Object(CCharClassComponentFields)

CCharClassEventScenarioComponent = Object(CCharClassComponentFields)

CCharClassFXComponent = Object(CCharClassComponentFields)

CCharClassFXControlTrack = Object({
    **base_global_timeline_CTrackFields,
    "sActive": common_types.StrId,
    "sEnabled": common_types.StrId,
})

CCharClassFXCrazyTrack = Object(base_global_timeline_CTrackFields)

CCharClassFXCreateAndLinkBaseEvent = Object(CCharClassFXCreateAndLinkBaseEventFields := ICharClassFXCreateAndLinkEventFields)

CCharClassFXCreateAndLinkAndNotifyAIEvent = Object(CCharClassFXCreateAndLinkBaseEventFields)

CCharClassFXCreateAndLinkEvent = Object(CCharClassFXCreateAndLinkBaseEventFields)

CCharClassFXCreateTrailEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "sMaterial": common_types.StrId,
    "eLinkType": construct_ELinkType,
    "sBone": common_types.StrId,
    "fColorR": common_types.Float,
    "fColorG": common_types.Float,
    "fColorB": common_types.Float,
    "fColorA": common_types.Float,
    "fLength": common_types.Float,
    "fStepLength": common_types.Float,
    "fWidth": common_types.Float,
    "bUVCycling": construct.Flag,
    "fUVCyclingDistance": common_types.Float,
    "fLifeTime": common_types.Float,
    "fPositionOffsetX": common_types.Float,
    "fPositionOffsetY": common_types.Float,
    "fPositionOffsetZ": common_types.Float,
    "fRotationOffsetX": common_types.Float,
    "fRotationOffsetY": common_types.Float,
    "fRotationOffsetZ": common_types.Float,
})

CCharClassFXDeleteEvent = Object(ICharClassFXDeleteEventFields)

CCharClassFXDisolveEvent = Object({
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
})

CCharClassFXFadeEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "fTime": common_types.Float,
    "fIntensitySrc": common_types.Float,
    "fIntensityDst": common_types.Float,
    "bEnableBefore": construct.Flag,
    "bDisableAfter": construct.Flag,
})

CCharClassFXLinkEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "eLinkType": construct_ELinkType,
    "fPositionOffsetX": common_types.Float,
    "fPositionOffsetY": common_types.Float,
    "fPositionOffsetZ": common_types.Float,
    "fAngleOffsetX": common_types.Float,
    "fAngleOffsetY": common_types.Float,
    "fAngleOffsetZ": common_types.Float,
    "sAdditional": common_types.StrId,
})

CCharClassFXPlayModelEffectAnim = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassFXSetActiveEvent = Object(ICharClassFXSetActiveEventFields)

CCharClassFXSetAutoManagedEvent = Object(ICharClassFXSetAutoManagedEventFields)

CCharClassFXSetEnabledEvent = Object(ICharClassFXSetEnabledEventFields)

CCharClassFXSetMaterialPropertyEvent = Object({
    **base_global_timeline_CEventFields,
    "sFXId": common_types.StrId,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
    "fColorR": common_types.Float,
    "fColorG": common_types.Float,
    "fColorB": common_types.Float,
    "fColorA": common_types.Float,
    "fHDR": common_types.Float,
})

CCharClassFXSetMaterialPropertyTransitionEvent = Object({
    **base_global_timeline_CEventFields,
    "sFXId": common_types.StrId,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
    "fColorR": common_types.Float,
    "fColorG": common_types.Float,
    "fColorB": common_types.Float,
    "fColorA": common_types.Float,
    "fHDR": common_types.Float,
    "fTime": common_types.Float,
})

CCharClassFXStopAllFXEvent = Object(base_global_timeline_CEventFields)

CCharClassFXStopMaterialTransitionEvent = Object({
    **base_global_timeline_CEventFields,
    "sFXId": common_types.StrId,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
})

CCharClassFXStopModelEffectAnim = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassFXUnlinkEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassFactionComponent = Object(CCharClassComponentFields)

CCharClassFadeInEvent = Object(CCharClassBaseFadeInEventFields)

CCharClassFadeOutEvent = Object({
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
    "fR": common_types.Float,
    "fG": common_types.Float,
    "fB": common_types.Float,
})

CCharClassFadeOutMusicEvent = Object({
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
})

CCharClassFadeToBlackDeathTrack = Object(base_global_timeline_CTrackFields)

CCharClassFakeDropEvent = Object({
    **base_global_timeline_CEventFields,
    "iNumLife": common_types.Int,
    "iNumMissile": common_types.Int,
})

CCharClassFallAfterFrozenTrack = Object(base_global_timeline_CTrackFields)

CCharClassFallForwardTrack = Object(base_global_timeline_CTrackFields)

CCharClassFallInitTrack = Object(base_global_timeline_CTrackFields)

CCharClassFallTrack = Object(base_global_timeline_CTrackFields)

CCharClassFanComponent = Object({
    **CCharClassBaseTriggerComponentFields,
    "sFX_wind": common_types.StrId,
    "sFX_hurricane": common_types.StrId,
})

CCharClassFanCoolDownComponent = Object(CCharClassComponentFields)

CCharClassFingSwarmControllerComponent = Object(CCharClassFlockingSwarmControllerComponentFields)

CCharClassFireActionBaseTrack = Object(CCharClassFireActionBaseTrackFields := {
    **CCharClassTweakActionBaseTrackFields,
    "bWantsRecoil": construct.Flag,
    "sActionForward": common_types.StrId,
    "sActionForwardShort": common_types.StrId,
    "sActionBackward": common_types.StrId,
    "sActionBackwardShort": common_types.StrId,
})

CCharClassFireActionTrack = Object(CCharClassFireActionBaseTrackFields)

CCharClassFixRotationEvent = Object(base_global_timeline_CEventFields)

CCharClassFleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlide26Track = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlide45Track = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideAirMorphBallTransitionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassFloorSlideCanRelaunchTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideDefaultMeleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideEnlargeCollisionTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideFallInitTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideInitTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideRunTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideShrinkCollisionTrack = Object(base_global_timeline_CTrackFields)

CCharClassFloorSlideTrack = Object(base_global_timeline_CTrackFields)

CCharClassFlotingPropActingStopFlotationEvent = Object(base_global_timeline_CEventFields)

CCharClassFlyingTrack = Object(base_global_timeline_CTrackFields)

CCharClassForbidImmediateShinesparkDownTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceAIUpdateFXEvent = Object(base_global_timeline_CEventFields)


class EAimDirection(enum.IntEnum):
    NONE = 0
    Up = 1
    FrontUp = 2
    Front = 3
    FrontDown = 4
    Down = 5
    Invalid = 2147483647


construct_EAimDirection = StrictEnum(EAimDirection)

CCharClassForceAimDirectionTrack = Object({
    **base_global_timeline_CTrackFields,
    "eDirection": construct_EAimDirection,
})

CCharClassForceAnalogInputAngTrack = Object({
    **base_global_timeline_CTrackFields,
    "bForce": construct.Flag,
    "fAngle": common_types.Float,
    "bIgnoreOnFire": construct.Flag,
})

CCharClassForceBossCameraTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceBringDropsTrack = Object({
    **base_global_timeline_CTrackFields,
    "fSpeedIncrementFactor": common_types.Float,
})

CCharClassForceBumpFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "sColliders": common_types.StrId,
})

CCharClassForceCameraDetphEntityPositionZeroTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceChangeToSubareaEvent = Object({
    **base_global_timeline_CEventFields,
    "sSubareaID": common_types.StrId,
    "bInCutscene": construct.Flag,
    "bFade": construct.Flag,
})

CCharClassForceDeadEvent = Object({
    **base_global_timeline_CEventFields,
    "bLaunchDeadAnimation": construct.Flag,
    "bSetPlayerAsInstigator": construct.Flag,
})

CCharClassForceDefaultActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "brelax": construct.Flag,
    "brun": construct.Flag,
    "bWhileAimPressed": construct.Flag,
})

CCharClassForceDisableSubareaEvent = Object({
    **base_global_timeline_CEventFields,
    "sSubareaID": common_types.StrId,
    "bAllSubareaItems": construct.Flag,
    "bScenarioCollider": construct.Flag,
    "bLightGroup": construct.Flag,
    "bSoundGroup": construct.Flag,
    "bSceneGroup": construct.Flag,
    "bLogicEntityGroup": construct.Flag,
    "bBreakableTileGroupGroup": construct.Flag,
    "bEnvironmentPreset": construct.Flag,
    "bEnvironmentSoundPreset": construct.Flag,
    "bEnvironmentMusicPreset": construct.Flag,
})

CCharClassForceEnableSubareaEvent = Object({
    **base_global_timeline_CEventFields,
    "sSubareaID": common_types.StrId,
    "bAllSubareaItems": construct.Flag,
    "bScenarioCollider": construct.Flag,
    "bLightGroup": construct.Flag,
    "bSoundGroup": construct.Flag,
    "bSceneGroup": construct.Flag,
    "bLogicEntityGroup": construct.Flag,
    "bBreakableTileGroupGroup": construct.Flag,
    "bEnvironmentPreset": construct.Flag,
    "bEnvironmentSoundPreset": construct.Flag,
    "bEnvironmentMusicPreset": construct.Flag,
})

CCharClassForceHyperBeamFireTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceMeleeActionTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceMoveInDesiredViewDirectionTrack = Object(base_global_timeline_CTrackFields)

CCharClassForceRotationOnActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sLeftAction": common_types.StrId,
    "sRightAction": common_types.StrId,
})

CCharClassForceUpdateEnvironmentEvent = Object(base_global_timeline_CEventFields)

CCharClassFreezeInFrameTrack = Object(base_global_timeline_CTrackFields)

CCharClassFromRecoilBlendTimeOverrideTrack = Object({
    **base_global_timeline_CTrackFields,
    "fValue": common_types.Float,
})

CCharClassFrozenComponent = Object(CCharClassFrozenComponentFields := {
    **CCharClassComponentFields,
    "fTotalFreezeTime": common_types.Float,
    "fThawingTime": common_types.Float,
    "sTimelineIdOnFrozen": common_types.StrId,
    "sTimelineIdOnThawing": common_types.StrId,
    "sTimelineIdOnUnfreeze": common_types.StrId,
    "sActionFreezeInit": common_types.StrId,
    "sActionFreezeEnd": common_types.StrId,
    "sActionFreezeEndFalling": common_types.StrId,
    "sCustomLayer": common_types.StrId,
    "sCustomLayerMixerNode": common_types.StrId,
})

std_unique_ptr_CBarelyFrozenIceInfo_ = Pointer_CBarelyFrozenIceInfo.create_construct()

base_global_CRntVector_std_unique_ptr_CBarelyFrozenIceInfo__ = common_types.make_vector(std_unique_ptr_CBarelyFrozenIceInfo_)

CCharClassFrozenAsFrostbiteComponent = Object({
    **CCharClassFrozenComponentFields,
    "iRequiredFrostbiteLevel": common_types.Int,
    "fFrostbiteLevelResetTime": common_types.Float,
    "fAfterHitNoFrostbiteLevelResetTime": common_types.Float,
    "sTimelineIdOnFrostbiteStart": common_types.StrId,
    "sTimelineIdOnFrostbiteStop": common_types.StrId,
    "bShouldDieWithDashMelee": construct.Flag,
    "tBarelyIceInfo": base_global_CRntVector_std_unique_ptr_CBarelyFrozenIceInfo__,
})

CCharClassFrozenAsPlatformComponent = Object({
    **CCharClassFrozenComponentFields,
    "sCollisionMaskToFreeze": common_types.StrId,
    "sCollisionTagsExcludedFromFreezing": common_types.StrId,
    "fPlatformDepth": common_types.Float,
    "sIceCubeCharClass": common_types.StrId,
    "vIceCubeSize": common_types.CVector2D,
})

CCharClassFulmiteBellyMineAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fLifeTime": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fTimeToExplosion": common_types.Float,
    "fTimeAtMaxRadiusExplosion": common_types.Float,
    "fDamageFulmiteBellyMineExplosion": common_types.Float,
    "fNormalXFactor": common_types.Float,
    "fNormalYFactor": common_types.Float,
    "fUpsideDownXFactor": common_types.Float,
    "fUpsideDownYFactor": common_types.Float,
    "fInWallXFactor": common_types.Float,
    "fInWallYFactor": common_types.Float,
    "uGroundRebounds": common_types.UInt,
    "fWallImpulseXFactor": common_types.Float,
    "fWallImpulseYFactor": common_types.Float,
    "fGroundImpulseXFactor": common_types.Float,
    "fGroundImpulseYFactor": common_types.Float,
    "bPlayReboundActions": construct.Flag,
    "fImpulseVelocityXLimit": common_types.Float,
    "fImpulseVelocityYLimit": common_types.Float,
    "fTimeToShowBeforeExplosionFX": common_types.Float,
    "fMinTimeBetweenBeeps": common_types.Float,
    "fMaxTimeBetweenBeeps": common_types.Float,
    "fMinBeepVolume": common_types.Float,
    "fMaxBeepVolume": common_types.Float,
    "fMinBeepPitch": common_types.Float,
    "fMaxBeepPitch": common_types.Float,
})

CCharClassFulmiteBellyMineAttackComponent = Object(CCharClassAIAttackComponentFields)

CCharClassFulmiteBellyMineMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassFusibleBoxComponent = Object(CCharClassComponentFields)

CCharClassGeneratorActivatedNotificationEvent = Object(base_global_timeline_CEventFields)

CCharClassGhostDashTrack = Object(base_global_timeline_CTrackFields)

CCharClassGhostDashTrailTrack = Object(base_global_timeline_CTrackFields)

CCharClassGhostTimeTrack = Object(base_global_timeline_CTrackFields)

CCharClassGobblerBiteAttack = Object(CCharClassAttackFields)

CCharClassGobblerAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oGobblerBiteAttackDef": CCharClassGobblerBiteAttack,
    "fMinImpulseFactorX": common_types.Float,
    "fMinImpulseFactorY": common_types.Float,
    "fMaxImpulseFactorX": common_types.Float,
    "fMaxImpulseFactorY": common_types.Float,
    "fDistForMaxImpulse": common_types.Float,
    "fDistForMinImpulse": common_types.Float,
    "fDistanceToBiteAttack": common_types.Float,
    "fMinNervousnessDist": common_types.Float,
    "fMaxNervousnessDist": common_types.Float,
})

CCharClassGobblerAIComponent_CTunableCharClassGobblerAIComponent = Object(base_tunable_CTunableFields)

CCharClassGobblerApplyCustomImpulseTrack = Object(base_global_timeline_CTrackFields)

CCharClassGobblerCanCounterAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassGobblerEyeOpenTrack = Object(base_global_timeline_CTrackFields)

CCharClassGobblerIgnorePrefixChangeTrack = Object(base_global_timeline_CTrackFields)

CCharClassGoliathAttack = Object(CCharClassGoliathAttackFields := {
    **CCharClassAttackFields,
    "fPostAttackLoopDuration": common_types.Float,
})

CCharClassGoliathAIComponent = Object(CCharClassGoliathAIComponentFields := {
    **CCharClassBaseBigFistAIComponentFields,
    "oGoliathAttackDef": CCharClassGoliathAttack,
    "fAnimSpeedMultiplier": common_types.Float,
})

CCharClassGoliathAIComponent_CTunableCharClassGoliathAIComponent = Object({
    **base_tunable_CTunableFields,
    "fFleeTimeToReturnToPatrol": common_types.Float,
    "fChaseMinDistance": common_types.Float,
    "fChaseMaxDistance": common_types.Float,
})

CCharClassGoliathAttack_CTunableCharClassGoliathAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fMaxAttackDistanceWShockwave": common_types.Float,
    "fFrontSpaceToForbidAttack": common_types.Float,
    "fShockWaveLength": common_types.Float,
    "fShockWaveTimeGrowing": common_types.Float,
    "fShockWaveTimeAtMaxRadius": common_types.Float,
    "fShockWaveAttackHeight": common_types.Float,
})

CCharClassGoliathXBurstProjectionBombsAttack = Object({
    **CCharClassAttackFields,
    "fChargingTime": common_types.Float,
    "fTimeBetweenWaves": common_types.Float,
    "uNumWaves": common_types.UInt,
})

CCharClassGoliathXSlamAttack = Object(CCharClassGoliathAttackFields)

CCharClassGoliathXAIComponent = Object({
    **CCharClassGoliathAIComponentFields,
    "oGoliathXBurstProjectionBombsAttackDef": CCharClassGoliathXBurstProjectionBombsAttack,
    "oGoliathXSlamAttackDef": CCharClassGoliathXSlamAttack,
})

CCharClassGoliathXBurstProjectionBombMovement = Object({
    **CCharClassWeaponMovementFields,
    "fExplosionRadius": common_types.Float,
    "fExplosionGrowthTime": common_types.Float,
    "fExplosionLifeTime": common_types.Float,
    "fSubExplosionLifeTime": common_types.Float,
    "fSubExplosionStepTime": common_types.Float,
    "fClosestAxisSpeedMultiplier": common_types.Float,
    "fDetonationTime": common_types.Float,
})


class CCharClassGooplotAIComponent_ESubspecies(enum.IntEnum):
    Gooplot = 0
    Gooshocker = 1
    Invalid = 2147483647


construct_CCharClassGooplotAIComponent_ESubspecies = StrictEnum(CCharClassGooplotAIComponent_ESubspecies)

CCharClassGooplotJumpAttack = Object(CCharClassAttackFields)

CCharClassGooplotUndoJumpAttack = Object(CCharClassAttackFields)

CCharClassGooplotAIComponent = Object(CCharClassGooplotAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "eSubspecies": construct_CCharClassGooplotAIComponent_ESubspecies,
    "fExplosionTime": common_types.Float,
    "oGooplotJumpAttackDef": CCharClassGooplotJumpAttack,
    "oGooplotUndoJumpAttackDef": CCharClassGooplotUndoJumpAttack,
})

CCharClassGooplotAIComponent_CTunableCharClassGooplotAIComponent = Object({
    **base_tunable_CTunableFields,
    "fAwareTime": common_types.Float,
    "fAttackRecoveryTime": common_types.Float,
    "iMaxJumps": common_types.Int,
    "fMaxSingleJumpTime": common_types.Float,
    "iStaminaLossPerParry": common_types.Int,
    "fAttackTrackingTime": common_types.Float,
    "fAttackAirSpeed": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fExplosionDamage": common_types.Float,
    "fExplosionTime": common_types.Float,
    "fJumpTargetYOffset1": common_types.Float,
    "fJumpTargetYOffset2": common_types.Float,
    "fJumpTargetYOffset3": common_types.Float,
})

CCharClassGooplotCapsuleComponent = Object(CCharClassComponentFields)

CCharClassGooplotJumpAttack_CTunableCharClassGooplotJumpAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassGooplotUndoJumpAttack_CTunableCharClassGooplotUndoJumpAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassGooshockerAIComponent = Object({
    **CCharClassGooplotAIComponentFields,
    "fShockAttackDuration": common_types.Float,
})

CCharClassGrabAddRootMotionTrack = Object({
    **base_global_timeline_CTrackFields,
    "fX": common_types.Float,
    "fY": common_types.Float,
    "fZ": common_types.Float,
})


class base_global_timeline_ELayer(enum.IntEnum):
    Layer_0 = 0
    Layer_1 = 1
    Layer_2 = 2
    Layer_3 = 3
    Layer_4 = 4
    Layer_5 = 5
    Layer_6 = 6
    Layer_7 = 7


construct_base_global_timeline_ELayer = StrictEnum(base_global_timeline_ELayer)

base_global_timeline_TLayers = construct.FlagsEnum(construct.Int32ul, construct_base_global_timeline_ELayer.enum_class)

CCharClassGrabComponent = Object({
    **CCharClassComponentFields,
    "sFireCameraFXPreset": common_types.StrId,
    "oAnimationLayers": base_global_timeline_TLayers,
})

CCharClassGrabInterpolateActorPositionsTrack = Object(base_global_timeline_CTrackFields)

CCharClassGrabbedTrackTrack = Object({
    **base_global_timeline_CTrackFields,
    "sGrabbedNode": common_types.StrId,
    "bMarksPosition": construct.Flag,
    "bMarksRotation": construct.Flag,
})

CCharClassGrabberTrackTrack = Object({
    **base_global_timeline_CTrackFields,
    "sGrabberNode": common_types.StrId,
    "sGrabbedAnimation": common_types.StrId,
    "bMarksPosition": construct.Flag,
    "bMarksRotation": construct.Flag,
    "sWorksWith": common_types.StrId,
})

CCharClassGrappleBeamComponent = Object({
    **CCharClassWeaponMovementFields,
    "fDamage": common_types.Float,
})

CCharClassGrappleFinalPullEndEvent = Object({
    **base_global_timeline_CEventFields,
    "sAction": common_types.StrId,
})


class ESamusUsingGrapplePullPointStatePullStage(enum.IntEnum):
    NONE = 0
    ControlledPull = 1
    UncontrolledPull = 2
    FinalPull = 3
    Invalid = 2147483647


construct_ESamusUsingGrapplePullPointStatePullStage = StrictEnum(ESamusUsingGrapplePullPointStatePullStage)

CCharClassGrappleTrack = Object({
    **base_global_timeline_CTrackFields,
    "ePullStage": construct_ESamusUsingGrapplePullPointStatePullStage,
    "sSwingAccelImpulseAnim": common_types.StrId,
    "sSwingEndAnim": common_types.StrId,
})

CCharClassGrazeTrack = Object(base_global_timeline_CTrackFields)

CCharClassGroundShockerAttack = Object(CCharClassAttackFields)

CCharClassGroundShockerAIComponent = Object({
    **CCharClassBaseGroundShockerAIComponentFields,
    "oGroundShockerAttackDef": CCharClassGroundShockerAttack,
})

CCharClassGroundShockerAIComponent_CTunableCharClassGroundShockerAIComponent = Object({
    **base_tunable_CTunableFields,
    "fCombatMotionSpeed": common_types.Float,
    "fMotionSpeed": common_types.Float,
})

CCharClassGroundShockerAttack_CTunableCharClassGroundShockerAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fInitLoopDuration": common_types.Float,
    "fHitLoopDuration": common_types.Float,
    "fVulnerableAfterHitDuration": common_types.Float,
    "fVulnerableOnPushDuration": common_types.Float,
})

CCharClassGroundShockerIsVulnerableTrack = Object(base_global_timeline_CTrackFields)

CCharClassGunCheckBackAnalogDistanceTrack = Object(base_global_timeline_CTrackFields)

CCharClassGunCheckBackAnalogFallDistanceTrack = Object(base_global_timeline_CTrackFields)

CCharClassGunCheckBackHangDistanceTrack = Object(base_global_timeline_CTrackFields)

CCharClassGunUnpossessCheckCantFireTrack = Object(base_global_timeline_CTrackFields)


class GUI_CHUD_EForceVisibilityState(enum.IntEnum):
    DONT_FORCE = 0
    FORCE_VISIBLE_WITH_FADE = 1
    FORCE_INVISIBLE_WITH_FADE = 2
    FORCE_VISIBLE_NO_FADE = 3
    FORCE_INVISIBLE_NO_FADE = 4


construct_GUI_CHUD_EForceVisibilityState = StrictEnum(GUI_CHUD_EForceVisibilityState)

CCharClassHUDSetForceVisibilityStateEvent = Object({
    **base_global_timeline_CEventFields,
    "eForceVisibilityState": construct_GUI_CHUD_EForceVisibilityState,
})

CCharClassHangInitTrack = Object(base_global_timeline_CTrackFields)

CCharClassHangShotTrack = Object(base_global_timeline_CTrackFields)

CCharClassHangTrack = Object(base_global_timeline_CTrackFields)

CCharClassHangableGrappleSurfaceComponent = Object(CCharClassHangableGrappleSurfaceComponentFields := {
    **CCharClassGrapplePointComponentFields,
    "fMagnetSurfaceMaxIntensityOnGrappleNotAllowed": common_types.Float,
    "sGrappleHelperColliderId": common_types.StrId,
    "fGrappleHelperMaxSegmentLengthToUseCenter": common_types.Float,
})

CCharClassHangableGrappleMagnetSlidingBlockComponent = Object(CCharClassHangableGrappleSurfaceComponentFields)

CCharClassHeatableShieldEnhanceWeakSpotComponent = Object({
    **CCharClassEnhanceWeakSpotComponentFields,
    "sOnWeakSpotAimedWithMask": PropertyEnum,
    "sOnWeakSpotAimedWithoutMask": PropertyEnum,
    "sOnWeakSpotNotAimedWithMask": PropertyEnum,
    "sOnWeakSpotNotAimedWithoutMask": PropertyEnum,
})


class CCharClassHecathonAIComponent_ESubspecies(enum.IntEnum):
    Hecathon = 0
    Omnithon = 1
    Invalid = 2147483647


construct_CCharClassHecathonAIComponent_ESubspecies = StrictEnum(CCharClassHecathonAIComponent_ESubspecies)

CCharClassHecathonAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "eSubspecies": construct_CCharClassHecathonAIComponent_ESubspecies,
})

CCharClassHecathonAIComponent_CTunableCharClassHecathoAIComponent = Object({
    **base_tunable_CTunableFields,
    "fTimeToGoPatrol": common_types.Float,
    "fPatrolEatPreparationTime": common_types.Float,
    "fFeedAnimPreparationTime": common_types.Float,
    "fStopFeedAnimPreparationTime": common_types.Float,
    "fPatrolEatDurationMin": common_types.Float,
    "fPatrolEatDurationMax": common_types.Float,
    "fPatrolEatCooldownMin": common_types.Float,
    "fPatrolEatCooldownMax": common_types.Float,
    "fTimeToPlanktonDamage": common_types.Float,
    "fExtraDistanceDamage": common_types.Float,
    "fDistanceToNoticeOtherHecathons": common_types.Float,
    "fTimeToChangeBetweenModes": common_types.Float,
    "fTimeToAdjustDir": common_types.Float,
    "fDistToEndPathToAttack": common_types.Float,
    "fTimeToChangeSpeed": common_types.Float,
    "fSpeedFactor": common_types.Float,
    "fTimeToEat": common_types.Float,
})

CCharClassHecathonLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassHecathonPlanktonFXComponent = Object({
    **CCharClassComponentFields,
    "sModelResPath": common_types.StrId,
    "fScale": common_types.Float,
    "fScaleRandom": common_types.Float,
    "vRotation": common_types.CVector3D,
    "vRotationRandom": common_types.CVector3D,
})

CCharClassHideAreaNameEvent = Object({
    **base_global_timeline_CEventFields,
    "fFade": common_types.Float,
})

CCharClassHideCutsceneActorEvent = Object({
    **base_global_timeline_CEventFields,
    "sActorNameLike": common_types.StrId,
    "bResetMaterialAnimation": construct.Flag,
})

CCharClassHideHUDTrack = Object({
    **base_global_timeline_CTrackFields,
    "bHUD": construct.Flag,
    "bMiniMap": construct.Flag,
})

CCharClassHideMessageEvent = Object({
    **base_global_timeline_CEventFields,
    "sMissionLogTutoId": common_types.StrId,
})

CCharClassHideNodeEvent = Object({
    **base_global_timeline_CEventFields,
    "sNode": common_types.StrId,
})

CCharClassHideProtectorEvent = Object(base_global_timeline_CEventFields)

CCharClassHideScenarioItemByNameEvent = Object({
    **base_global_timeline_CEventFields,
    "sItemName": common_types.StrId,
    "bHideItem": construct.Flag,
    "bResetMaterialAnimation": construct.Flag,
})

CCharClassHomingMovement = Object(CCharClassProjectileMovementFields)

CCharClassHydrogigaAttack = Object(CCharClassHydrogigaAttackFields := CCharClassAttackFields)

CCharClassHydrogigaBraidAttack = Object({
    **CCharClassHydrogigaAttackFields,
    "fPrepareTime": common_types.Float,
    "fHitTime": common_types.Float,
})

CCharClassHydrogigaMaelstormAttack = Object(CCharClassHydrogigaAttackFields)

std_unique_ptr_CPolypFallPattern_ = Pointer_CPolypFallPattern.create_construct()

base_global_CRntVector_std_unique_ptr_CPolypFallPattern__ = common_types.make_vector(std_unique_ptr_CPolypFallPattern_)

CCharClassHydrogigaPolypsAttack = Object({
    **CCharClassHydrogigaAttackFields,
    "iAttackPattern": common_types.Int,
    "fTimeBetweenWaves": common_types.Float,
    "uMinNumWaves": common_types.UInt,
    "uMaxNumWaves": common_types.UInt,
    "tUnbreakableFarPatterns": base_global_CRntVector_std_unique_ptr_CPolypFallPattern__,
    "tUnbreakableMiddlePatterns": base_global_CRntVector_std_unique_ptr_CPolypFallPattern__,
    "tUnbreakableClosePatterns": base_global_CRntVector_std_unique_ptr_CPolypFallPattern__,
})

CCharClassHydrogigaTentacleBashAttack = Object(CCharClassHydrogigaAttackFields)

CCharClassHydrogigaTongueSwirlAttack = Object(CCharClassHydrogigaAttackFields)

CCharClassHydrogigaAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "tTentacles": base_global_CRntVector_std_unique_ptr_CTentacle__,
    "oHydrogigaBraidAttackDef": CCharClassHydrogigaBraidAttack,
    "oHydrogigaMaelstormAttackDef": CCharClassHydrogigaMaelstormAttack,
    "oHydrogigaPolypsAttackDef": CCharClassHydrogigaPolypsAttack,
    "oHydrogigaTentacleBashAttackDef": CCharClassHydrogigaTentacleBashAttack,
    "oHydrogigaTongueSwirlAttackDef": CCharClassHydrogigaTongueSwirlAttack,
    "fTimeOpened": common_types.Float,
    "fTimeDry": common_types.Float,
    "fTimeStunned": common_types.Float,
    "fUnderwaterZipLineMultiplier": common_types.Float,
    "fTurbineRestoreTime": common_types.Float,
    "bMeleeDestroyPolyps": construct.Flag,
    "fMaxDamageDry": common_types.Float,
    "fMaxDamageStunned": common_types.Float,
    "fDamageStage2": common_types.Float,
    "fDamageFactorFillingPool": common_types.Float,
    "oDamageSourceFactorClose": CDamageSourceFactor,
    "oDamageSourceFactorOpen": CDamageSourceFactor,
    "oDamageSourceFactorDry": CDamageSourceFactor,
    "oDamageSourceFactorPolyps": CDamageSourceFactor,
})

CCharClassHydrogigaAIComponent_CTunableCharClassHydrogigaAIComponent = Object({
    **base_tunable_CTunableFields,
    "HYDROGIGA_BRAID_ATTACK": construct.Flag,
    "HYDROGIGA_MAELSTORM_ATTACK": construct.Flag,
    "HYDROGIGA_POLYPS_ATTACK": construct.Flag,
    "HYDROGIGA_TENTACLE_BASH_ATTACK": construct.Flag,
    "HYDROGIGA_TONGUE_SWIRL_ATTACK": construct.Flag,
})

CCharClassHydrogigaCancelAttackActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCancelAction": common_types.StrId,
})

CCharClassHydrogigaHalfEmptyTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaSetZiplinesRailEnabledEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassHydrogigaTentacleC01FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaTentacleC02FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaTentacleL01FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaTentacleL02FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaTentacleR01FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassHydrogigaTentacleR02FXTrack = Object(base_global_timeline_CTrackFields)

CCharClassMagnetSlidingBlockComponent = Object(CCharClassMagnetSlidingBlockComponentFields := {
    **CCharClassComponentFields,
    "bFreezeOnFinish": construct.Flag,
    "bActiveRailCameraOnFinish": construct.Flag,
    "fMinMovementPercentToForceContinueMovingOnStopHang": common_types.Float,
})

CCharClassHydrogigaZiplineComponent = Object({
    **CCharClassMagnetSlidingBlockComponentFields,
    "fMovementMultiplierUnderwater": common_types.Float,
    "fWaterLevelToSlowDownBeforeUnderwater": common_types.Float,
    "fWaterLevelToConsiderUnderwater": common_types.Float,
    "fTimeToMatchMovementMultiplierGoingBackToStartUnderwater": common_types.Float,
    "fTimeToMatchMovementMultiplierSlowingDown": common_types.Float,
})

CCharClassHyperBeamRecoilTrack = Object(base_global_timeline_CTrackFields)

CCharClassHyperDashTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAINavigationTrack = Object({
    **base_global_timeline_CTrackFields,
    "sSpeedSampleNode": common_types.StrId,
})

CCharClassIgnoreAITrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAbilityActivationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAbsorbTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAimBlendToDefaultTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAimLaserTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAimPressedTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAimTrack = Object({
    **base_global_timeline_CTrackFields,
    "bAllowLaser": construct.Flag,
})

CCharClassIgnoreAirMovementTrack = Object({
    **base_global_timeline_CTrackFields,
    "bResetPhysicsVelocityX": construct.Flag,
})

CCharClassIgnoreAnalogWideInitTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAngryTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreAttackTrack = Object({
    **base_global_timeline_CTrackFields,
    "bKeepApplyingAfterAnimationIsFinished": construct.Flag,
})

CCharClassIgnoreAutoLockOnMeleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreBossCameraFinishedTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreBossCameraTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreBumpFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "sColliders": common_types.StrId,
})

CCharClassIgnoreCalculateAimAngleToTargetTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCameraUseBoundariesTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCantFallTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreChangeSegmentOnInpathTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCharacterPlayerCollisionTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreClearNormalizedAnalogInputTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreClimbTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCollisionMaskTrack = Object({
    **base_global_timeline_CTrackFields,
    "sMasksToIgnore": common_types.StrId,
    "sMasksToEnforce": common_types.StrId,
})

CCharClassIgnoreCollisionTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreColorChangeTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCombatTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreConvertToSamusTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCrazyEndCounterTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCrazyEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCrouchEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreCrouchTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreDamageInFloorSlideTunnelTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreDamageWithFeedbackTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreDeathTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreDefaultDropItemEventTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreEmmySpeedOverrideTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFallEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFloorSlide45Track = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFollowPathActionSpeedInterpolationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFollowPathSpeedInterpolationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFollowPathTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreFreezeTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGaleTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGenerateNavigablePathTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGhostAuraTrack = Object({
    **base_global_timeline_CTrackFields,
    "bCancelAbility": construct.Flag,
})

CCharClassIgnoreGoingToGrapplePointImpulseTrack = Object({
    **base_global_timeline_CTrackFields,
    "fIgnoredImpulseMultiplier": common_types.Float,
})

CCharClassIgnoreGotoSideNavigationStateTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGrabSlavePositionInterpolationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGrappleAbortTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGrapplePullTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGrappleSelectionTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGravityTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreGrazeTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreHangTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreHangTransitionToShootingPoseTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreHitsFromMeleeFailEntityTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreHyperBeamTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreImpactTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreInPathNextSmartLinkTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreInputTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreInterpolationTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreJumpTrack = Object({
    **base_global_timeline_CTrackFields,
    "bBufferInput": construct.Flag,
})

CCharClassIgnoreKraidBellyBombAnimationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreLaserFXTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreLaunchEmmyGrabByDistanceTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMagnetGloveMovementTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMeleeHitReactionDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMeleeHitTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMeleeTrack = Object({
    **base_global_timeline_CTrackFields,
    "bBufferInput": construct.Flag,
})

CCharClassIgnoreMetroidCameraOffsetsTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreModifyForceDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMorphballTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMotionSpeedTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreMovementTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreOpticCamouflageTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnorePatrolTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnorePerceptionTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnorePriorityOfFallOnChangeDirTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnorePushTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRailTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreReactionTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRecoilTopBoneMaskTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRecoveryFrozenTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRelocateInPathTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRodotukSuckAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRotateToInstigatorTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRotateWhenMovingTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreRotationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSecondaryGun = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSetSmartLinkMovementStateTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSlomoInLowWaterTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSlopeIKBlendingTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSmartLinkMovementTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSmartLinkRulesTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSonarTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSpeedBoosterTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreStartSmartLinkUseTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreStopAndSearchTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreStopGrappleImpulseTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreStoppedTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreSuspendTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreTurnForEvent = Object({
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
    "bLockViewDirChange": construct.Flag,
})

CCharClassIgnoreTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreUsableInterpolationTrack = Object(base_global_timeline_CTrackFields)

CCharClassIgnoreViewDirChangeTrack = Object(base_global_timeline_CTrackFields)

CCharClassImpactMeleeDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassImpactedTrack = Object(CCharClassToStateTrackFields)

CCharClassInfesterShootAttack = Object(CCharClassAttackFields)

CCharClassInfesterReloadAttack = Object(CCharClassAttackFields)


class CCharClassInfesterAIComponent_ESubspecies(enum.IntEnum):
    Infester = 0
    Fulmite = 1
    Invalid = 2147483647


construct_CCharClassInfesterAIComponent_ESubspecies = StrictEnum(CCharClassInfesterAIComponent_ESubspecies)

CCharClassInfesterAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fTimeToReloadBeam": common_types.Float,
    "sProjectileModelName": common_types.StrId,
    "oInfesterShootAttackDef": CCharClassInfesterShootAttack,
    "oInfesterReloadAttackDef": CCharClassInfesterReloadAttack,
    "eSubspecies": construct_CCharClassInfesterAIComponent_ESubspecies,
})

CCharClassInfesterBallAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fLifeTime": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fTimeToExplosion": common_types.Float,
    "fTimeAtMaxRadiusExplosion": common_types.Float,
    "fDamageInfesterBallExplosion": common_types.Float,
    "bChangeDirOnLand": construct.Flag,
    "fXImpulseInWallSpawn": common_types.Float,
    "bNotExplodeInWallCollision": construct.Flag,
    "iNumCollisionsToExplode": common_types.Int,
    "iNumWallCollisions": common_types.Int,
    "bExplodeInVerticalTunnelCollision": construct.Flag,
    "fTunnelImpulseFactor": common_types.Float,
    "fReboundInWallFactor": common_types.Float,
    "fReboundInGroundFactor": common_types.Float,
    "fReboundInSlopeFactor": common_types.Float,
})

CCharClassInfesterBallAttackComponent = Object(CCharClassAIAttackComponentFields)

CCharClassInfesterBallLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassInfesterBallMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassInfesterBallResetRotationEvent = Object(base_global_timeline_CEventFields)

CCharClassInfesterLaunchBallEvent = Object({
    **base_global_timeline_CEventFields,
    "bFulmiteMine": construct.Flag,
})

CCharClassInstantMorphballConversionTrack = Object(base_global_timeline_CTrackFields)


class CInterpolationComponent_EInterpolationType(enum.IntEnum):
    ACCUMULATIVE = 0
    LINEAR = 1
    INSTANT = 2
    EASY_IN_EASY_OUT = 3
    Invalid = 2147483647


construct_CInterpolationComponent_EInterpolationType = StrictEnum(CInterpolationComponent_EInterpolationType)

CCharClassInterpolatePositionTrack = Object({
    **base_global_timeline_CTrackFields,
    "eType": construct_CInterpolationComponent_EInterpolationType,
    "fInterpolationSpeed": common_types.Float,
})


class CInterpolationComponent_EInterpDirection(enum.IntEnum):
    INDIR_Left = 0
    INDIR_Right = 1
    INDIR_Any = 2
    Invalid = 2147483647


construct_CInterpolationComponent_EInterpDirection = StrictEnum(CInterpolationComponent_EInterpDirection)

CCharClassInterpolateRotationTrack = Object({
    **base_global_timeline_CTrackFields,
    "eType": construct_CInterpolationComponent_EInterpolationType,
    "eDirection": construct_CInterpolationComponent_EInterpDirection,
    "fInterpolationSpeed": common_types.Float,
})

CCharClassInvertRotationEvent = Object({
    **base_global_timeline_CEventFields,
    "bRaw": construct.Flag,
})

CCharClassJumpTrack = Object(base_global_timeline_CTrackFields)

CCharClassKeepAttackOnSubareaChangeTrack = Object(base_global_timeline_CTrackFields)

CCharClassKeepAutoLockOnTargetTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidAttack = Object(CCharClassKraidAttackFields := CCharClassAttackFields)

std_unique_ptr_CKraidSpinningNailsDef_ = Pointer_CKraidSpinningNailsDef.create_construct()

base_global_CRntVector_std_unique_ptr_CKraidSpinningNailsDef__ = common_types.make_vector(std_unique_ptr_CKraidSpinningNailsDef_)

base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CKraidSpinningNailsDef___ = common_types.make_vector(base_global_CRntVector_std_unique_ptr_CKraidSpinningNailsDef__)

CCharClassKraidSpinningNailsAttack = Object({
    **CCharClassKraidAttackFields,
    "tPatternsPhase1": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CKraidSpinningNailsDef___,
    "tPatternsPhase2": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CKraidSpinningNailsDef___,
})

CCharClassKraidBackSlapAttack = Object(CCharClassKraidAttackFields)

CCharClassKraidFierceSwipeAttack = Object(CCharClassKraidAttackFields)

std_unique_ptr_CAcidBlobsLaunchPattern_ = Pointer_CAcidBlobsLaunchPattern.create_construct()

base_global_CRntVector_std_unique_ptr_CAcidBlobsLaunchPattern__ = common_types.make_vector(std_unique_ptr_CAcidBlobsLaunchPattern_)

base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CAcidBlobsLaunchPattern___ = common_types.make_vector(base_global_CRntVector_std_unique_ptr_CAcidBlobsLaunchPattern__)

CCharClassKraidAcidBlobsAttack = Object({
    **CCharClassKraidAttackFields,
    "sEndAttackAnim": common_types.StrId,
    "fDuration": common_types.Float,
    "fUnbreakableGravity": common_types.Float,
    "fBreakableGravity": common_types.Float,
    "fMaxAngle": common_types.Float,
    "fMinAngle": common_types.Float,
    "tLaunchPatterns": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CAcidBlobsLaunchPattern___,
})

CCharClassKraidFlyingSpikesAttack = Object({
    **CCharClassKraidAttackFields,
    "fSpike1VerticalOffset": common_types.Float,
    "fSpike1HorizontalOffset": common_types.Float,
    "fSpike2VerticalOffset": common_types.Float,
    "fSpike2HorizontalOffset": common_types.Float,
    "fSpike3VerticalOffset": common_types.Float,
    "fSpike3HorizontalOffset": common_types.Float,
})

CCharClassKraidTripleFlyingSpikesAttack = Object({
    **CCharClassKraidAttackFields,
    "fSpike1VerticalOffset": common_types.Float,
    "fSpike1HorizontalOffset": common_types.Float,
    "fSpike2VerticalOffset": common_types.Float,
    "fSpike2HorizontalOffset": common_types.Float,
    "fSpike3VerticalOffset": common_types.Float,
    "fSpike3HorizontalOffset": common_types.Float,
})

std_unique_ptr_CBouncingCreaturesLaunchPattern_ = Pointer_CBouncingCreaturesLaunchPattern.create_construct()

base_global_CRntVector_std_unique_ptr_CBouncingCreaturesLaunchPattern__ = common_types.make_vector(std_unique_ptr_CBouncingCreaturesLaunchPattern_)

base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CBouncingCreaturesLaunchPattern___ = common_types.make_vector(base_global_CRntVector_std_unique_ptr_CBouncingCreaturesLaunchPattern__)

CCharClassKraidBouncingCreaturesAttack = Object({
    **CCharClassKraidAttackFields,
    "sEndAttackAnim": common_types.StrId,
    "tPatterns": base_global_CRntVector_base_global_CRntVector_std_unique_ptr_CBouncingCreaturesLaunchPattern___,
})

CCharClassKraidShockerSplashAttack = Object(CCharClassKraidAttackFields)

CCharClassKraidAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "oKraidSpinningNailsAttackDef": CCharClassKraidSpinningNailsAttack,
    "oKraidBackSlapAttackDef": CCharClassKraidBackSlapAttack,
    "oKraidFierceSwipeAttackDef": CCharClassKraidFierceSwipeAttack,
    "oKraidAcidBlobsAttackDef": CCharClassKraidAcidBlobsAttack,
    "oKraidFlyingSpikesAttackDef": CCharClassKraidFlyingSpikesAttack,
    "oKraidTripleFlyingSpikesAttackDef": CCharClassKraidTripleFlyingSpikesAttack,
    "oKraidBouncingCreaturesAttackDef": CCharClassKraidBouncingCreaturesAttack,
    "oKraidShockerSplashAttackDef": CCharClassKraidShockerSplashAttack,
    "fOpenMouthInterpolationSpeed": common_types.Float,
    "fDesiredTimeToCloseMouth": common_types.Float,
    "fDamageToCloseMouth": common_types.Float,
    "fBellyLife": common_types.Float,
    "fMinTimeToRelaxAction": common_types.Float,
    "fMaxTimeToRelaxAction": common_types.Float,
    "fTimeToUncoverBelly": common_types.Float,
    "fIgnoreOpenMouthTimeAfterCloseMouth": common_types.Float,
    "fTimeToBellyDamage": common_types.Float,
    "fBellyButtonRadius": common_types.Float,
    "oGrabDamageSourceFactor": CDamageSourceFactor,
    "oFierceswipeActingDamageSourceFactor": CDamageSourceFactor,
})

CCharClassKraidAIComponent_CTunableCharClassKraidAIComponent = Object({
    **base_tunable_CTunableFields,
    "fFlyingSpikeMotionSpeed": common_types.Float,
    "fFlyingSpikeStickedWallTime": common_types.Float,
    "fZipLineDownTime": common_types.Float,
    "iInitialStage": common_types.Int,
    "uBombsToDieInMorphGrab": common_types.UInt,
    "SPINNING_NAILS": construct.Flag,
    "BACK_SLAP": construct.Flag,
    "ACID_BLOBS": construct.Flag,
    "FLYING_SPIKES": construct.Flag,
    "TRIPLE_FLYING_SPIKES": construct.Flag,
    "BOUNCING_CREATURES": construct.Flag,
    "SHOCKER_SPLASH": construct.Flag,
    "FIERCE_SWIPE": construct.Flag,
})

CCharClassKraidAcidBlobsAttack_CTunableCharClassKraidAcidBlobsAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassKraidAcidBlobsMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fRotationFactor": common_types.Float,
})

CCharClassKraidAllowGhostDashGrabTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidBackSlapAttack_CTunableCharClassKraidBackSlapAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassKraidBellyDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidBellyGrabTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidBouncingCreaturesAttack_CTunableCharClassKraidBouncingCreaturesAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "iPattern": common_types.Int,
})

CCharClassKraidBouncingCreaturesMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fRotationFactor": common_types.Float,
})

CCharClassKraidCanAbortFierceSwipeAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidCanUncoverBellyTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidCheckDeadInGrabEvent = Object(base_global_timeline_CEventFields)

CCharClassKraidFierceSwipeAttack_CTunableCharClassKraidFierceSwipeAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassKraidFlyingSpikesAttack_CTunableCharClassKraidFlyingSpikesAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassKraidIgnoreHeadDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidIgnoreMouthAdditiveActionsTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidLaunchDeathCutsceneEvent = Object(base_global_timeline_CEventFields)

CCharClassKraidMouthOpenedTrack = Object(base_global_timeline_CTrackFields)

CCharClassKraidMoveDownZiplineEvent = Object(base_global_timeline_CEventFields)

CCharClassKraidNailMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fRotationFactor": common_types.Float,
    "fPhase1LeftHandCloseSpeed": common_types.Float,
    "fPhase1LeftHandFarSpeed": common_types.Float,
    "fPhase1RightHandCloseSpeed": common_types.Float,
    "fPhase1RightHandFarSpeed": common_types.Float,
    "fPhase2LeftHandSpeed": common_types.Float,
    "fPhase2RightHandSpeed": common_types.Float,
})

CCharClassKraidSetOpenMouthFactorEvent = Object({
    **base_global_timeline_CEventFields,
    "fFactor": common_types.Float,
})

CCharClassKraidShockerSplashAttack_CTunableCharClassKraidShockerSplashAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassKraidShockerSplashMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassMovablePlatformComponent = Object(CCharClassMovablePlatformComponentFields := {
    **CCharClassMovementComponentFields,
    "sMovableColliderId": common_types.StrId,
    "bDisableOnActivatedOnLoadScenario": construct.Flag,
})

CCharClassKraidSpikeMovablePlatformComponent = Object({
    **CCharClassMovablePlatformComponentFields,
    "fInitialMotionSpeed": common_types.Float,
    "fMotionSpeed": common_types.Float,
    "fInitialDisplacement": common_types.Float,
    "fPreparationTime": common_types.Float,
    "fShakeDisplacementX": common_types.Float,
    "fShakeSpeedX": common_types.Float,
    "fShakeDisplacementY": common_types.Float,
    "fShakeSpeedY": common_types.Float,
    "fFlyingSpikeStickedWallTime": common_types.Float,
})

CCharClassKraidSpinningNailsAttack_CTunableCharClassKraidSpinningNailsAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "iPattern": common_types.Int,
})

CCharClassKraidTripleFlyingSpikesAttack_CTunableCharClassKraidTripleFlyingSpikesAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
})

CCharClassLandingTrack = Object(base_global_timeline_CTrackFields)

CCharClassLaunchJumpFXEvent = Object(base_global_timeline_CEventFields)

CCharClassLiquidPoolComponent = Object(CCharClassLiquidPoolComponentFields := {
    **CCharClassBaseDamageTriggerComponentFields,
    "sLiquidMaterial0": common_types.StrId,
    "sLiquidMaterial1": common_types.StrId,
    "sSolidMaterial0": common_types.StrId,
    "sSolidMaterial1": common_types.StrId,
})

CCharClassLavaPoolComponent = Object({
    **CCharClassLiquidPoolComponentFields,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "sLevelChangeEasingFunction": common_types.StrId,
})

CCharClassLavaPumpComponent = Object(CCharClassActivatableComponentFields)

CCharClassLetBossDieTrack = Object(base_global_timeline_CTrackFields)

CCharClassLifeComponent_CTunableCharClassLifeComponent = Object({
    **base_tunable_CTunableFields,
    "fLifeArachnus": common_types.Float,
    "fLifeArmadigger": common_types.Float,
    "fLifeAutclast": common_types.Float,
    "fLifeAutector": common_types.Float,
    "fLifeAutomper": common_types.Float,
    "fLifeAutool": common_types.Float,
    "fLifeAutsharp": common_types.Float,
    "fLifeAutsniper": common_types.Float,
    "fLifeBatalloon": common_types.Float,
    "fLifeBigFist": common_types.Float,
    "fLifeBigkranX": common_types.Float,
    "fLifeBlindFly": common_types.Float,
    "fLifeCaterzilla": common_types.Float,
    "fLifeCentralUnitArmorCaves": common_types.Float,
    "fLifeCentralUnitArmorForest": common_types.Float,
    "fLifeCentralUnitArmorLaboratory": common_types.Float,
    "fLifeCentralUnitArmorMagma": common_types.Float,
    "fLifeCentralUnitArmorPlaceholder": common_types.Float,
    "fLifeCentralUnitArmorSanctuary": common_types.Float,
    "fLifeCentralUnitCaves": common_types.Float,
    "fLifeCentralUnitForest": common_types.Float,
    "fLifeCentralUnitLaboratory": common_types.Float,
    "fLifeCentralUnitMagma": common_types.Float,
    "fLifeCentralUnitPlaceholder": common_types.Float,
    "fLifeCentralUnitSanctuary": common_types.Float,
    "fLifeChozoCommander": common_types.Float,
    "fLifeChozoCommanderEnergyShards": common_types.Float,
    "fLifeChozoCommanderSentenceSphere": common_types.Float,
    "fLifeChozoCommanderStage1": common_types.Float,
    "fLifeChozoCommanderStage2": common_types.Float,
    "fLifeChozoRobotSoldier": common_types.Float,
    "fLifeChozoRobotSoldierAlternative": common_types.Float,
    "fLifeChozoWarrior": common_types.Float,
    "fLifeChozoWarriorElite": common_types.Float,
    "fLifeChozoWarriorWeak": common_types.Float,
    "fLifeChozoWarriorX": common_types.Float,
    "fLifeChozoWarriorXElite": common_types.Float,
    "fLifeChozoWarriorXWeak": common_types.Float,
    "fLifeChozoZombieX": common_types.Float,
    "fLifeCooldownXBoss": common_types.Float,
    "fLifeCooldownXBossFireBall": common_types.Float,
    "fLifeCooldownXBossWeakPoint": common_types.Float,
    "fLifeCoreX": common_types.Float,
    "fLifeCoreXSuperQuetzoa": common_types.Float,
    "fLifeDaivo": common_types.Float,
    "fLifeDaivoSwarm": common_types.Float,
    "fLifeDepthorn": common_types.Float,
    "fLifeDizzean": common_types.Float,
    "fLifeDredhed": common_types.Float,
    "fLifeDropter": common_types.Float,
    "fLifeDummy": common_types.Float,
    "fLifeEmmy": common_types.Float,
    "fLifeFing": common_types.Float,
    "fLifeFulmite": common_types.Float,
    "fLifeFulmiteBellyMine": common_types.Float,
    "fLifeGobbler": common_types.Float,
    "fLifeGobblerChozoWarriorX": common_types.Float,
    "fLifeGobblerCooldownX": common_types.Float,
    "fLifeGobblerHydrogiga": common_types.Float,
    "fLifeGobblerKraid": common_types.Float,
    "fLifeGobblerScorpius": common_types.Float,
    "fLifeGobblerSuperGoliath": common_types.Float,
    "fLifeGobblerSuperQuetzoa": common_types.Float,
    "fLifeGoliath": common_types.Float,
    "fLifeGoliathX": common_types.Float,
    "fLifeGooplot": common_types.Float,
    "fLifeGooshocker": common_types.Float,
    "fLifeGroundShocker": common_types.Float,
    "fLifeHecathon": common_types.Float,
    "fLifeHydrogiga": common_types.Float,
    "fLifeHydrogigaBlockingTentacle": common_types.Float,
    "fLifeHydrogigaPolyps": common_types.Float,
    "fLifeIceflea": common_types.Float,
    "fLifeInfester": common_types.Float,
    "fLifeInfesterBall": common_types.Float,
    "fLifeKlaida": common_types.Float,
    "fLifeKraid": common_types.Float,
    "fLifeKraidAcidBlobs": common_types.Float,
    "fLifeKraidBouncingCreatures": common_types.Float,
    "fLifeKraidNail": common_types.Float,
    "fLifeKraidStage1": common_types.Float,
    "fLifeKreep": common_types.Float,
    "fLifeMagnetHusk": common_types.Float,
    "fLifeNailong": common_types.Float,
    "fLifeNailugger": common_types.Float,
    "fLifeObsydomithon": common_types.Float,
    "fLifeOmnithon": common_types.Float,
    "fLifePoisonFly": common_types.Float,
    "fLifeQuetshocker": common_types.Float,
    "fLifeQuetshockerEnergyWave": common_types.Float,
    "fLifeQuetzoa": common_types.Float,
    "fLifeQuetzoaX": common_types.Float,
    "fLifeRedenki": common_types.Float,
    "fLifeRinka": common_types.Float,
    "fLifeRinkaCaves": common_types.Float,
    "fLifeRinkaForest": common_types.Float,
    "fLifeRinkaLab": common_types.Float,
    "fLifeRinkaMagma": common_types.Float,
    "fLifeRinkaSanc": common_types.Float,
    "fLifeRockDiver": common_types.Float,
    "fLifeRodomithonX": common_types.Float,
    "fLifeRodotuk": common_types.Float,
    "fLifeSabotoru": common_types.Float,
    "fLifeSakai": common_types.Float,
    "fLifeSclawk": common_types.Float,
    "fLifeScorpius": common_types.Float,
    "fLifeScorpiusSpit": common_types.Float,
    "fLifeScorpiusStage1": common_types.Float,
    "fLifeScorpiusTail": common_types.Float,
    "fLifeScorpiusTailPhase3": common_types.Float,
    "fLifeScourge": common_types.Float,
    "fLifeShakernaut": common_types.Float,
    "fLifeSharpaw": common_types.Float,
    "fLifeShelmit": common_types.Float,
    "fLifeShelmitNaked": common_types.Float,
    "fLifeShineon": common_types.Float,
    "fLifeSlidle": common_types.Float,
    "fLifeSlugger": common_types.Float,
    "fLifeSluggerAcidBall": common_types.Float,
    "fLifeSpitclawk": common_types.Float,
    "fLifeSpittail": common_types.Float,
    "fLifeSunnap": common_types.Float,
    "fLifeSwarmer": common_types.Float,
    "fLifeSwifter": common_types.Float,
    "fLifeTakumaku": common_types.Float,
    "fLifeVulkran": common_types.Float,
    "fLifeWarLotus": common_types.Float,
    "fLifeXParasite": common_types.Float,
    "fLifeYampa": common_types.Float,
    "fLifeYamplotX": common_types.Float,
    "fLifeYojimbee": common_types.Float,
    "sName": common_types.StrId,
})

CCharClassLightingAttParamsEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttInnerOrLenght": common_types.Float,
    "fAttOuter": common_types.Float,
    "fTransitionTime": common_types.Float,
})

CCharClassLightingComponent = Object({
    **CCharClassComponentFields,
    "sLightsDefPath": common_types.StrId,
    "bOverrideDisableInEditor": construct.Flag,
})

CCharClassLightingSetCastShadowsEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "bCastShadows": construct.Flag,
})

CCharClassLightingSetColorEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "fR": common_types.Float,
    "fG": common_types.Float,
    "fB": common_types.Float,
    "fA": common_types.Float,
    "fInterpolationTime": common_types.Float,
})

CCharClassLightingSetEnableEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "bEnable": construct.Flag,
})

CCharClassLightingSetIntensityEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "fIntensity": common_types.Float,
    "fInterpolationTime": common_types.Float,
})

CCharClassLightingSetPosOffsetEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "vPosOffset": common_types.CVector3D,
    "fInterpolationTime": common_types.Float,
})

CCharClassLightingSetRotOffsetEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "vRotOffset": common_types.CVector3D,
    "fInterpolationTime": common_types.Float,
})

CCharClassLightingSetUseSpecularEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "bUseSpecular": construct.Flag,
})

CCharClassLinkToFloorTrack = Object({
    **base_global_timeline_CTrackFields,
    "fDistanceFromEdge": common_types.Float,
})

CCharClassLockAnalogInputAngTrack = Object(base_global_timeline_CTrackFields)

CCharClassMissileMovement = Object(CCharClassMissileMovementFields := {
    **CCharClassProjectileMovementFields,
    "fInitialSpeed": common_types.Float,
    "fTimeInInitialSpeed": common_types.Float,
    "fTimeToReachSpeed": common_types.Float,
})

CCharClassLockOnMissileMovement = Object(CCharClassLockOnMissileMovementFields := CCharClassMissileMovementFields)

CCharClassLogicLookAtPlayerComponent = Object({
    **CCharClassComponentFields,
    "sIdNodeName": common_types.StrId,
})

CCharClassLogicPathNavMeshItemComponent = Object(CCharClassNavMeshItemComponentFields)

CCharClassLogicSoundEvent = Object({
    **base_global_timeline_CEventFields,
    "sStimulusId": common_types.StrId,
    "sNode": common_types.StrId,
})

CCharClassSoundBaseEvent = Object(CCharClassSoundBaseEventFields := base_global_timeline_CEventFields)

CCharClassLoopSoundEvent = Object({
    **CCharClassSoundBaseEventFields,
    "sSoundID": common_types.StrId,
    "sNode": common_types.StrId,
    "fVolume": common_types.Float,
    "fRadiusMinAttenuation": common_types.Float,
    "fRadiusMaxAttenuation": common_types.Float,
    "fPitch": common_types.Float,
    "bStopOnChangeAnim": construct.Flag,
    "bStopOnEntityDead": construct.Flag,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "fStopInTime": common_types.Float,
    "sType": common_types.StrId,
    "bRumbleSync": construct.Flag,
    "fRumbleGainOverride": common_types.Float,
})

CCharClassLuaCallbackEvent = Object({
    **base_global_timeline_CEventFields,
    "sCallbackName": common_types.StrId,
})

CCharClassLuaCommandEvent = Object({
    **base_global_timeline_CEventFields,
    "sLUAFunction": common_types.StrId,
})

CCharClassMagnetCeiling45DownToRunTrack = Object(CCharClassToStateTrackFields)

CCharClassMagnetCeiling45UpToRunTrack = Object(CCharClassToStateTrackFields)

CCharClassMagnetHuskSetBreakableEvent = Object({
    **base_global_timeline_CEventFields,
    "bBreakable": construct.Flag,
    "sEntityName": PropertyEnum,
})

CCharClassMagnetSpiderPoseTrack = Object(base_global_timeline_CTrackFields)

CCharClassMagnetSurfaceHuskComponent = Object({
    **CCharClassComponentFields,
    "sHuskName": common_types.StrId,
    "sBrokenHuskName": common_types.StrId,
})

CCharClassMagnetSurfaceHuskComponent_CTunableCharClassMagnetSurfaceHuskComponent = Object({
    **base_tunable_CTunableFields,
    "fTimeToRespawn": common_types.Float,
    "fTimeToRespawnAfterMagnet": common_types.Float,
})

CCharClassMagnetSurfaceTransitionCompletedEvent = Object(base_global_timeline_CEventFields)

CCharClassMagnetSurfaceTransitionTrack = Object(base_global_timeline_CTrackFields)

CCharClassMaintainAnalogTrack = Object(base_global_timeline_CTrackFields)

CCharClassMaintainSPRTrack = Object(base_global_timeline_CTrackFields)

CCharClassMakingNoiseTrack = Object(base_global_timeline_CTrackFields)

CCharClassMapAcquisitionComponent = Object({
    **CCharClassUsableComponentFields,
    "sUsePrepareLeftMRNoUsedAction": common_types.StrId,
    "sUsePrepareRightMRNoUsedAction": common_types.StrId,
    "sUseInitMRUsedAction": common_types.StrId,
    "sUseMRUsedAction": common_types.StrId,
    "sUseAfterDownLoadMapAction": common_types.StrId,
    "sUseEndUseAfterDownLoadMapAction": common_types.StrId,
    "sUsableInitMRUsedAction": common_types.StrId,
    "sSaveRingsOpenAction": common_types.StrId,
    "sSaveRingsCloseAction": common_types.StrId,
    "sSaveRingLoopAction": common_types.StrId,
})

CCharClassMapRoomDownloadMapNotificationEvent = Object(base_global_timeline_CEventFields)

CCharClassMaterialFXComponent = Object(CCharClassComponentFields)

CCharClassMaterialPropertyTransitionTrack = Object({
    **base_global_timeline_CTrackFields,
    "fColorR1": common_types.Float,
    "fColorG1": common_types.Float,
    "fColorB1": common_types.Float,
    "fAlpha1": common_types.Float,
    "sName1": common_types.StrId,
    "sProperty1": common_types.StrId,
    "fColorR2": common_types.Float,
    "fColorG2": common_types.Float,
    "fColorB2": common_types.Float,
    "fAlpha2": common_types.Float,
    "sName2": common_types.StrId,
    "sProperty2": common_types.StrId,
    "fColorR3": common_types.Float,
    "fColorG3": common_types.Float,
    "fColorB3": common_types.Float,
    "fAlpha3": common_types.Float,
    "sName3": common_types.StrId,
    "sProperty3": common_types.StrId,
    "fIn": common_types.Float,
    "fOut": common_types.Float,
})

CCharClassMelee360ActionTrack = Object(base_global_timeline_CTrackFields)

CCharClassMeleeCameraAllowedTrack = Object(base_global_timeline_CTrackFields)

CCharClassMeleeComponent = Object({
    **CCharClassComponentFields,
    "bAutoLockOnMelee": construct.Flag,
    "sMeleeKillFX": common_types.StrId,
    "sMeleeKillSound": common_types.StrId,
})

CCharClassMeleeDamageProgressiveArcTrack = Object(base_global_timeline_CTrackFields)

CCharClassMeleeDamageTrack = Object({
    **base_global_timeline_CTrackFields,
    "bCheckCollider": construct.Flag,
})

CCharClassMeleeFailActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "iFrame": common_types.Int,
})

CCharClassMeleeHitReactionTrack = Object(base_global_timeline_CTrackFields)

CCharClassMeleeHitStopTrack = Object({
    **base_global_timeline_CTrackFields,
    "fTime": common_types.Float,
})

CCharClassMeleeSkippableTrack = Object(base_global_timeline_CTrackFields)

CCharClassMeleeSuccessActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "iFrame": common_types.Int,
})

CCharClassMeleeSuccessBigAIActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "iFrame": common_types.Int,
})

CCharClassMeleeTrack = Object(base_global_timeline_CTrackFields)

CCharClassMenuAnimationChangeComponent = Object(CCharClassComponentFields)

CCharClassMetroidCameraFollowMorphBallDCCamTrack = Object(base_global_timeline_CTrackFields)

CCharClassModelUpdaterComponent = Object(CCharClassModelUpdaterComponentFields := {
    **CCharClassComponentFields,
    "vInitPosWorldOffset": common_types.CVector3D,
    "vInitAngWorldOffset": common_types.CVector3D,
    "bOverrideDisableInEditor": construct.Flag,
    "vInitScale": common_types.CVector3D,
})

CCharClassModifyBumpedActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sOnSuccessFrontLeft": common_types.StrId,
    "sOnSuccessBackRight": common_types.StrId,
    "sOnSuccessUp": common_types.StrId,
    "sOnSuccessDown": common_types.StrId,
})

CCharClassModifyColliderStateBaseTrack = Object(CCharClassModifyColliderStateBaseTrackFields := {
    **base_global_timeline_CTrackFields,
    "sCollidersEnabled": common_types.StrId,
    "sLayersEnabled": common_types.StrId,
    "sCollidersDisabled": common_types.StrId,
    "sLayersDisabled": common_types.StrId,
    "sCollidersEnabled2": common_types.StrId,
    "sLayersEnabled2": common_types.StrId,
    "sCollidersDisabled2": common_types.StrId,
    "sLayersDisabled2": common_types.StrId,
    "sCollidersEnabled3": common_types.StrId,
    "sLayersEnabled3": common_types.StrId,
    "sCollidersDisabled3": common_types.StrId,
    "sLayersDisabled3": common_types.StrId,
})

CCharClassModifyColliderStateTrack = Object(CCharClassModifyColliderStateBaseTrackFields)

CCharClassModifyDamageTrack = Object({
    **base_global_timeline_CTrackFields,
    "sColliders": common_types.StrId,
    "sDamageID": common_types.StrId,
    "eDamageStrength": construct_EDamageStrength,
})

CCharClassModifyForceDamageTrack = Object({
    **base_global_timeline_CTrackFields,
    "eForcedDamageMode": construct_EForcedDamageMode,
})

CCharClassMorphBallLauncherComponent = Object({
    **CCharClassComponentFields,
    "fTimeShootSequence": common_types.Float,
    "fTimeRepositioningEntities": common_types.Float,
    "fTimeToAccelerateCannon": common_types.Float,
    "fMinCannonActionPlayRate": common_types.Float,
    "fMaxCannonActionPlayRate": common_types.Float,
    "sCannonActionPlayRateEasingFunction": common_types.StrId,
})

CCharClassMorphBallLauncherExitComponent = Object({
    **CCharClassComponentFields,
    "fExpelImpulseSize": common_types.Float,
    "fInputIgnoreTimeAfterExpelling": common_types.Float,
    "fFrictionIgnoreTimeAfterExpelling": common_types.Float,
})

CCharClassMorphBallLauncherMovementTrack = Object(base_global_timeline_CTrackFields)

CCharClassMorphBallLauncherTravellingAllowInputTrack = Object(base_global_timeline_CTrackFields)

CCharClassPlayerMovement = Object(CCharClassPlayerMovementFields := {
    **CCharClassCharacterMovementFields,
    "sFrozenStartTimeline": common_types.StrId,
    "sFrozenStopTimeline": common_types.StrId,
    "sFrozenGroundTimeline": common_types.StrId,
    "sFrozenImpactTimeline": common_types.StrId,
    "sFrozenRestoreTimeline": common_types.StrId,
})

CCharClassMorphBallMovement = Object({
    **CCharClassPlayerMovementFields,
    "fSlopeExitFrictionFactorTime": common_types.Float,
    "fSlopeExitFrictionFactor": common_types.Float,
    "sSlopeAccelerationFunction": common_types.StrId,
    "fSlopeTimeToAccelerate": common_types.Float,
    "fSlopeMinImpulse": common_types.Float,
    "fSlopeMaxImpulse": common_types.Float,
    "sMovementAudioPreset": common_types.StrId,
    "fInitialSpeedDiffDecrease": common_types.Float,
    "fMaxInitialSpeedDiff": common_types.Float,
    "fOnAirImpulseFactor": common_types.Float,
    "fXImpulseStrenght": common_types.Float,
})

CCharClassMovingBackwardsTrack = Object(base_global_timeline_CTrackFields)

base_global_CRntSmallDictionary_base_global_CStrId__base_global_CFilePathStrId_ = common_types.make_dict(common_types.StrId, key=common_types.StrId)

CCharClassMultiModelUpdaterComponent = Object({
    **CCharClassModelUpdaterComponentFields,
    "dctModels": base_global_CRntSmallDictionary_base_global_CStrId__base_global_CFilePathStrId_,
})

CCharClassMushroomPlatformComponent = Object({
    **CCharClassLifeComponentFields,
    "fTimeToRetract": common_types.Float,
    "fRetractedTime": common_types.Float,
})

CCharClassMuteMusicTrackEvent = Object({
    **base_global_timeline_CEventFields,
    "uTrack": common_types.UInt,
    "fFadeTime": common_types.Float,
    "bMute": construct.Flag,
})


class CCharClassNailongThornsAttack_EDepthornAttackType(enum.IntEnum):
    ClassicShoot = 0
    SequenceShoot = 1
    SineWaveShoot = 2
    Invalid = 2147483647


construct_CCharClassNailongThornsAttack_EDepthornAttackType = StrictEnum(CCharClassNailongThornsAttack_EDepthornAttackType)

CCharClassNailongThornsAttack = Object({
    **CCharClassAttackFields,
    "bAttackInIntervals": construct.Flag,
    "fIntervalMin": common_types.Float,
    "fIntervalMax": common_types.Float,
    "fRepeatAttackTimer": common_types.Float,
    "fTimeToChargeAttack": common_types.Float,
    "sProjectile": common_types.StrId,
    "fBallGravity": common_types.Float,
    "fBallInitialSpeed": common_types.Float,
    "eDepthornAttackType": construct_CCharClassNailongThornsAttack_EDepthornAttackType,
    "fTimeBetweenThornsMin": common_types.Float,
    "fTimeBetweenThornsMax": common_types.Float,
    "bUseSineWavesInSequenceShoot": construct.Flag,
    "uNumSequences": common_types.UInt,
})

CCharClassNailuggerAcidBallsAttack = Object({
    **CCharClassAttackFields,
    "fIntervalMin": common_types.Float,
    "fIntervalMax": common_types.Float,
    "fRepeatAttackTimer": common_types.Float,
    "fTimeToChargeAttack": common_types.Float,
})

std_unique_ptr_CShootDCBones_ = Pointer_CShootDCBones.create_construct()

base_global_CRntVector_std_unique_ptr_CShootDCBones__ = common_types.make_vector(std_unique_ptr_CShootDCBones_)

std_unique_ptr_CPattern_ = Pointer_CPattern.create_construct()

base_global_CRntVector_std_unique_ptr_CPattern__ = common_types.make_vector(std_unique_ptr_CPattern_)

CCharClassNailongAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oNailongThornsAttackDef": CCharClassNailongThornsAttack,
    "oNailuggerAcidBallsAttackDef": CCharClassNailuggerAcidBallsAttack,
    "fTimeBetweenThornsAttack": common_types.Float,
    "fSteeringTargetReachDistance": common_types.Float,
    "fSteeringCloseToTargetAccel": common_types.Float,
    "fSteeringMaxDistToTurn": common_types.Float,
    "fSteeringLookAheadDistance": common_types.Float,
    "fSteeringAcceleration": common_types.Float,
    "fMaxTargetDistanceToAccelerateCloseToTarget": common_types.Float,
    "fSlowSteeringTargetReachDistance": common_types.Float,
    "fSlowSteeringCloseToTargetAccel": common_types.Float,
    "fSlowSteeringMaxDistToTurn": common_types.Float,
    "fSlowSteeringLookAheadDistance": common_types.Float,
    "fSlowSteeringAcceleration": common_types.Float,
    "fSlowMaxTargetDistanceToAccelerateCloseToTarget": common_types.Float,
    "fSlowMotionSpeed": common_types.Float,
    "tShootDCBones": base_global_CRntVector_std_unique_ptr_CShootDCBones__,
    "tLaunchConfig": base_global_CRntVector_std_unique_ptr_CPattern__,
})

CCharClassNailongChangeDirEvent = Object(base_global_timeline_CEventFields)

CCharClassNailongThornMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fAmplitude": common_types.Float,
    "fFrequency": common_types.Float,
})

CCharClassNailuggerAcidBallMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassNeedSmallestHittableTrack = Object(base_global_timeline_CTrackFields)

CCharClassNoApplyPushActionTrack = Object(base_global_timeline_CTrackFields)

CCharClassNonSnappedRotationIsValidTrack = Object(base_global_timeline_CTrackFields)

CCharClassObsydomithonAttack = Object({
    **CCharClassAttackFields,
    "fBlockableAttackTime": common_types.Float,
    "fBlockableAttackWarningTime": common_types.Float,
})

CCharClassObsydomithonAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oObsydomithonAttackDef": CCharClassObsydomithonAttack,
})

CCharClassObsydomithonAIComponent_CTunableCharClassObsydomithonAIComponent = Object({
    **base_tunable_CTunableFields,
    "fHeadAngleInterpolationSpeed": common_types.Float,
})

CCharClassObsydomithonAttack_CTunableCharClassObsydomithonAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fChargeLoopDuration": common_types.Float,
    "fAttackLoopDuration": common_types.Float,
    "fVerticalAttackAngleToleranceForOtherPlatform": common_types.Float,
})

CCharClassObsydomithonBlockAimTrack = Object(base_global_timeline_CTrackFields)

CCharClassObsydomithonChargePoseTrack = Object(base_global_timeline_CTrackFields)

CCharClassObsydomithonIdleTrack = Object(base_global_timeline_CTrackFields)

CCharClassOverrideAnalogAimInvalidAnglesTrack = Object({
    **base_global_timeline_CTrackFields,
    "fMinInvaligAngle": common_types.Float,
    "fMaxInvaligAngle": common_types.Float,
})

CCharClassOverrideAngularSpeedTrack = Object({
    **base_global_timeline_CTrackFields,
    "fNewAngSpeed": common_types.Float,
})

CCharClassOverrideBlendValueTrack = Object({
    **base_global_timeline_CTrackFields,
    "fDesiredBlendValue": common_types.Float,
})

CCharClassOverrideMeleeCameraFXPresetTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCameraFXPreset": common_types.StrId,
})

CCharClassOverrideMeleeTrailFXTrack = Object({
    **base_global_timeline_CTrackFields,
    "sDefault": common_types.StrId,
})

CCharClassOverrideMovementTransitionTrack = Object(CCharClassToStateTrackFields)

CCharClassOverrideSamusMeleeActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sMeleeAction": common_types.StrId,
    "bMaintainFrame": construct.Flag,
    "iFrame": common_types.Int,
})

CCharClassOverrideSpeedHyperDashTrack = Object({
    **base_global_timeline_CTrackFields,
    "fSpeed": common_types.Float,
})

CCharClassParkourTrack = Object(base_global_timeline_CTrackFields)

CCharClassPatrolTrack = Object(base_global_timeline_CTrackFields)

CCharClassPerceptionComponent = Object(CCharClassComponentFields)

CGameBBPropID = Object({})

CCharClassPersistenceComponent = Object({
    **CCharClassComponentFields,
    "sBoolProperty": CGameBBPropID,
    "sIntProperty": CGameBBPropID,
    "sFloatProperty": CGameBBPropID,
    "sSection": common_types.StrId,
})

CCharClassPickAllItemsEvent = Object({
    **base_global_timeline_CEventFields,
    "bPlaySound": construct.Flag,
})

CCharClassPickableComponent = Object({
    **CCharClassComponentFields,
    "sOnPickFX": common_types.StrId,
    "sOnPickCaption": common_types.StrId,
    "sOnPickEnergyFragment1Caption": common_types.StrId,
    "sOnPickEnergyFragment2Caption": common_types.StrId,
    "sOnPickEnergyFragment3Caption": common_types.StrId,
    "sOnPickEnergyFragmentCompleteCaption": common_types.StrId,
    "sOnPickTankUnknownCaption": common_types.StrId,
})

CCharClassPlatformTrapGrapplePointComponent = Object({
    **CCharClassPullableGrapplePointComponentFields,
    "sGrappleCollider": common_types.StrId,
})

ICharClassPlayAudioPresetEvent = Object(ICharClassPlayAudioPresetEventFields := {
    **base_global_timeline_CEventFields,
    "sPresetUniqueID": common_types.StrId,
    "fVolume": common_types.Float,
    "fPitch": common_types.Float,
    "bApplyModifier": construct.Flag,
})

CCharClassPlayAudioPresetEvent = Object(ICharClassPlayAudioPresetEventFields)

CCharClassPlayAudioPresetWithMaterialEvent = Object(ICharClassPlayAudioPresetEventFields)

CCharClassPlayCaptionVoiceEvent = Object({
    **base_global_timeline_CEventFields,
    "sCaptionID": common_types.StrId,
    "fVolume": common_types.Float,
    "bSubtitledInOccident": construct.Flag,
    "bSubltiledInOrient": construct.Flag,
    "bSoundLocalized": construct.Flag,
})

CCharClassPlayCurrentEnvironmentMusicEvent = Object(base_global_timeline_CEventFields)

CCharClassPlayCurrentEnvironmentSoundEvent = Object(base_global_timeline_CEventFields)

CCharClassPlayEntityTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntityId": common_types.StrId,
    "sTimelineId": common_types.StrId,
})

CCharClassPlayEnvironmentStreamEvent = Object({
    **base_global_timeline_CEventFields,
    "fVolume": common_types.Float,
    "sPath": common_types.StrId,
    "bLoop": construct.Flag,
    "fFadeInTime": common_types.Float,
})


class SMusicPriority(enum.IntEnum):
    NONE = 0
    LOWEST = 1
    ENVIRONMENT = 2
    TRIGGER = 3
    NORMAL = 4
    EVENT = 5
    STATE = 6
    SCRIPT = 7
    LOADING = 8
    Invalid = 2147483647


construct_SMusicPriority = StrictEnum(SMusicPriority)

CCharClassPlayMusicEvent = Object({
    **base_global_timeline_CEventFields,
    "sPath": common_types.StrId,
    "ePriority": construct_SMusicPriority,
    "fVolume": common_types.Float,
    "bLoop": construct.Flag,
    "fFadeInTime": common_types.Float,
})


class CLiquidPoolBaseComponent_ELiquidType(enum.IntEnum):
    NONE = 0
    Water = 1
    Lava = 2
    All = 3
    Invalid = 2147483647


construct_CLiquidPoolBaseComponent_ELiquidType = StrictEnum(CLiquidPoolBaseComponent_ELiquidType)

CCharClassPlayPlayerTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "ePlayOnly": construct_CLiquidPoolBaseComponent_ELiquidType,
})

CCharClassPlayRandomTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "uTimelineCount": common_types.UInt,
    "fMinDelay": common_types.Float,
    "fMaxDelay": common_types.Float,
    "ePlayOnly": construct_CLiquidPoolBaseComponent_ELiquidType,
    "sName0": common_types.StrId,
    "sName1": common_types.StrId,
    "sName2": common_types.StrId,
    "sName3": common_types.StrId,
    "sName4": common_types.StrId,
    "sName5": common_types.StrId,
    "sName6": common_types.StrId,
    "sName7": common_types.StrId,
})

CCharClassPlayTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
    "ePlayOnly": construct_CLiquidPoolBaseComponent_ELiquidType,
})

CCharClassPlayTimelineEventByPlayerSuit = Object({
    **base_global_timeline_CEventFields,
    "sNamePower": common_types.StrId,
    "sNameVaria": common_types.StrId,
    "sNameGravity": common_types.StrId,
    "sNameHyper": common_types.StrId,
    "ePlayOnly": construct_CLiquidPoolBaseComponent_ELiquidType,
})

CCharClassPlayTimelineTrack = Object({
    **base_global_timeline_CTrackFields,
    "sOnStartTimeline": common_types.StrId,
    "sLoopTimeline": common_types.StrId,
    "sOnEndTimeline": common_types.StrId,
    "ePlayOnly": construct_CLiquidPoolBaseComponent_ELiquidType,
})


class base_input_ERumbleType(enum.IntEnum):
    RFX = 0
    RGUI = 1
    RGRUNT = 2
    RFX_EMMY = 3
    RMUSIC = 4
    Invalid = 2147483647


construct_base_input_ERumbleType = StrictEnum(base_input_ERumbleType)

CCharClassPlayVibrationEvent = Object({
    **base_global_timeline_CEventFields,
    "sPath": common_types.StrId,
    "sNode": common_types.StrId,
    "eType": construct_base_input_ERumbleType,
    "fAttMaxRange": common_types.Float,
    "fAttMinRange": common_types.Float,
    "fGain": common_types.Float,
    "fPitch": common_types.Float,
    "fPan": common_types.Float,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "fSpeed": common_types.Float,
    "b3D": construct.Flag,
    "bLoop": construct.Flag,
    "bStopOnEntityDead": construct.Flag,
    "bStopOnChangeAnim": construct.Flag,
})

CCharClassPlayerLifeComponent = Object({
    **CCharClassLifeComponentFields,
    "fImpactInvulnerableTime": common_types.Float,
    "fMinImpactInvulnerableTime": common_types.Float,
})


class CCharClassPoisonFlyAIComponent_ESubspecies(enum.IntEnum):
    Poisonfly = 0
    Blindfly = 1
    Invalid = 2147483647


construct_CCharClassPoisonFlyAIComponent_ESubspecies = StrictEnum(CCharClassPoisonFlyAIComponent_ESubspecies)

CCharClassPoisonFlyDiveAttack = Object({
    **CCharClassAttackFields,
    "fAttackDiveDistance": common_types.Float,
    "fAttackPreparationTime": common_types.Float,
})

CCharClassPoisonFlyAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "eSubspecies": construct_CCharClassPoisonFlyAIComponent_ESubspecies,
    "oPoisonFlyDiveAttackDef": CCharClassPoisonFlyDiveAttack,
})

CCharClassPoisonFlyAIComponent_CTunableCharClassPoisonFlyAIComponent = Object({
    **base_tunable_CTunableFields,
    "fHorizontalMoveDist": common_types.Float,
    "fVerticalMaxNoise": common_types.Float,
    "fNoNoiseRadiusFromTarget": common_types.Float,
    "fCombatSpeedMultiplier": common_types.Float,
    "fPatrolSpeedMultiplier": common_types.Float,
    "fAttackAnticipationSpeedMultiplier": common_types.Float,
    "fFrontMinDistToTarget": common_types.Float,
    "fBackMinDistToTarget": common_types.Float,
    "fOnHitRepositionDistance": common_types.Float,
    "fMinOnHitRepositionAngle": common_types.Float,
    "fTimeBetweenAttacks": common_types.Float,
    "fYOffsetToCrossTarget": common_types.Float,
    "fWaitTimeToReturnPatrol": common_types.Float,
    "fMotionSpeed": common_types.Float,
    "fMinAnticipationRelocationDistance": common_types.Float,
})

CCharClassPoisonFlyDiveAttack_CTunableCharClassPoisonFlyDiveAttack = Object({
    **base_tunable_CTunableFields,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassPopSetupEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
    "bPersistent": construct.Flag,
    "bForceUpdate": construct.Flag,
})

CCharClassPositionalSoundComponent = Object({
    **CCharClassComponentFields,
    "bOverrideDisableInEditor": construct.Flag,
})

CCharClassPreImpactEvent = Object(base_global_timeline_CEventFields)

CCharClassProcessAttackTrack = Object(base_global_timeline_CTrackFields)

CCharClassProcessCrouchRepositionTrack = Object(base_global_timeline_CTrackFields)

CCharClassProcessStandRepositionTrack = Object(base_global_timeline_CTrackFields)

CCharClassProjectDisplacementOnFloorTrack = Object({
    **base_global_timeline_CTrackFields,
    "bX": construct.Flag,
    "bY": construct.Flag,
})

CCharClassProtoEmmyChaseMusicTriggerComponent = Object(CCharClassBaseTriggerComponentFields)

CCharClassPushCanChangePrefixTrack = Object(base_global_timeline_CTrackFields)

CCharClassPushSetupEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
    "bPersistent": construct.Flag,
    "bForceUpdate": construct.Flag,
})

CCharClassPushTrack = Object(base_global_timeline_CTrackFields)

CCharClassQuetzoaChargeAttack = Object(CCharClassAttackFields)

CCharClassQuetzoaEnergyWaveAttack = Object(CCharClassAttackFields)


class CCharClassQuetzoaAIComponent_ESubspecies(enum.IntEnum):
    Quetzoa = 0
    Quetshocker = 1
    Invalid = 2147483647


construct_CCharClassQuetzoaAIComponent_ESubspecies = StrictEnum(CCharClassQuetzoaAIComponent_ESubspecies)

CCharClassQuetzoaAIComponent = Object(CCharClassQuetzoaAIComponentFields := {
    **CCharClassBossAIComponentFields,
    "oQuetzoaChargeAttackDef": CCharClassQuetzoaChargeAttack,
    "oQuetzoaEnergyWaveAttackDef": CCharClassQuetzoaEnergyWaveAttack,
    "eSubspecies": construct_CCharClassQuetzoaAIComponent_ESubspecies,
})

CCharClassQuetzoaAIComponent_CTunableCharClassQuetzoaAIComponent = Object({
    **base_tunable_CTunableFields,
    "fDodgeTimeThreshold": common_types.Float,
})

CCharClassQuetzoaChargeAttack_CTunableCharClassQuetzoaChargeAttack = Object({
    **base_tunable_CTunableFields,
    "fMaxChargingDistance": common_types.Float,
})

CCharClassQuetzoaEnergyWaveAttack_CTunableCharClassQuetzoaEnergyWaveAttack = Object({
    **base_tunable_CTunableFields,
    "fMaxProjectileDistance": common_types.Float,
    "fTimeBeforeElectrify": common_types.Float,
    "fElectrifyTime": common_types.Float,
})

CCharClassQuetzoaEnergyWaveMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassQuetzoaMultiTargetProjectileMovementComponent = Object({
    **CCharClassLockOnMissileMovementFields,
    "fLaunchAngle": common_types.Float,
    "fLaunchDist": common_types.Float,
    "fSteeringSpeed": common_types.Float,
    "fMaxDistanceFromGuide": common_types.Float,
})

CCharClassQuetzoaXMultiTargetAttack = Object({
    **CCharClassAttackFields,
    "uNumProjectiles": common_types.UInt,
    "fTimeBetweenShots": common_types.Float,
})

CCharClassQuetzoaXAIComponent = Object({
    **CCharClassQuetzoaAIComponentFields,
    "oQuetzoaXMultiTargetAttackDef": CCharClassQuetzoaXMultiTargetAttack,
    "fVulnerabilityTime": common_types.Float,
})

CCharClassReadySmartObjectEvent = Object(base_global_timeline_CEventFields)

CCharClassRecalculatePathEvent = Object(base_global_timeline_CEventFields)

CCharClassRecalculateTweakAttackPlayRatePresetEvent = Object(base_global_timeline_CEventFields)

CCharClassRecoilTrack = Object(base_global_timeline_CTrackFields)

CCharClassReferenceBoneToCreateBoundingBoxTrack = Object({
    **base_global_timeline_CTrackFields,
    "sBone": PropertyEnum,
})

CCharClassRelaxShotEndActionTrack = Object(CCharClassToStateTrackFields)

CCharClassRemoveBossMusicPresetEvent = Object(base_global_timeline_CEventFields)

CCharClassRepelWallCollisionEvent = Object(base_global_timeline_CEventFields)

CCharClassRestoreCameraFarEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
})

CCharClassRestoreCameraNearEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
})

CCharClassRestoreFanMudEvent = Object(base_global_timeline_CEventFields)

CCharClassRevertMeleeDamageTrack = Object(base_global_timeline_CTrackFields)

CCharClassRinkaAIComponent = Object(CCharClassAIComponentFields)

CCharClassRinkaAIComponent_CTunableCharClassRinkaAIComponent = Object({
    **base_tunable_CTunableFields,
    "fInitialScale": common_types.Float,
    "fTimeToMaxScale": common_types.Float,
    "fATypeMotionSpeed": common_types.Float,
    "fBTypeMotionSpeed": common_types.Float,
    "fCTypeMotionSpeed": common_types.Float,
})

CCharClassRinkaUnitComponent = Object(CCharClassComponentFields)

CCharClassRinkaUnitComponent_CTunableCharClassRinkaUnitComponent = Object({
    **base_tunable_CTunableFields,
    "fPreparationTime": common_types.Float,
    "fSpawnTime": common_types.Float,
})

CCharClassRockDiverAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fCloseWingsStartDistance": common_types.Float,
})

CCharClassRockDiverAIComponent_CTunableCharClassRockDiverAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMotionSpeed": common_types.Float,
})


class CCharClassRodotukAIComponent_SAbsorbConfig_EType(enum.IntEnum):
    NONE = 0
    Short = 1
    Medium = 2
    Long = 3
    Invalid = 2147483647


construct_CCharClassRodotukAIComponent_SAbsorbConfig_EType = StrictEnum(CCharClassRodotukAIComponent_SAbsorbConfig_EType)

CCharClassRodotukAIComponent_SAbsorbConfig = Object({
    "eType": construct_CCharClassRodotukAIComponent_SAbsorbConfig_EType,
    "fBaseAbsorbDistance": common_types.Float,
    "fAngryAbsorbDistance": common_types.Float,
    "fBombAbsorbExtraHeight": common_types.Float,
    "fBombAbsorbExtraWidth": common_types.Float,
    "fMaxAbsorbAngle": common_types.Float,
    "fAbsorbBaseSpeed": common_types.Float,
    "fAbsorbMaxSpeed": common_types.Float,
    "fAbsorbTimeToLoseControl": common_types.Float,
    "fAbsorbAcceleration": common_types.Float,
    "fBombAbsorbBaseSpeed": common_types.Float,
    "fBombAbsorbAcceleration": common_types.Float,
})

base_global_CRntVector_CCharClassRodotukAIComponent_SAbsorbConfig_ = common_types.make_vector(CCharClassRodotukAIComponent_SAbsorbConfig)

CCharClassRodotukAIComponent_TVAbsorbConfigs = base_global_CRntVector_CCharClassRodotukAIComponent_SAbsorbConfig_

CCharClassRodotukSuckAttack = Object(CCharClassRodotukSuckAttackFields := CCharClassAttackFields)

CCharClassRodotukAIComponent = Object(CCharClassRodotukAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "fBiteAnticipationDistance": common_types.Float,
    "fBombForceExplosionDistance": common_types.Float,
    "vAbsorbConfigs": CCharClassRodotukAIComponent_TVAbsorbConfigs,
    "oRodotukSuckAttackDef": CCharClassRodotukSuckAttack,
})


class CCharClassRodomithonXAIComponent_SFirePillarConfig_EType(enum.IntEnum):
    NONE = 0
    Short = 1
    Medium = 2
    Long = 3
    Invalid = 2147483647


construct_CCharClassRodomithonXAIComponent_SFirePillarConfig_EType = StrictEnum(CCharClassRodomithonXAIComponent_SFirePillarConfig_EType)

CCharClassRodomithonXAIComponent_SFirePillarConfig = Object({
    "eType": construct_CCharClassRodomithonXAIComponent_SFirePillarConfig_EType,
    "fFirePillarLength": common_types.Float,
    "fFirePillarWidth": common_types.Float,
    "fFirePillarLengthOffset": common_types.Float,
})

base_global_CRntVector_CCharClassRodomithonXAIComponent_SFirePillarConfig_ = common_types.make_vector(CCharClassRodomithonXAIComponent_SFirePillarConfig)

CCharClassRodomithonXAIComponent_TVFirePillarConfigs = base_global_CRntVector_CCharClassRodomithonXAIComponent_SFirePillarConfig_

CCharClassRodomithonXSuckAttack = Object(CCharClassRodotukSuckAttackFields)

CCharClassRodomithonXAIComponent = Object({
    **CCharClassRodotukAIComponentFields,
    "fFireActiveTime": common_types.Float,
    "fRestTime": common_types.Float,
    "vFirePillarConfigs": CCharClassRodomithonXAIComponent_TVFirePillarConfigs,
    "oRodomithonXSuckAttackDef": CCharClassRodomithonXSuckAttack,
})

CCharClassRodotukAIComponent_CTunableCharClassRodotukAIComponent = Object({
    **base_tunable_CTunableFields,
    "fBaseAbsorbDistance": common_types.Float,
    "fAngryAbsorbDistance": common_types.Float,
    "fMaxAbsorbAngle": common_types.Float,
    "fAbsorbBaseSpeed": common_types.Float,
    "fAbsorbMaxSpeed": common_types.Float,
    "fAbsorbTimeToLoseControl": common_types.Float,
    "fAbsorbAcceleration": common_types.Float,
    "fBombAbsorbBaseSpeed": common_types.Float,
    "fBombAbsorbAcceleration": common_types.Float,
    "fBiteAnticipationDistance": common_types.Float,
})

CCharClassRodotukSuckAttack_CTunableCharClassRodotukSuckAttack = Object(base_tunable_CTunableFields)

CCharClassRotateToInstigatorHitColliderTrack = Object(base_global_timeline_CTrackFields)

CCharClassRotateToViewDirEvent = Object({
    **base_global_timeline_CEventFields,
    "bRaw": construct.Flag,
})

CCharClassRumbleComponent = Object(CCharClassComponentFields)

CCharClassRunNearWallTrack = Object(base_global_timeline_CTrackFields)

CCharClassRunTrack = Object(base_global_timeline_CTrackFields)

CCharClassSPAnalogAimKinematicDeltaTrack = Object(base_global_timeline_CTrackFields)


class CCharClassSabotoruAIComponent_ESubspecies(enum.IntEnum):
    Sabotoru = 0
    Kreep = 1
    Invalid = 2147483647


construct_CCharClassSabotoruAIComponent_ESubspecies = StrictEnum(CCharClassSabotoruAIComponent_ESubspecies)

CCharClassSabotoruTurnInDoorAttack = Object(CCharClassAttackFields)

CCharClassSabotoruAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "eSubspecies": construct_CCharClassSabotoruAIComponent_ESubspecies,
    "oSabotoruTurnInDoorAttackDef": CCharClassSabotoruTurnInDoorAttack,
    "fDoorPlayRate": common_types.Float,
})

CCharClassSabotoruAIComponent_CTunableCharClassSabotoruAIComponent = Object({
    **base_tunable_CTunableFields,
    "fDoorLife": common_types.Float,
    "fTimeToStopPanic": common_types.Float,
})

CCharClassSabotoruLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassSamusActivateLegsNodesOverrideTrack = Object(base_global_timeline_CTrackFields)

CCharClassSamusDeactivateLegsNodesOverrideTrack = Object(base_global_timeline_CTrackFields)

CCharClassSamusLegsNodesOverrideWithBlendspaceTrack = Object(base_global_timeline_CTrackFields)

CCharClassSamusMovement = Object({
    **CCharClassPlayerMovementFields,
    "fMinTimeToSpaceJump": common_types.Float,
    "fMinTimeToDoubleJump": common_types.Float,
    "sFallOilFX": common_types.StrId,
    "fRunningImpulseX": common_types.Float,
    "fImpulseY": common_types.Float,
    "fHighJumpBootImpulseY": common_types.Float,
    "fMinImpulseY": common_types.Float,
    "fMaxImpulseY": common_types.Float,
    "fChangeDirectionOnAirBrakeFactor": common_types.Float,
    "fTimeOnAirAllowingJump": common_types.Float,
    "fNoJumpingDefaultGravityFactor": common_types.Float,
    "fTimeToAimUpAfterRaise": common_types.Float,
    "fTimeToHangClimb": common_types.Float,
    "fRunningFallInitImpulse": common_types.Float,
    "fWalkingFallInitImpulse": common_types.Float,
    "fTimeToAbortSpinJump": common_types.Float,
    "fSpinJumpVelocityX": common_types.Float,
    "fAirRunningVelocityX": common_types.Float,
    "fAirWalkingVelocityX": common_types.Float,
})

CCharClassSaveStationUsableComponent = Object({
    **CCharClassUsableComponentFields,
    "sSaveFXID": common_types.StrId,
    "sStartLevelFXID": common_types.StrId,
})

CCharClassScaredTrack = Object(base_global_timeline_CTrackFields)

CCharClassSceneModelAnimationComponent = Object(CCharClassComponentFields)

CCharClassScheduleFireTrack = Object(base_global_timeline_CTrackFields)

CCharClassScheduleStealthActionTrack = Object(base_global_timeline_CTrackFields)

CCharClassSclawkAIComponent = Object(CCharClassSclawkAIComponentFields := {
    **CCharClassBehaviorTreeAIComponentFields,
    "fMinHiddenTime": common_types.Float,
    "fMaxHiddenTime": common_types.Float,
    "fJumpPreparationTime": common_types.Float,
    "fJumpShortPreparationTime": common_types.Float,
})

CCharClassSclawkAIComponent_CTunableCharClassSclawkAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMinHiddenTime": common_types.Float,
    "fMaxHiddenTime": common_types.Float,
    "fJumpPreparationTime": common_types.Float,
})

CCharClassSclawkLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassScorpiusAttack = Object(CCharClassScorpiusAttackFields := {
    **CCharClassAttackFields,
    "bAnimateTail": construct.Flag,
    "fTailBlendTime": common_types.Float,
})

CCharClassScorpiusWhiplashAttack = Object(CCharClassScorpiusAttackFields)

CCharClassScorpiusSpikeBallPrickAttack = Object({
    **CCharClassScorpiusAttackFields,
    "sMagnetAttackAnim": common_types.StrId,
})

CCharClassScorpiusPoisonousSpitAttack = Object(CCharClassScorpiusAttackFields)

CCharClassScorpiusDefensiveSpikeBallPrickAttack = Object(CCharClassScorpiusAttackFields)

CCharClassScorpiusTailSmashAttack = Object(CCharClassScorpiusAttackFields)

CCharClassScorpiusPoisonousGasAttack = Object(CCharClassScorpiusPoisonousGasAttackFields := {
    **CCharClassScorpiusAttackFields,
    "sChargeAttackAnim": common_types.StrId,
    "sAfterChargeAttackAnim": common_types.StrId,
})

CCharClassScorpiusMovingPoisonousGasAttack = Object(CCharClassScorpiusPoisonousGasAttackFields)

CCharClassScorpiusDraggedBallPrickAttack = Object(CCharClassScorpiusAttackFields)

CCharClassScorpiusAIComponent = Object({
    **CCharClassBossAIComponentFields,
    "oWhiplashAttackDef": CCharClassScorpiusWhiplashAttack,
    "oSpikeBallPrickAttackDef": CCharClassScorpiusSpikeBallPrickAttack,
    "oPoisonousSpitAttackDef": CCharClassScorpiusPoisonousSpitAttack,
    "oDefensiveSpikeBallPrickAttackDef": CCharClassScorpiusDefensiveSpikeBallPrickAttack,
    "oTailSmashAttackDef": CCharClassScorpiusTailSmashAttack,
    "oPoisonousGasAttackDef": CCharClassScorpiusPoisonousGasAttack,
    "oMovingPoisonousGasAttackDef": CCharClassScorpiusMovingPoisonousGasAttack,
    "oDraggedBallPrickAttackDef": CCharClassScorpiusDraggedBallPrickAttack,
    "sHeadMovementFunction": common_types.StrId,
    "sTailMovementFunction": common_types.StrId,
    "fTailMinTimeToChange": common_types.Float,
    "fTailMaxTimeToChange": common_types.Float,
    "fRegenTailMaxAnimSpeed": common_types.Float,
    "sRegenTailAnimSpeedFunc": common_types.StrId,
    "fTimeRegenTailSlowMovement": common_types.Float,
    "fTimeRegenTailFastMovement": common_types.Float,
    "fTimeRegenTailMovementTransitionFactor": common_types.Float,
    "fTailHeightInterpolationSpeed": common_types.Float,
    "oGrabDamageSourceFactor": CDamageSourceFactor,
    "fHeadMaxSpeed": common_types.Float,
    "fHeadMinSpeed": common_types.Float,
})


class EForceOpticCamouflageMode(enum.IntEnum):
    Default = 0
    ForceEnabled = 1
    ForceDisabled = 2
    Invalid = 2147483647


construct_EForceOpticCamouflageMode = StrictEnum(EForceOpticCamouflageMode)

CCharClassScorpiusAIComponent_CTunableCharClassScorpiusAIComponent = Object({
    **base_tunable_CTunableFields,
    "eForceOpticCamouflageDisabledMode": construct_EForceOpticCamouflageMode,
    "iInitialStage": common_types.Int,
    "fMaskLife": common_types.Float,
    "fHeadPosInterpolationSpeed": common_types.Float,
    "fHeadPosChangeMinTime": common_types.Float,
    "fHeadPosChangeMaxTime": common_types.Float,
    "fStartRegenerationWallDistance": common_types.Float,
    "fRegenerationTime": common_types.Float,
    "iForceOpticCamouflageDisabledMode": common_types.Int,
    "fDamageToChangeHeadPos": common_types.Float,
    "fChaseMinDistance": common_types.Float,
    "fChaseMaxDistance": common_types.Float,
    "fFrontMaxDistance": common_types.Float,
    "fBackMaxDistance": common_types.Float,
    "fDamageMultiplayerInPhase2": common_types.Float,
    "fTailDamageToActivateCamouflage": common_types.Float,
})

CCharClassScorpiusAllowAttackSuccessTrack = Object(base_global_timeline_CTrackFields)

CCharClassScorpiusAllowDefensiveAttacksTrack = Object(base_global_timeline_CTrackFields)

CCharClassScorpiusAvoidMediumHeadPositionTrack = Object(base_global_timeline_CTrackFields)

CCharClassScorpiusDefensiveSpikeBallPrickAttack_CTunableCharClassScorpiusDefensiveSpikeBallPrickAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassScorpiusDraggedBallPrickAttack_CTunableCharClassScorpiusDraggedBallPrickAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassScorpiusFXComponent = Object(CCharClassComponentFields)

CCharClassScorpiusMovingPoisonousGasAttack_CTunableCharClassScorpiusMovingPoisonousGasAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fTimeToMove": common_types.Float,
    "fDistanceToStopMoving": common_types.Float,
    "fTimeToSmash": common_types.Float,
})

CCharClassScorpiusPoisonousGasAttack_CTunableCharClassScorpiusPoisonousGasAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fAttackTime": common_types.Float,
    "fShockWaveLength": common_types.Float,
    "fShockWaveTimeGrowing": common_types.Float,
    "fShockWaveTimeAtMaxRadius": common_types.Float,
    "fMinChargingTime": common_types.Float,
})

CCharClassScorpiusPoisonousSpitAttack_CTunableCharClassScorpiusPoisonousSpitAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fExplosionRadius": common_types.Float,
    "fTimeToReachExplosionRadius": common_types.Float,
    "fTimeToMaintainExplosionRadius": common_types.Float,
    "fTimeToDisapear": common_types.Float,
    "fPoisonDamagePerSecond": common_types.Float,
    "fPoisonDamage": common_types.Float,
})

CCharClassScorpiusPoisonousSpitMovementComponent = Object(CCharClassProjectileMovementFields)

CCharClassScorpiusRegeneratingMaskTrack = Object(base_global_timeline_CTrackFields)

CCharClassScorpiusSetTailDefaultMovementEvent = Object({
    **base_global_timeline_CEventFields,
    "fBlendingTime": common_types.Float,
})

CCharClassScorpiusSpikeBallPrickAttack_CTunableCharClassScorpiusSpikeBallPrickAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fTimeToDisableAttackAfterMeleeSuccess": common_types.Float,
    "fFrameToReleaseTail": common_types.Float,
})

CCharClassScorpiusSpikeBallPrickFailEvent = Object(base_global_timeline_CEventFields)

CCharClassScorpiusTailSmashAttack_CTunableCharClassScorpiusTailSmashAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
    "fMinTimeToAttack": common_types.Float,
})

CCharClassScorpiusWhiplashAttack_CTunableCharClassScorpiusWhiplashAttack = Object({
    **base_tunable_CTunableFields,
    "bEnabled": construct.Flag,
    "fMinAttackDistance": common_types.Float,
    "fMaxAttackDistance": common_types.Float,
})

CCharClassScourgeTongueSlashAttack = Object({
    **CCharClassAttackFields,
    "fMinInitTime": common_types.Float,
    "fMinDistanceIfTargetOnPath": common_types.Float,
})

CTentacle = Object({
    "sName": common_types.StrId,
    "fExtraNodeLengthFactor": common_types.Float,
    "tTentacleNodes": base_global_CRntVector_base_global_CStrId_,
    "bAllowTrail": construct.Flag,
})

CCharClassScourgeAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oScourgeTongueSlashAttackDef": CCharClassScourgeTongueSlashAttack,
    "oTongue": CTentacle,
    "fTentacleWidth": common_types.Float,
    "vTentacleZAxisThreshold": common_types.CVector3D,
    "fTongueCheckWidth": common_types.Float,
    "fTongueArcCheckBigWidth": common_types.Float,
    "fTongueArcCheckSmallWidth": common_types.Float,
    "fTongueScenarioCheckWidth": common_types.Float,
    "fDefaultShootOffset": common_types.Float,
    "fCrouchingShootOffset": common_types.Float,
    "fHangingAboveVerticalShootOffset": common_types.Float,
    "fHangingHorizontalShootOffset": common_types.Float,
})

CCharClassScourgeBlockAimTrack = Object(base_global_timeline_CTrackFields)

CCharClassScourgeExtendTongueTrack = Object(base_global_timeline_CTrackFields)

CCharClassScourgeLifeComponent = Object(CCharClassEnemyLifeComponentFields)

CCharClassScriptComponent = Object(CCharClassComponentFields)

CCharClassSensorDoorComponent = Object({
    **CCharClassComponentFields,
    "fDelayCloseTime": common_types.Float,
    "fDelayOpenTime": common_types.Float,
})

CCharClassSetActionEvent = Object({
    **base_global_timeline_CEventFields,
    "bForce": construct.Flag,
    "iFrame": common_types.Int,
    "sAction": common_types.StrId,
    "bIsAttack": construct.Flag,
    "fProbability": common_types.Float,
})

CCharClassSetActionToOtherEntityEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntity": common_types.StrId,
    "bForce": construct.Flag,
    "iFrame": common_types.Int,
    "sEntityAction": common_types.StrId,
    "bIsAttack": construct.Flag,
    "fProbability": common_types.Float,
})

CCharClassSetAnimStateTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAnimState": common_types.StrId,
})

CCharClassSetBossMusicPresetEvent = Object({
    **base_global_timeline_CEventFields,
    "sPresetID": common_types.StrId,
})


class EMusicManagerInGameState(enum.IntEnum):
    NONE = 0
    RELAX = 1
    PATROL = 2
    SEARCH = 3
    PATROL2 = 4
    SEARCH2 = 5
    DEATH = 6
    COMBAT = 7
    Invalid = 2147483647


construct_EMusicManagerInGameState = StrictEnum(EMusicManagerInGameState)

CCharClassSetBossMusicPresetStateEvent = Object({
    **base_global_timeline_CEventFields,
    "eState": construct_EMusicManagerInGameState,
})

CCharClassSetCameraFarEvent = Object({
    **base_global_timeline_CEventFields,
    "fValue": common_types.Float,
    "sId": common_types.StrId,
})


class CCharClassSetCameraNearEvent_EDir(enum.IntEnum):
    Any = 0
    Left = 1
    Right = 2
    Invalid = 2147483647


construct_CCharClassSetCameraNearEvent_EDir = StrictEnum(CCharClassSetCameraNearEvent_EDir)

CCharClassSetCameraNearEvent = Object({
    **base_global_timeline_CEventFields,
    "fValue": common_types.Float,
    "sId": common_types.StrId,
    "eDir": construct_CCharClassSetCameraNearEvent_EDir,
})

CCharClassSetComponentEnabledEvent = Object({
    **base_global_timeline_CEventFields,
    "sComponent": common_types.StrId,
    "bEnabled": construct.Flag,
})

CCharClassSetCurrentCubemapIntensityEvent = Object({
    **base_global_timeline_CEventFields,
    "fIntensity": common_types.Float,
    "fTime": common_types.Float,
    "bRelative": construct.Flag,
    "bInSameSubareaEntity": construct.Flag,
})

CCharClassSetCutsceneActorVolumeOverrideEvent = Object({
    **base_global_timeline_CEventFields,
    "sActorName": PropertyEnum,
    "fVolume": common_types.Float,
    "fFadeTime": common_types.Float,
    "sSoundGroupId": common_types.StrId,
})

CCharClassSetDesiredViewDirToPlayerEvent = Object(base_global_timeline_CEventFields)

CCharClassSetDoorLockedEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntityName": PropertyEnum,
    "bLocked": construct.Flag,
})

CCharClassSetDoorStateEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntityName": PropertyEnum,
    "bState": construct.Flag,
    "bUseTransitionAnims": construct.Flag,
    "bPlaySFX": construct.Flag,
    "fSpeed": common_types.Float,
})

CCharClassSetEmmyDoorNearSamusVisibilityEvent = Object({
    **base_global_timeline_CEventFields,
    "bVisible": construct.Flag,
})

CCharClassSetEntityAngEvent = Object({
    **base_global_timeline_CEventFields,
    "vAng": common_types.CVector3D,
    "bRaw": construct.Flag,
})

CCharClassSetEntityStateEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntityName": PropertyEnum,
    "bState": construct.Flag,
})

CCharClassSetEntityVisibilityStateEvent = Object({
    **base_global_timeline_CEventFields,
    "sEntityName": PropertyEnum,
    "bState": construct.Flag,
})

CCharClassSetEnvironmentPresetEvent = Object({
    **base_global_timeline_CEventFields,
    "sPreset": common_types.StrId,
    "bRawChange": construct.Flag,
})

CCharClassSetFadeInSubareaChangeEvent = Object({
    **base_global_timeline_CEventFields,
    "bState": construct.Flag,
})

CCharClassSetLockEnvironmentEvent = Object({
    **base_global_timeline_CEventFields,
    "bMusic": construct.Flag,
    "bEnvironment": construct.Flag,
    "bSound": construct.Flag,
})

CCharClassSetMaterialPropertyBonePositionEvent = Object({
    **base_global_timeline_CEventFields,
    "sNode": common_types.StrId,
    "sActor": common_types.StrId,
    "sFXId": common_types.StrId,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
    "fColorASrc": common_types.Float,
    "fColorADst": common_types.Float,
    "bLocalPosition": construct.Flag,
    "fTime": common_types.Float,
})

CCharClassSetMaterialPropertyEvent = Object({
    **base_global_timeline_CEventFields,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
    "fColorR": common_types.Float,
    "fColorG": common_types.Float,
    "fColorB": common_types.Float,
    "fColorA": common_types.Float,
    "fHDR": common_types.Float,
})

CCharClassSetMaterialPropertyTransitionEvent = Object({
    **base_global_timeline_CEventFields,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
    "fColorR": common_types.Float,
    "fColorG": common_types.Float,
    "fColorB": common_types.Float,
    "fColorA": common_types.Float,
    "fHDR": common_types.Float,
    "fTime": common_types.Float,
})

CCharClassSetMeAsEntityToFollowEvent = Object(base_global_timeline_CEventFields)


class CMeleeComponent_EMeleeTrailFXType(enum.IntEnum):
    NONE = 0
    Trail = 1
    TrailEnd = 2


construct_CMeleeComponent_EMeleeTrailFXType = StrictEnum(CMeleeComponent_EMeleeTrailFXType)

CCharClassSetMeleeTrailFXEnabledEvent = Object({
    **base_global_timeline_CEventFields,
    "eEnabledFX": construct_CMeleeComponent_EMeleeTrailFXType,
})

CCharClassSetModelHiddenEvent = Object({
    **base_global_timeline_CEventFields,
    "bHidden": construct.Flag,
})

CCharClassSetModelVisibleEvent = Object({
    **base_global_timeline_CEventFields,
    "bVisible": construct.Flag,
})

CCharClassSetMusicInGameStateEvent = Object({
    **base_global_timeline_CEventFields,
    "eState": construct_EMusicManagerInGameState,
    "bLockState": construct.Flag,
})

CCharClassSetOnFloorTrack = Object(base_global_timeline_CTrackFields)

CCharClassSetPlayerAsEntityToFollowEvent = Object(base_global_timeline_CEventFields)

CCharClassSetRelativeCameraAnimationBaseEvent = Object(CCharClassSetRelativeCameraAnimationBaseEventFields := {
    **base_global_timeline_CEventFields,
    "sAnimationPath": common_types.StrId,
    "bRawChange": construct.Flag,
    "fInitInterpTime": common_types.Float,
    "fExitInterpTime": common_types.Float,
    "sExitInterpCurve": common_types.StrId,
    "bExitInterpStoringValues": construct.Flag,
    "sStartCallback": common_types.StrId,
    "sEndCallback": common_types.StrId,
    "bHideGUI": construct.Flag,
    "bInitialInterp": construct.Flag,
    "bInvertSide": construct.Flag,
    "bInvertAng": construct.Flag,
    "iIniFrame": common_types.Int,
    "fInitInterpFactor": common_types.Float,
    "bExitWantsToForceEntitiesInFOV": construct.Flag,
    "bResetInterpOnPossess": construct.Flag,
    "fDuration": common_types.Float,
    "bReplaceCurrentCameraAnimation": construct.Flag,
    "sAnimID": common_types.StrId,
    "bUpdateGoalParamsOnExitInterpolation": construct.Flag,
    "bLoopAnim": construct.Flag,
    "bUseRelativeAnimTime": construct.Flag,
    "bUseBoundaries": construct.Flag,
})

TShinesparkTravellingDirectionFlagSet = construct.FlagsEnum(construct.Int32ul, construct_EShinesparkTravellingDirection.enum_class)

TCoolShinesparkSituation = construct.FlagsEnum(construct.Int32ul, construct_ECoolShinesparkSituation.enum_class)

CCharClassSetRelativeCameraAnimationCoolShinesparkEvent = Object({
    **CCharClassSetRelativeCameraAnimationBaseEventFields,
    "tTravellingDirections": TShinesparkTravellingDirectionFlagSet,
    "tSituations": TCoolShinesparkSituation,
    "fTargetSlomo": common_types.Float,
    "fTargetSlomoInterpolation": common_types.Float,
})

CCharClassSetRelativeCameraAnimationEmmyGrabEvent = Object({
    **CCharClassSetRelativeCameraAnimationBaseEventFields,
    "sAlternativeAnimationPath": common_types.StrId,
    "fAlternativeCameraDistanceThreshold": common_types.Float,
})

CCharClassSetRelativeCameraAnimationEvent = Object(CCharClassSetRelativeCameraAnimationBaseEventFields)

CCharClassSetRelativeCameraAnimationWithDirectionEvent = Object({
    **CCharClassSetRelativeCameraAnimationBaseEventFields,
    "sAnimationPathLookingRight": common_types.StrId,
    "sAnimationPathLookingLeft": common_types.StrId,
    "sAnimationPathLookingUp": common_types.StrId,
    "sAnimationPathLookingDown": common_types.StrId,
})

CCharClassSetSceneGroupEnabledEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
    "bEnabled": construct.Flag,
})

CCharClassSetShadowCasterEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassSetSlomoCustomEvent = Object({
    **base_global_timeline_CEventFields,
    "fSlomo": common_types.Float,
    "fTime": common_types.Float,
    "sFunction": common_types.StrId,
})

CCharClassSetSubAreaSetupEvent = Object({
    **base_global_timeline_CEventFields,
    "sSetup": common_types.StrId,
    "sSubArea": common_types.StrId,
    "bPersistent": construct.Flag,
})

CCharClassShakernautDoubleGroundShockAttack = Object({
    **CCharClassAttackFields,
    "fTimeToChargeDoubleGroundShock": common_types.Float,
    "uNumShocks": common_types.UInt,
    "fTimeBetweenShockwaves": common_types.Float,
    "fTimeToEndShockwaves": common_types.Float,
})

CCharClassShakernautPiercingLaserAttack = Object({
    **CCharClassAttackFields,
    "fTimeToChargePiercingLaser": common_types.Float,
    "fTimeToChargeSecondLaser": common_types.Float,
    "fTimeToPrepareLaser": common_types.Float,
    "fTimeLaser": common_types.Float,
    "fTimeToRelocateEye": common_types.Float,
})

CCharClassShakernautAIComponent = Object({
    **CCharClassRobotAIComponentFields,
    "oShakernautDoubleGroundShockAttackDef": CCharClassShakernautDoubleGroundShockAttack,
    "oShakernautPiercingLaserAttackDef": CCharClassShakernautPiercingLaserAttack,
    "fMaxDistToMeleeAttack": common_types.Float,
    "fTimeSinceLastRangedAttack": common_types.Float,
    "fExplosionDuration": common_types.Float,
    "fExplosionWidth": common_types.Float,
    "fExplosionHeight": common_types.Float,
})

CCharClassShakernautInitAttackTrack = Object({
    **CCharClassToStateTrackFields,
    "sInPosAction": common_types.StrId,
})

CCharClassShelmitPlasmaRayAttack = Object({
    **CCharClassAttackFields,
    "fDistanceToInitShooting": common_types.Float,
    "fDistanceToInitShootingWithGrapple": common_types.Float,
    "fMinYAimForGrappleShootDistance": common_types.Float,
    "fMaxTimeShooting": common_types.Float,
    "fMaxTrackedDistance2ReleaseTurn": common_types.Float,
    "fMaxLaunchedTime2ReleaseTurn": common_types.Float,
})

CCharClassShelmitAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oShelmitPlasmaRayAttackDef": CCharClassShelmitPlasmaRayAttack,
    "fMinOpenGrappleTimeAfterAttack": common_types.Float,
    "fMaxGrappledTime": common_types.Float,
    "fMinGrapplePullTimeToBreak": common_types.Float,
    "fMinPlatformRotationSpeed": common_types.Float,
    "fMaxPlatformRotationSpeed": common_types.Float,
    "fMinEntitySpeedForMinRotation": common_types.Float,
    "fMaxEntitySpeedForMaxRotation": common_types.Float,
    "fCrystalMinAlbedoEmissiveFactor": common_types.Float,
    "fCrystalMaxAlbedoEmissiveFactor": common_types.Float,
    "fTimeToDisableCrystal": common_types.Float,
    "fChargeLoopTime": common_types.Float,
    "oRegularShelmitMeleeChargeShotDropProbabilities": SDropProbabilities,
})

CCharClassShelmitChargeTrack = Object(base_global_timeline_CTrackFields)

CCharClassShineonAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fSteeringAcceleration": common_types.Float,
    "fSteeringSpeed": common_types.Float,
    "fMaxTargetDistanceToAccelerateCloseToTarget": common_types.Float,
    "fCloseToTargetAcceleration": common_types.Float,
    "fMaxDistanceToTurn": common_types.Float,
})

CCharClassShineonAIComponent_CTunableCharClassShineonAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMotionSpeed": common_types.Float,
})

CCharClassShinesparkTrack = Object(base_global_timeline_CTrackFields)

CCharClassShipRechargeComponent = Object({
    **CCharClassUsableComponentFields,
    "sSaveUseQuestionID": common_types.StrId,
    "sSaveUseSuccessMessage": common_types.StrId,
})

CCharClassShootActivatorComponent = Object(CCharClassShootActivatorComponentFields := {
    **CCharClassItemLifeComponentFields,
    "fActivationTime": common_types.Float,
    "fTimePerShot": common_types.Float,
})

CCharClassShootActivatorHidrogigaComponent = Object(CCharClassShootActivatorComponentFields)

std_unique_ptr_CShotLaunchConfig_ = Pointer_CShotLaunchConfig.create_construct()

base_global_CRntVector_std_unique_ptr_CShotLaunchConfig__ = common_types.make_vector(std_unique_ptr_CShotLaunchConfig_)

CCharClassShotComponent = Object({
    **CCharClassComponentFields,
    "vLaunchShotConfigs": base_global_CRntVector_std_unique_ptr_CShotLaunchConfig__,
})

CCharClassShowAreaNameEvent = Object({
    **base_global_timeline_CEventFields,
    "fFade": common_types.Float,
})

CCharClassShowCutsceneActorEvent = Object({
    **base_global_timeline_CEventFields,
    "sActorNameLike": common_types.StrId,
    "bResetMaterialAnimation": construct.Flag,
})

CCharClassShowHUDTrack = Object(base_global_timeline_CTrackFields)

CCharClassShowMessageEvent = Object({
    **base_global_timeline_CEventFields,
    "sText": common_types.StrId,
    "sOnMessageSkippedLuaCallback": common_types.StrId,
    "bWaitForInput": construct.Flag,
})

CCharClassShowNodeEvent = Object({
    **base_global_timeline_CEventFields,
    "sNode": common_types.StrId,
})

CCharClassShowRandomNodeEvent = Object({
    **base_global_timeline_CEventFields,
    "sFX": common_types.StrId,
})

CCharClassShowSmartObjectDialogEvent = Object(base_global_timeline_CEventFields)

CCharClassShowTutorialMessageEvent = Object({
    **base_global_timeline_CEventFields,
    "sText": common_types.StrId,
    "sMissionLogTutoId": common_types.StrId,
})

CCharClassSlidleOutSPAgitateTrack = Object(base_global_timeline_CTrackFields)

CCharClassSluggerAcidBallMovementComponent = Object({
    **CCharClassProjectileMovementFields,
    "fTimeMeleeable": common_types.Float,
    "fTimeAbortable": common_types.Float,
})

CCharClassSmartLinkOnAirTrack = Object(base_global_timeline_CTrackFields)

CCharClassSmartLinkWithStopAndSearchTrack = Object(base_global_timeline_CTrackFields)

CCharClassSoundEvent = Object({
    **CCharClassSoundBaseEventFields,
    "sSoundID": common_types.StrId,
    "sAlternativeSoundID1": common_types.StrId,
    "sAlternativeSoundID2": common_types.StrId,
    "sAlternativeSoundID3": common_types.StrId,
    "sAlternativeSoundID4": common_types.StrId,
    "sAlternativeSoundID5": common_types.StrId,
    "sAlternativeSoundID6": common_types.StrId,
    "sAlternativeSoundID7": common_types.StrId,
    "fVolume": common_types.Float,
    "fRadiusMinAttenuation": common_types.Float,
    "fRadiusMaxAttenuation": common_types.Float,
    "sNode": common_types.StrId,
    "fPitch": common_types.Float,
    "fPitchMax": common_types.Float,
    "bStopOnChangeAnim": construct.Flag,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "fStopInTime": common_types.Float,
    "bStopOnEntityDead": construct.Flag,
    "sSoundGroupId": common_types.StrId,
    "sType": common_types.StrId,
    "eSoundType": construct_base_snd_ESndType,
    "bRumbleSync": construct.Flag,
    "fRumbleGainOverride": common_types.Float,
})

CCharClassSoundProofTriggerComponent = Object(CCharClassBaseTriggerComponentFields)

CCharClassSpawnNextCaterzillaEvent = Object(base_global_timeline_CEventFields)

CCharClassSpeedBoosterTrack = Object(base_global_timeline_CTrackFields)

CCharClassSpinJumpEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassSpinJumpTrack = Object(base_global_timeline_CTrackFields)

CCharClassSpitclawkAIComponent = Object({
    **CCharClassSclawkAIComponentFields,
    "fAcidRadius": common_types.Float,
    "fAcidGrowthTime": common_types.Float,
    "fTimeAtMaxRadius": common_types.Float,
    "fWidthMax": common_types.Float,
    "fWidthMin": common_types.Float,
})

CCharClassVulkranMagmaBallMovementComponent = Object(CCharClassVulkranMagmaBallMovementComponentFields := CCharClassProjectileMovementFields)

CCharClassSpittailMagmaBallMovementComponent = Object({
    **CCharClassVulkranMagmaBallMovementComponentFields,
    "fWidthMax": common_types.Float,
    "fWidthMin": common_types.Float,
    "fYOffset": common_types.Float,
    "fTimeToGrow": common_types.Float,
    "fTimeAtMaxSize": common_types.Float,
})

CCharClassStaggerRecoveryTrack = Object(base_global_timeline_CTrackFields)

CCharClassStaggerTrack = Object(base_global_timeline_CTrackFields)

CCharClassStartCentralUnitProtoEvent = Object(base_global_timeline_CEventFields)

CCharClassStartDarknessEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
    "fDarknessLevel": common_types.Float,
    "fInterpolationTime": common_types.Float,
})

CCharClassStartForceEmmyChasePulseEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
})

CCharClassStartPointComponent = Object(CCharClassStartPointComponentFields := {
    **CCharClassComponentFields,
    "bProjectOnFloor": construct.Flag,
})

CCharClassStaticLUACallback1Event = Object({
    **base_global_timeline_CEventFields,
    "sLUAFunction": common_types.StrId,
    "sParam1": common_types.StrId,
})

CCharClassStaticLUACallback2Event = Object({
    **base_global_timeline_CEventFields,
    "sLUAFunction": common_types.StrId,
    "sParam1": common_types.StrId,
    "sParam2": common_types.StrId,
})

CCharClassStaticLUACallbackEvent = Object({
    **base_global_timeline_CEventFields,
    "sLUAFunction": common_types.StrId,
})

CCharClassStealthTrack = Object(base_global_timeline_CTrackFields)

CCharClassSteamJetComponent = Object({
    **CCharClassBaseDamageTriggerComponentFields,
    "fDefaultDamage": common_types.Float,
    "sFX_init": common_types.StrId,
    "sFX_end": common_types.StrId,
    "sFX_1_1": common_types.StrId,
    "sFX_1_2": common_types.StrId,
    "sFX_1_3": common_types.StrId,
    "sFX_1_4": common_types.StrId,
    "sFX_1_5": common_types.StrId,
    "bSteamOnly": construct.Flag,
})

CCharClassStopAllMaterialTransitionEvent = Object(base_global_timeline_CEventFields)

CCharClassStopAudioPresetEvent = Object({
    **base_global_timeline_CEventFields,
    "sPresetID": common_types.StrId,
    "fFadeOut": common_types.Float,
    "fDelayed": common_types.Float,
})

CCharClassStopCameraAnimationEvent = Object(base_global_timeline_CEventFields)

CCharClassStopCameraFXPresetEvent = Object({
    **base_global_timeline_CEventFields,
    "sPreset": common_types.StrId,
})

CCharClassStopChargeEvent = Object({
    **base_global_timeline_CEventFields,
    "bShot": construct.Flag,
})

CCharClassStopDarknessEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
    "fInterpolationTime": common_types.Float,
})

CCharClassStopEnvironmentSoundEvent = Object({
    **base_global_timeline_CEventFields,
    "fTime": common_types.Float,
})

CCharClassStopEnvironmentStreamEvent = Object({
    **base_global_timeline_CEventFields,
    "sPath": common_types.StrId,
    "fFadeOutTime": common_types.Float,
})

CCharClassStopForceEmmyChasePulseEvent = Object({
    **base_global_timeline_CEventFields,
    "sId": common_types.StrId,
})

CCharClassStopLoopSoundEvent = Object({
    **base_global_timeline_CEventFields,
    "sSoundID": common_types.StrId,
    "fFadeOutTime": common_types.Float,
    "fStopInTime": common_types.Float,
})

CCharClassStopMaterialTransitionEvent = Object({
    **base_global_timeline_CEventFields,
    "sMaterialName": common_types.StrId,
    "ePropertyName": construct_engine_utils_EMaterialConstantColor,
    "eStage": construct_msapi_api_shdr_EShaderType,
})

CCharClassStopMusicEvent = Object({
    **base_global_timeline_CEventFields,
    "sPath": common_types.StrId,
    "fFadeOut": common_types.Float,
    "bClearStack": construct.Flag,
})

CCharClassStopPlanktonConeTrack = Object(base_global_timeline_CTrackFields)

CCharClassStopPlayerTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassStopTimelineEvent = Object({
    **base_global_timeline_CEventFields,
    "sName": common_types.StrId,
})

CCharClassStopVibrationEvent = Object({
    **base_global_timeline_CEventFields,
    "sPath": common_types.StrId,
})

CCharClassStunnedTrack = Object(base_global_timeline_CTrackFields)

CCharClassSunnapAIComponent = Object(CCharClassRodotukAIComponentFields)

CCharClassSuperQuetzoaSetVulnerableEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassSwarmAttackComponent = Object({
    **CCharClassAttackComponentFields,
    "fMaxDamage": common_types.Float,
})

CCharClassSwifterAIComponent = Object(CCharClassBehaviorTreeAIComponentFields)

CCharClassSwifterAIComponent_CTunableCharClassSwifterAIComponent = Object({
    **base_tunable_CTunableFields,
    "fMotionSpeed": common_types.Float,
})


class ESwifterSpawnGroupDirection(enum.IntEnum):
    Left = 0
    Right = 1
    Invalid = 2147483647


construct_ESwifterSpawnGroupDirection = StrictEnum(ESwifterSpawnGroupDirection)

CCharClassSwifterSpawnGroupSpawnEvent = Object({
    **base_global_timeline_CEventFields,
    "eDirection": construct_ESwifterSpawnGroupDirection,
    "iSpawnPoint": common_types.Int,
})

CCharClassTakumakuDashAttack = Object(CCharClassAttackFields)


class CCharClassTakumakuAIComponent_ESubspecies(enum.IntEnum):
    Takumaku = 0
    Armadigger = 1
    Klaida = 2
    Invalid = 2147483647


construct_CCharClassTakumakuAIComponent_ESubspecies = StrictEnum(CCharClassTakumakuAIComponent_ESubspecies)

CCharClassTakumakuAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oTakumakuDashAttackDef": CCharClassTakumakuDashAttack,
    "eSubspecies": construct_CCharClassTakumakuAIComponent_ESubspecies,
    "fMinTimeBetweenDigs": common_types.Float,
    "fMaxTimeBetweenDigs": common_types.Float,
    "fMinTimeDigging": common_types.Float,
    "fMaxTimeDigging": common_types.Float,
    "fReachableHeightBeforeAttack": common_types.Float,
    "fReachableHeightOnAttack": common_types.Float,
    "fSpikeTime": common_types.Float,
    "fSpikeActivationInterpolationSpeed": common_types.Float,
    "fSpikeDeactivationInterpolationSpeed": common_types.Float,
    "fSpikeShakeActivationInterpolationSpeed": common_types.Float,
    "fSpikeShakeDeactivationInterpolationSpeed": common_types.Float,
    "fMinChaseDistance": common_types.Float,
    "fMaxChaseDistance": common_types.Float,
    "iChaseMaxNumJumps": common_types.Int,
    "fMinChargeTime": common_types.Float,
    "bWantsAttackPreparationAfterMelee": construct.Flag,
    "bWantsAttackPreparationAfterDetection": construct.Flag,
    "fMaxTargetSeparationBehindToTurn": common_types.Float,
    "fMaxTimeDetectingBehindToTurn": common_types.Float,
    "fMaxTimeMissingToStop": common_types.Float,
})

CCharClassTakumakuAllowEndForcedTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassTakumakuAllowFrontWallCrashTrack = Object(base_global_timeline_CTrackFields)

CCharClassTakumakuAllowSpikesTrack = Object(base_global_timeline_CTrackFields)

CCharClassTakumakuChargeTrack = Object(base_global_timeline_CTrackFields)

CCharClassTakumakuIgnoreJumpbackTrack = Object(base_global_timeline_CTrackFields)

CCharClassThrowElectricBombEvent = Object({
    **base_global_timeline_CEventFields,
    "sBone": common_types.StrId,
})

CCharClassThrowSuccubusShitEvent = Object({
    **base_global_timeline_CEventFields,
    "sBone": common_types.StrId,
    "fBonePositionOffsetX": common_types.Float,
    "fSpeed": common_types.Float,
})

CCharClassThrowWeaponEvent = Object({
    **base_global_timeline_CEventFields,
    "fTimeToLive": common_types.Float,
    "fThrowingAngle": common_types.Float,
    "bRotateToDirection": construct.Flag,
    "fSpinFactorX": common_types.Float,
    "fSpinFactorY": common_types.Float,
    "fSpinFactorZ": common_types.Float,
    "bRepositionOnEnd": construct.Flag,
    "fMass": common_types.Float,
    "bReboundEnabled": construct.Flag,
    "iReboundMaxNumber": common_types.Int,
    "fReboundRestitution": common_types.Float,
    "fDestinationOffsetX": common_types.Float,
    "bDestinationOnFloor": construct.Flag,
    "fDamage": common_types.Float,
    "iEntitiesToDamage": common_types.Int,
    "bIgnoreCollisionWithEntities": construct.Flag,
    "bDamageWithBox": construct.Flag,
})


class CTimelineComponent_ENextPolicy(enum.IntEnum):
    NEXT = 0
    RANDOM = 1
    RANDOM_DELAY = 2
    Invalid = 2147483647


construct_CTimelineComponent_ENextPolicy = StrictEnum(CTimelineComponent_ENextPolicy)

CCharClassTimelineComponent = Object({
    **CCharClassComponentFields,
    "sInitAction": common_types.StrId,
    "eNextPolicy": construct_CTimelineComponent_ENextPolicy,
    "fMinDelayTime": common_types.Float,
    "fMaxDelayTime": common_types.Float,
    "eLayerInFrustumToLaunchInRandomDelayPolicy": base_global_timeline_TLayers,
})

CCharClassToAimBlendTimeOverrideTrack = Object({
    **base_global_timeline_CTrackFields,
    "fValue": common_types.Float,
})

CCharClassToCrouchTrack = Object(CCharClassToStateTrackFields)

CCharClassToDefaultBlendTimeOverrideTrack = Object({
    **base_global_timeline_CTrackFields,
    "fValue": common_types.Float,
})

CCharClassToRecoilBlendTimeOverrideTrack = Object({
    **base_global_timeline_CTrackFields,
    "fValue": common_types.Float,
})

CCharClassToRelaxTrack = Object(CCharClassToStateTrackFields)

CCharClassToRunNearWallTrack = Object({
    **CCharClassToStateTrackFields,
    "sHighAction": common_types.StrId,
    "sLowAction": common_types.StrId,
    "sNoHandAction": common_types.StrId,
    "fCheckDistance": common_types.Float,
})

CCharClassToRunTrack = Object(CCharClassToStateTrackFields)

CCharClassToSmartLinkTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
})

CCharClassTrackTargetTrack = Object(base_global_timeline_CTrackFields)

CCharClassTrainUsableComponent = Object({
    **CCharClassUsableComponentFields,
    "sUsableLeftAction": common_types.StrId,
    "sUsableRightAction": common_types.StrId,
    "sUsableLevelChangeLeftAction": common_types.StrId,
    "sUsableLevelChangeRightAction": common_types.StrId,
    "sUseInitRightAction": common_types.StrId,
    "sUseInitLeftAction": common_types.StrId,
    "sUseLeftAction": common_types.StrId,
    "sUseRightAction": common_types.StrId,
    "sUseLeftLevelChangeAction": common_types.StrId,
    "sUseRightLevelChangeAction": common_types.StrId,
    "sUseLeftEndAction": common_types.StrId,
    "sUseRightEndAction": common_types.StrId,
})

CCharClassTriggerNavMeshItemComponent = Object(CCharClassNavMeshItemComponentFields)

CCharClassTryToLaunchBlockableAttackWarningTrack = Object({
    **base_global_timeline_CTrackFields,
    "sFXName": common_types.StrId,
})

CCharClassTunnelTrapMorphballComponent = Object({
    **CCharClassComponentFields,
    "bEnableFinalCollisionOnClose": construct.Flag,
})

CCharClassTurnEndTrack = Object(base_global_timeline_CTrackFields)

CCharClassTurnTrack = Object(base_global_timeline_CTrackFields)

CCharClassTweakAIEndActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakAbortAlternativeActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakAirFrictionTrack = Object({
    **base_global_timeline_CTrackFields,
    "fFrictionFactor": common_types.Float,
    "fNonAffectedSpeedFactorFromAirVelocityX": common_types.Float,
})

CCharClassTweakAttackPlayRateTrack = Object({
    **base_global_timeline_CTrackFields,
    "fPresetA": common_types.Float,
    "fPresetB": common_types.Float,
    "fPresetC": common_types.Float,
})

CCharClassTweakBackInitTrack = Object(CCharClassToStateTrackFields)

CCharClassTweakBombCharClassTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCharClass": common_types.StrId,
})

CCharClassTweakCameraDesiredInterpolationTrack = Object({
    **base_global_timeline_CTrackFields,
    "fDesiredInterpolation": common_types.Float,
})

CCharClassTweakComputeDeltaTrack = Object({
    **base_global_timeline_CTrackFields,
    "fMultiplierX": common_types.Float,
    "fMultiplierY": common_types.Float,
    "fMultiplierZ": common_types.Float,
})

CCharClassTweakConvertToMorphBallVelocityTrack = Object({
    **base_global_timeline_CTrackFields,
    "bUseFrontDirection": construct.Flag,
    "fVelocity": common_types.Float,
})

CCharClassTweakDeathActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakDisplacementTrack = Object({
    **base_global_timeline_CTrackFields,
    "fFactor": common_types.Float,
})

CCharClassTweakFallActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFallEndActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFallForwardActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFallInSmallHoleAheadActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFloorSlide45InitActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFloorSlideEndActionTrack = Object({
    **CCharClassTweakActionBaseTrackFields,
    "fMaxDistanceToCollision": common_types.Float,
})

CCharClassTweakFloorSlideEndWallActionTrack = Object({
    **CCharClassTweakActionBaseTrackFields,
    "fMaxDistanceToCollisionToApply": common_types.Float,
})

CCharClassTweakFreezeActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakFrontInitTrack = Object({
    **CCharClassToStateTrackFields,
    "bTweakWithSameActionAndDifferentPrefix": construct.Flag,
})

CCharClassTweakGrappleDragActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakGrappleInitActionTrack = Object({
    **CCharClassTweakActionBaseTrackFields,
    "sInvertAction": common_types.StrId,
})

CCharClassTweakGrappleToMagnetCeilingActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakGrappleToMagnetWallActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakGrappleVisualNodeTrack = Object({
    **base_global_timeline_CTrackFields,
    "sNode": common_types.StrId,
})

CCharClassTweakGravityTrack = Object({
    **base_global_timeline_CTrackFields,
    "fGravity": common_types.Float,
    "fMinTimeOnAirToApply": common_types.Float,
})

CCharClassTweakHangToMorphBallActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakHangTransitionToShootingPoseActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakInvertAnalogAimActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakJumpGroundActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakJumpImpulseTrack = Object({
    **base_global_timeline_CTrackFields,
    "fImpulseMultiplierX": common_types.Float,
    "fImpulseMultiplierY": common_types.Float,
    "bKeepExistingVelocityX": construct.Flag,
    "bKeepExistingVelocityY": construct.Flag,
})

CCharClassTweakJumpToFallAction = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakLineBombCharClassTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCharClass": common_types.StrId,
})

CCharClassTweakMagnetCeilingUpToWallActionTrack = Object(CCharClassTweakActionBaseTrackFields)


class CSamusMagnetGloveMovementState_ESurfaceType(enum.IntEnum):
    WALL = 0
    CEILING = 1
    CEILING_45 = 2
    Invalid = 2147483647


construct_CSamusMagnetGloveMovementState_ESurfaceType = StrictEnum(CSamusMagnetGloveMovementState_ESurfaceType)

CCharClassTweakMagnetJumpSurfaceTypeTrack = Object({
    **base_global_timeline_CTrackFields,
    "eSurfaceType": construct_CSamusMagnetGloveMovementState_ESurfaceType,
})

CCharClassTweakMotionSpeedTrack = Object({
    **base_global_timeline_CTrackFields,
    "fFactor": common_types.Float,
})

CCharClassTweakNextWalkCyclesEvent = Object(base_global_timeline_CEventFields)

CCharClassTweakParkourActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakParkourCloseActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakParkourFallActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakParkourNearActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakPlayRateTrack = Object({
    **base_global_timeline_CTrackFields,
    "sTunableId": common_types.StrId,
})

CCharClassTweakPlayRateTrack_CTunableCharClassTweakPlayRateTrack = Object({
    **base_tunable_CTunableFields,
    "fCommanderUltimateGrabSpeed1": common_types.Float,
    "fCommanderUltimateGrabSpeed2": common_types.Float,
    "fWarriorXUltimateGrabSpeed1": common_types.Float,
    "fWarriorXUltimateGrabSpeed2": common_types.Float,
    "fPlayRateFactor": common_types.Float,
    "fMagnetWallRunUp": common_types.Float,
    "fMagnetWallRunDown": common_types.Float,
    "fMagnetCeilingRun": common_types.Float,
    "fStealthMagnetWallRunUp": common_types.Float,
    "fStealthMagnetWallRunDown": common_types.Float,
    "fStealthMagnetCeilingRun": common_types.Float,
    "fShinesparkChargeExtensionFactor": common_types.Float,
    "fCommanderUltimateGrabSpeed0": common_types.Float,
    "fWarriorXUltimateGrabSpeed0": common_types.Float,
    "fHydrogigaPolyp01FallSpeed": common_types.Float,
    "fHydrogigaPolyp02FallSpeed": common_types.Float,
    "fHydrogigaPolyp03FallSpeed": common_types.Float,
    "fHydrogigaPolyp04FallSpeed": common_types.Float,
    "fHydrogigaPolyp05FallSpeed": common_types.Float,
    "fHydrogigaPolyp06FallSpeed": common_types.Float,
    "fHydrogigaPolyp07FallSpeed": common_types.Float,
    "fHydrogigaPolyp08FallSpeed": common_types.Float,
    "fHydrogigaPolyp09FallSpeed": common_types.Float,
    "fOpticCamouflageSpeed": common_types.Float,
    "fKraidPistonMoveUpSpeed": common_types.Float,
    "fGoliathSpeed": common_types.Float,
    "fChozoCommanderCommanderXSpeed": common_types.Float,
    "fCooldownXBossLavaCarpetSpeed": common_types.Float,
    "fCooldownXBossMoveArmSpeedLeftUp": common_types.Float,
    "fCooldownXBossMoveArmSpeedLeftDown": common_types.Float,
    "fCooldownXBossMoveArmSpeedRightUp": common_types.Float,
    "fCooldownXBossMoveArmSpeedRightDown": common_types.Float,
    "fEmmyTunnelWalk": common_types.Float,
    "fMeleeSpeed": common_types.Float,
    "fEmmyStaggerRecoverySpeed": common_types.Float,
    "fEmmyStaggerRecoveryTurnSpeed": common_types.Float,
    "fCantFireBufferedInput": common_types.Float,
    "fScorpiusRegereratingMaskAction": common_types.Float,
    "fScorpiusHeadBlendSpeed": common_types.Float,
})

CCharClassTweakPowerBombCharClassTrack = Object({
    **base_global_timeline_CTrackFields,
    "sCharClass": common_types.StrId,
})


class CSamusMovement_EUpdateCollisionsPhaseOrder(enum.IntEnum):
    SinglePhaseVerticalHorizontal = 0
    TwoPhasesVerticalThenHorizontal = 1
    Invalid = 2147483647


construct_CSamusMovement_EUpdateCollisionsPhaseOrder = StrictEnum(CSamusMovement_EUpdateCollisionsPhaseOrder)

CCharClassTweakSamusUpdateCollisionsTrack = Object({
    **base_global_timeline_CTrackFields,
    "eOrder": construct_CSamusMovement_EUpdateCollisionsPhaseOrder,
})

CCharClassTweakShinesparkCollisionActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakShinesparkImpactActionTrack = Object({
    **base_global_timeline_CTrackFields,
    "sAction": common_types.StrId,
    "bSchedule": construct.Flag,
})

CCharClassTweakSlopeModelOffsetTrack = Object({
    **base_global_timeline_CTrackFields,
    "fSlopeUpOffset": common_types.Float,
    "fSlopeDownOffset": common_types.Float,
    "fFadeInFrames": common_types.Float,
    "fFadeOutFrames": common_types.Float,
})

CCharClassTweakStealthActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakStealthEndActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassTweakTurnActionTrack = Object({
    **CCharClassTweakActionBaseTrackFields,
    "bKeepViewDir": construct.Flag,
})

CCharClassTweakUnfreezeActionTrack = Object(CCharClassTweakActionBaseTrackFields)

CCharClassUltimateGrabEnergyRecharge = Object(base_global_timeline_CTrackFields)

CCharClassUsableFadeInEvent = Object(CCharClassBaseFadeInEventFields)

CCharClassUseDCCenterTrack = Object(base_global_timeline_CTrackFields)

CCharClassUseDCFeetForSlopeModelOffsetTrack = Object(base_global_timeline_CTrackFields)

CCharClassUseDC_ShotOrientationTrack = Object({
    **base_global_timeline_CTrackFields,
    "bProjectOnXY": construct.Flag,
})

CCharClassUseSmartObjectEvent = Object(base_global_timeline_CEventFields)

CCharClassUseWalkTurnTrack = Object(base_global_timeline_CTrackFields)

base_global_CRntVector_SLaunchConfig_ = common_types.make_vector(SLaunchConfig)

TLaunchConfigs = base_global_CRntVector_SLaunchConfig_


class CCharClassVulkranAIComponent_ESubspecies(enum.IntEnum):
    Vulkran = 0
    Spittail = 1
    Invalid = 2147483647


construct_CCharClassVulkranAIComponent_ESubspecies = StrictEnum(CCharClassVulkranAIComponent_ESubspecies)

CCharClassVulkranAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fFrenzyTime": common_types.Float,
    "fActivationTime": common_types.Float,
    "fPatrolMinTimeBetweenBalls": common_types.Float,
    "fPatrolMaxTimeBetweenBalls": common_types.Float,
    "fCombatMinTimeBetweenBalls": common_types.Float,
    "fCombatMaxTimeBetweenBalls": common_types.Float,
    "fBallGravity": common_types.Float,
    "fLaunchUpAngleRef": common_types.Float,
    "fLaunchUpAngleLowerOffset": common_types.Float,
    "fLaunchUpAngleUpperOffset": common_types.Float,
    "fLaunchRightAngleRef": common_types.Float,
    "fLaunchLeftAngleRef": common_types.Float,
    "fLaunchSideAngleLowerOffset": common_types.Float,
    "fLaunchSideAngleUpperOffset": common_types.Float,
    "fLaunchDownAngleRef": common_types.Float,
    "bMirrorLaunchDown": construct.Flag,
    "fLaunchDownAngleLowerOffset": common_types.Float,
    "fLaunchDownAngleUpperOffset": common_types.Float,
    "fLaunchUpMinInitialSpeed": common_types.Float,
    "fLaunchUpMaxInitialSpeed": common_types.Float,
    "fLaunchSideMinInitialSpeed": common_types.Float,
    "fLaunchSideMaxInitialSpeed": common_types.Float,
    "fLaunchDownMinInitialSpeed": common_types.Float,
    "fLaunchDownMaxInitialSpeed": common_types.Float,
    "sWalkRightLaunchUpConfig": SLaunchConfig,
    "sWalkDownLaunchRightConfig": SLaunchConfig,
    "sWalkLeftLaunchDownConfig": SLaunchConfig,
    "sWalkUpLaunchLeftConfig": SLaunchConfig,
    "tLaunchConfigs": TLaunchConfigs,
    "fMinTimeBetweenAttacks": common_types.Float,
    "fMaxTimeBetweenAttacks": common_types.Float,
    "fMinTimeAttacking": common_types.Float,
    "fMaxTimeAttacking": common_types.Float,
    "fShotHeightOffset": common_types.Float,
    "fTimeInFrustumToStartAttack": common_types.Float,
    "fTimeOutOfFrustumToEndAttack": common_types.Float,
    "fMaxLOSDistanceToChasePoint": common_types.Float,
    "sMagmaBallCharClass": common_types.StrId,
    "eSubspecies": construct_CCharClassVulkranAIComponent_ESubspecies,
})


class CCharClassVulkranAIComponent_EDir(enum.IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3
    Invalid = 2147483647


construct_CCharClassVulkranAIComponent_EDir = StrictEnum(CCharClassVulkranAIComponent_EDir)

CCharClassVulnerableToFloorSlideAvoidableAttacksTrack = Object(base_global_timeline_CTrackFields)

CCharClassWantsMissileVisibleEvent = Object({
    **base_global_timeline_CEventFields,
    "bVisible": construct.Flag,
})

CCharClassWarLotusAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fImpactToRelaxTime": common_types.Float,
    "fBumpToRelaxTime": common_types.Float,
    "fImpactTime": common_types.Float,
    "fBumpTime": common_types.Float,
})

CCharClassWaterNozzleComponent = Object({
    **CCharClassComponentFields,
    "fNozzleHeightOffset": common_types.Float,
})

CCharClassWaterPoolComponent = Object({
    **CCharClassLiquidPoolComponentFields,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CCharClassWaterValveAllowWaterLoopEndEvent = Object(base_global_timeline_CEventFields)

CCharClassWeightActivableMovablePlatformComponent = Object({
    **CCharClassMovablePlatformComponentFields,
    "sActionOnActivated": common_types.StrId,
})

CCharClassWeightActivablePropComponent = Object({
    **CCharClassComponentFields,
    "bDeleteOnOpenAnimationFinished": construct.Flag,
})

CCharClassWeightActivatedPlatformSmartObjectComponent = Object({
    **CCharClassComponentFields,
    "sActionLayer": common_types.StrId,
})

CCharClassXParasiteAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "fAbsorptionDistance": common_types.Float,
    "uMaxSimultaneous": common_types.UInt,
    "fMaxSteeringAcceleration": common_types.Float,
    "fMaxSteeringBrake": common_types.Float,
    "fMaxSteeringChangingDir": common_types.Float,
    "fBrakeDistance": common_types.Float,
    "bLimitSteeringForceAngle": construct.Flag,
    "fMaxSteeringForceAngle": common_types.Float,
    "fWanderRadius": common_types.Float,
    "fInitTime": common_types.Float,
    "fWanderTime": common_types.Float,
    "fOffSetDisplacementNearPowerBomb": common_types.Float,
    "fDistanceArriveEndAttract": common_types.Float,
})

CCharClassXParasiteAbsorbedEvent = Object(base_global_timeline_CEventFields)

CCharClassXParasiteDropComponent = Object(CCharClassComponentFields)

CCharClassXParasiteEnableTrailParticlesEvent = Object({
    **base_global_timeline_CEventFields,
    "bEnabled": construct.Flag,
})

CCharClassYamplotXBiteAttack = Object(CCharClassAttackFields)

CCharClassYamplotXStepAttack = Object(CCharClassAttackFields)


class CCharClassYamplotXAIComponent_ESubspecies(enum.IntEnum):
    Yampa = 0
    YamplotX = 1
    Invalid = 2147483647


construct_CCharClassYamplotXAIComponent_ESubspecies = StrictEnum(CCharClassYamplotXAIComponent_ESubspecies)

CCharClassYamplotXAIComponent = Object({
    **CCharClassBehaviorTreeAIComponentFields,
    "oYamplotXBiteAttackDef": CCharClassYamplotXBiteAttack,
    "oYamplotXStepAttackDef": CCharClassYamplotXStepAttack,
    "eSubspecies": construct_CCharClassYamplotXAIComponent_ESubspecies,
})

CCharClassYamplotXConcatSLTrack = Object(base_global_timeline_CTrackFields)

CCharacterMovement = Object(CCharacterMovementFields := CMovementComponentFields)

CCharacterMovement_CTunableCharacterMovement = Object({
    **base_tunable_CTunableFields,
    "fFixPositionDefaultTolerance": common_types.Float,
})

CChasingCameraCtrl = Object(CCameraCtrlFields)

CCheckCoolShinesparkSuccessfullyCompletedLogicAction = Object(CTriggerLogicActionFields)

CChozoCommanderAIComponent = Object({
    **CBossAIComponentFields,
    "bUltimateGrabTestMode": construct.Flag,
    "wpUltimateGrabLandmark": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
    "wpPhase2CutscenePlayer": common_types.StrId,
    "wpPhase3CutscenePlayer": common_types.StrId,
    "wpPhase3EndLeftCutscenePlayer": common_types.StrId,
    "wpPhase3EndRightCutscenePlayer": common_types.StrId,
})

CChozoCommanderAttack = Object(CChozoCommanderAttackFields := CAttackFields)

CChozoCommanderAirAttack = Object(CChozoCommanderAirAttackFields := CChozoCommanderAttackFields)

CChozoCommanderAirChargeAttack = Object(CChozoCommanderAirAttackFields)

CChozoCommanderGroundAttack = Object(CChozoCommanderGroundAttackFields := CChozoCommanderAttackFields)

CChozoCommanderAuraScratchAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderBeamBurstAttack = Object(CChozoCommanderAirAttackFields)

CChozoCommanderDropCameraCtrl = Object(CCameraBoundaryCtrlFields)

CChozoCommanderEnergyShardsAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderEnergyShardsFragmentMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderEnergyShardsSphereMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderHyperDashAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderHypersparkAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderKiCounterAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderKiGrabAttack = Object(CChozoCommanderAttackFields)


class CChozoCommanderKiGrabAttack_SState(enum.IntEnum):
    NONE = 0
    Idle = 1
    SamusImpacted = 2
    GrabSeqPrep1 = 3
    GrabSeq1 = 4
    GrabSeq1EarlyFail = 5
    GrabSeq1TimeOut = 6
    GrabSeq1Win = 7
    Invalid = 2147483647


construct_CChozoCommanderKiGrabAttack_SState = StrictEnum(CChozoCommanderKiGrabAttack_SState)

CChozoCommanderKiStrikeAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderLandingSlamAttack = Object(CChozoCommanderAirAttackFields)

CChozoCommanderPowerPulseAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderSentenceSphereAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderSentenceSphereLifeComponent = Object(CBasicLifeComponentFields)

CChozoCommanderSentenceSphereMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderTriComboAttack = Object(CChozoCommanderGroundAttackFields)

CChozoCommanderUltimateGrabAttack = Object(CChozoCommanderAttackFields)

CChozoCommanderUltimateGrabAttack_CTunableCommanderUltimateGrab = Object(base_tunable_CTunableFields)


class CChozoCommanderUltimateGrabAttack_SState(enum.IntEnum):
    NONE = 0
    Idle = 1
    SamusImpacted = 2
    GrabSeqPrep1 = 3
    GrabSeq1 = 4
    GrabSeq1EarlyFail = 5
    GrabSeq1TimeOut = 6
    GrabSeq1Win = 7
    GrabSeqPrep2 = 8
    GrabSeq2 = 9
    GrabSeq2EarlyFail = 10
    GrabSeq2TimeOut = 11
    GrabSeq2Win = 12
    Invalid = 2147483647


construct_CChozoCommanderUltimateGrabAttack_SState = StrictEnum(CChozoCommanderUltimateGrabAttack_SState)

CChozoCommanderXLifeComponent = Object({
    **CLifeComponentFields,
    "wpIntroductionCutScenePlayer": common_types.StrId,
    "wpDeathCutScenePlayer": common_types.StrId,
})

CChozoCommanderZeroLaserAttack = Object(CChozoCommanderAirAttackFields)

CChozoCommanderZeroLaserBaseAttack = Object(CChozoCommanderAttackFields)

CChozoCommanderZeroLaserGroundedAttack = Object(CChozoCommanderGroundAttackFields)

CChozoRobotSoldierAIComponent = Object({
    **CBossAIComponentFields,
    "bAlternativeSkin": construct.Flag,
    "wpPatrolPath": common_types.StrId,
    "tShootingPositions": base_global_CRntVector_CGameLink_CActor__,
})

CChozoRobotSoldierBeamMovementComponent = Object(CProjectileMovementFields)

CChozoRobotSoldierCannonShotAttack = Object(CAttackFields)

CChozoRobotSoldierCannonShotPattern = Object({
    "fInitialTimeToShot": common_types.Float,
    "fTimeBetweenShot_1_2": common_types.Float,
    "fTimeBetweenShot_2_3": common_types.Float,
})

CChozoRobotSoldierDashSlashAttack = Object(CAttackFields)

CChozoRobotSoldierDisruptionFieldAttack = Object(CAttackFields)

CChozoRobotSoldierUppercutAttack = Object(CAttackFields)


class CChozoWarriorAIComponent_ETransformationType(enum.IntEnum):
    NONE = 0
    Quick = 1
    Full = 2
    Quick_without_init = 3
    Invalid = 2147483647


construct_CChozoWarriorAIComponent_ETransformationType = StrictEnum(CChozoWarriorAIComponent_ETransformationType)

CChozoWarriorAIComponent = Object(CChozoWarriorAIComponentFields := {
    **CBossAIComponentFields,
    "wpChozoWarrioXSpawnPoint": common_types.StrId,
    "eTransformationType": construct_CChozoWarriorAIComponent_ETransformationType,
})

CChozoWarriorAttack = Object(CChozoWarriorAttackFields := CAttackFields)

CChozoWarriorDeflectorShieldAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorEliteAIComponent = Object(CChozoWarriorAIComponentFields)

CChozoWarriorGlaiveSpinAttack = Object(CChozoWarriorGlaiveSpinAttackFields := CChozoWarriorAttackFields)

CChozoWarriorGlaiveWalljumpAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorXAIComponent = Object(CChozoWarriorXAIComponentFields := CChozoWarriorAIComponentFields)

CChozoWarriorXChangeWallAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorXEliteAIComponent = Object(CChozoWarriorXAIComponentFields)

CChozoWarriorXGlaiveSpinAttack = Object(CChozoWarriorGlaiveSpinAttackFields)

CChozoWarriorXLandAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorXSpitAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorXSpitMovementComponent = Object(CProjectileMovementFields)

CChozoWarriorXUltimateGrabAttack = Object(CChozoWarriorAttackFields)

CChozoWarriorXUltimateGrabAttack_CTunableChozoWarriorXUltimateGrabAttack = Object(base_tunable_CTunableFields)


class CChozoWarriorXUltimateGrabAttack_SState(enum.IntEnum):
    NONE = 0
    Idle = 1
    SamusImpacted = 2
    GrabSeqPrep1 = 3
    GrabSeq1 = 4
    GrabSeq1EarlyFail = 5
    GrabSeq1TimeOut = 6
    GrabSeq1Win = 7
    GrabSeqPrep2 = 8
    GrabSeq2 = 9
    GrabSeq2EarlyFail = 10
    GrabSeq2TimeOut = 11
    GrabSeq2Win = 12
    Invalid = 2147483647


construct_CChozoWarriorXUltimateGrabAttack_SState = StrictEnum(CChozoWarriorXUltimateGrabAttack_SState)

CChozoWarriorXWallClimbAttack = Object(CChozoWarriorAttackFields)

CChozoZombieXAIComponent = Object(CBehaviorTreeAIComponentFields)

CChozoZombieXPoisonClawsAttack = Object(CAttackFields)


class CChozoZombieXPoisonClawsAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    AttackState = 2
    AttackEndState = 3
    End = 4
    Invalid = 2147483647


construct_CChozoZombieXPoisonClawsAttack_EState = StrictEnum(CChozoZombieXPoisonClawsAttack_EState)

CChozoZombieXSpawnPointComponent = Object(CSpawnPointComponentFields)

CChozombieFXComponent = Object(CSceneComponentFields)

std_unique_ptr_CTriggerComponent_SActivationCondition_ = Pointer_CTriggerComponent_SActivationCondition.create_construct()

base_global_CRntVector_std_unique_ptr_CTriggerComponent_SActivationCondition__ = common_types.make_vector(std_unique_ptr_CTriggerComponent_SActivationCondition_)

CTriggerComponent = Object(CTriggerComponentFields := {
    **CComponentFields,
    "bCallEntityLuaCallback": construct.Flag,
    "iReverb": common_types.Int,
    "iLowPassFilter": common_types.Int,
    "sOnEnable": common_types.StrId,
    "sOnDisable": common_types.StrId,
    "bOnEnableAlways": construct.Flag,
    "bOnDisableAlways": construct.Flag,
    "bStartEnabled": construct.Flag,
    "bCheckAllEntities": construct.Flag,
    "bPersistentState": construct.Flag,
    "sSfxType": common_types.StrId,
    "lstActivationConditions": base_global_CRntVector_std_unique_ptr_CTriggerComponent_SActivationCondition__,
})

CColliderTriggerComponent = Object({
    **CTriggerComponentFields,
    "lnkShape": common_types.StrId,
})

CCollisionMaterialCacheComponent = Object(CComponentFields)

CConstantMovement = Object(CCharacterMovementFields)

CMarkMinimapLogicAction = Object(CMarkMinimapLogicActionFields := {
    **CTriggerLogicActionFields,
    "wpVisibleLogicShape": common_types.StrId,
    "wpVisitedLogicShape": common_types.StrId,
})

CCoolShinesparkMarkMinimapLogicAction = Object(CMarkMinimapLogicActionFields)

CCooldownXBossAIComponent = Object({
    **CBossAIComponentFields,
    "wpWindTunnelDamageTrigger": common_types.StrId,
    "wpLavaCarpetFloorFX": common_types.StrId,
    "wpCoolShinesparkTrigger": common_types.StrId,
    "wpDeathCutscenePlayer": common_types.StrId,
    "wpDeathFromGrabCutscenePlayer": common_types.StrId,
})

CCooldownXBossAttack = Object(CCooldownXBossAttackFields := CAttackFields)

CCooldownXBossFireBallDef = Object({
    "bEnabled": construct.Flag,
    "fPreparationTimeOffset": common_types.Float,
    "bBreakable": construct.Flag,
})

CCooldownXBossFireBallMovementComponent = Object(CProjectileMovementFields)

base_global_CRntVector_CCooldownXBossFireBallDef_ = common_types.make_vector(CCooldownXBossFireBallDef)

CCooldownXBossFireWallDef = Object({
    "tFireBalls": base_global_CRntVector_CCooldownXBossFireBallDef_,
    "fDelay": common_types.Float,
    "fHorizontalOffset": common_types.Float,
    "bSpawnWallDamage": construct.Flag,
    "bStartWind": construct.Flag,
    "bStartStun": construct.Flag,
})

CCooldownXBossLaserBiteAttack = Object(CCooldownXBossAttackFields)

CCooldownXBossLavaCarpetAttack = Object(CCooldownXBossAttackFields)


class ELavaCarpetState(enum.IntEnum):
    Init = 0
    ShotInit = 1
    Shot = 2
    StopShot = 3
    Breathe = 4
    End = 5
    Invalid = 2147483647


construct_ELavaCarpetState = StrictEnum(ELavaCarpetState)

CCooldownXBossLavaCarpetDef = Object({
    "eState": construct_ELavaCarpetState,
    "fWidth": common_types.Float,
    "fTime": common_types.Float,
    "fPlayRateFactor": common_types.Float,
    "bChangeDirection": construct.Flag,
})

CCooldownXBossLavaDropsAttack = Object(CCooldownXBossAttackFields)

CCooldownXBossReaperAttack = Object(CCooldownXBossAttackFields)

CCooldownXBossStrongWhipAttack = Object(CCooldownXBossAttackFields)

CCooldownXBossWeakPointLifeComponent = Object(CBasicLifeComponentFields)

CCooldownXBossWindTunnelAttack = Object(CCooldownXBossAttackFields)

CCoreXAIComponent = Object(CBossAIComponentFields)

CCreditsMode_CTunableCredits = Object({
    **base_tunable_CTunableFields,
    "vColorTitle": common_types.CVector3D,
    "vColorSubtitle": common_types.CVector3D,
    "vColorEntry": common_types.CVector3D,
})

CCubeMapComponent = Object({
    **CComponentFields,
    "vCubePos": common_types.CVector3D,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "vBoxBounds": common_types.CVector3D,
    "fIntensity": common_types.Float,
    "bEnableCulling": construct.Flag,
    "sTexturePathSpecular": common_types.StrId,
    "sTexturePathDiffuse": common_types.StrId,
})


class cutscene_EDevelopmentState(enum.IntEnum):
    Internal = 0
    PlaceHolder = 1
    WorkInProgress = 2
    Completed = 3
    ShowPlaceholder = 4
    Invalid = 2147483647


construct_cutscene_EDevelopmentState = StrictEnum(cutscene_EDevelopmentState)

CCutSceneDef_CTakeDef = Object({
    "sId": common_types.StrId,
    "iFrames": common_types.Int,
    "sCamera": common_types.StrId,
    "sOnStart": common_types.StrId,
    "sOnExit": common_types.StrId,
    "sOnSkip": common_types.StrId,
    "fInitialDistanceListenerToTarget": common_types.Float,
    "fMinimumDistanceListenerToTarget": common_types.Float,
    "fMaximumDistanceListenerToTarget": common_types.Float,
})

base_global_CRntVector_CCutSceneDef_CTakeDef_ = common_types.make_vector(CCutSceneDef_CTakeDef)

TAnimationTagFlagSet = construct.FlagsEnum(construct.Int32ul, construct_EAnimationTag.enum_class)

base_global_CRntSmallDictionary_base_global_CStrId__float_ = common_types.make_dict(common_types.Float, key=common_types.StrId)

CCutSceneDef_CAnimationLayerDef = Object({
    "sExitAnim": common_types.StrId,
    "sExitAnimChannel": common_types.StrId,
    "fExitAnimFrame": common_types.Float,
})

base_global_CRntSmallDictionary_base_global_CStrId__CCutSceneDef_CAnimationLayerDef_ = common_types.make_dict(CCutSceneDef_CAnimationLayerDef, key=common_types.StrId)

CCutSceneDef_CActorDef = Object({
    "sId": common_types.StrId,
    "sCharClass": common_types.StrId,
    "sInGameEntityId": common_types.StrId,
    "bInGameEntityVisibleOnEnd": construct.Flag,
    "bExitClearTags": construct.Flag,
    "fExitAnimTags": TAnimationTagFlagSet,
    "dBlendSpaceVars": base_global_CRntSmallDictionary_base_global_CStrId__float_,
    "sSkelRootNode": PropertyEnum,
    "sExitAnim": common_types.StrId,
    "sExitAnimChannel": common_types.StrId,
    "fExitAnimFrame": common_types.Float,
    "dLayersExitAnim": base_global_CRntSmallDictionary_base_global_CStrId__CCutSceneDef_CAnimationLayerDef_,
    "sLightingDef": common_types.StrId,
})

base_global_CRntVector_CCutSceneDef_CActorDef_ = common_types.make_vector(CCutSceneDef_CActorDef)

base_global_CRntVector_base_global_CFilePathStrId_ = common_types.make_vector(common_types.StrId)

CFXPool_CDefinition = Object({
    "sFile": common_types.StrId,
    "eType": construct_EFXType,
    "uSize": common_types.UInt,
})

base_global_CRntVector_CFXPool_CDefinition_ = common_types.make_vector(CFXPool_CDefinition)

CFXPoolPack = Object({
    "lPoolDefinitions": base_global_CRntVector_CFXPool_CDefinition_,
})

CCutSceneDef = Object({
    "eDevelopmentState": construct_cutscene_EDevelopmentState,
    "sId": common_types.StrId,
    "sActionSet": common_types.StrId,
    "vWorldOffset": common_types.CVector3D,
    "sOnLoaded": common_types.StrId,
    "sOnBeforeStart": common_types.StrId,
    "sOnStart": common_types.StrId,
    "sOnFinished": common_types.StrId,
    "sOnEnd": common_types.StrId,
    "sOnSkip": common_types.StrId,
    "fCamInitInterpTime": common_types.Float,
    "fCamExitInterpTime": common_types.Float,
    "fFps": common_types.Int,
    "bSkippable": construct.Flag,
    "aTakes": base_global_CRntVector_CCutSceneDef_CTakeDef_,
    "aActors": base_global_CRntVector_CCutSceneDef_CActorDef_,
    "aSounds": base_global_CRntVector_base_global_CFilePathStrId_,
    "oPoolDefinitions": CFXPoolPack,
})

CCutSceneDefPtr = Pointer_CCutSceneDef.create_construct()

CCutscene_CActor = Object({})

base_global_CRntVector_CCutscene_CActor_ = common_types.make_vector(CCutscene_CActor)

CCutscene = Object({
    "oDefinition": CCutSceneDefPtr,
    "lstActors": base_global_CRntVector_CCutscene_CActor_,
})

CCutscene_CTunableCutscene = Object({
    **base_tunable_CTunableFields,
    "fDistanceListenerToTarget": common_types.Float,
})

base_global_CRntVector_base_math_CVector3D_ = common_types.make_vector(common_types.CVector3D)

base_global_CRntVector_bool_ = common_types.make_vector(construct.Flag)

CCutsceneComponent_SActorInfo = Object(CCutsceneComponent_SActorInfoFields := {
    "sId": common_types.StrId,
    "lnkActor": common_types.StrId,
    "bStartingVisibleState": construct.Flag,
    "bReceiveLogicUpdate": construct.Flag,
    "vctVisibilityPerTake": base_global_CRntVector_bool_,
})

base_global_CRntVector_CCutsceneComponent_SActorInfo_ = common_types.make_vector(CCutsceneComponent_SActorInfo)

std_unique_ptr_CTriggerLogicAction_ = Pointer_CTriggerLogicAction.create_construct()

base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__ = common_types.make_vector(std_unique_ptr_CTriggerLogicAction_)

CCutsceneComponent = Object({
    **CActorComponentFields,
    "sCutsceneName": common_types.StrId,
    "bDisableScenarioEntitiesOnPlay": construct.Flag,
    "vOriginalPos": common_types.CVector3D,
    "vctCutscenesOffsets": base_global_CRntVector_base_math_CVector3D_,
    "vctExtraInvolvedSubareas": base_global_CRntVector_base_global_CStrId_,
    "vctExtraInvolvedActors": base_global_CRntVector_CCutsceneComponent_SActorInfo_,
    "vctOnBeforeCutsceneStartsLA": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
    "vctOnAfterCutsceneEndsLA": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
    "bHasSamusAsExtraActor": construct.Flag,
})

CCutsceneComponent_SSamusActorInfo = Object(CCutsceneComponent_SActorInfoFields)

CCutsceneTriggerComponent = Object({
    **CBaseTriggerComponentFields,
    "lnkTargetCutsceneActor": common_types.StrId,
    "bOneShot": construct.Flag,
})

CSluggerAIComponent = Object(CSluggerAIComponentFields := CBehaviorTreeAIComponentFields)

CDaivoAIComponent = Object({
    **CSluggerAIComponentFields,
    "wpSwarmActor": common_types.StrId,
    "wpSwarmAOIBegin": common_types.StrId,
    "wpSwarmAOIEnd": common_types.StrId,
    "fChaseForcedDistanceToWall": common_types.Float,
})

CDaivoSpitAttack = Object(CAttackFields)

CSwarmControllerComponent = Object(CSwarmControllerComponentFields := {
    **CComponentFields,
    "wpPathToFollow": common_types.StrId,
    "ePathType": construct_IPath_EType,
    "fGroupVelocity": common_types.Float,
})

CFlockingSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields := CSwarmControllerComponentFields)

CRedenkiSwarmControllerComponent = Object(CRedenkiSwarmControllerComponentFields := CFlockingSwarmControllerComponentFields)

CDaivoSwarmControllerComponent = Object(CRedenkiSwarmControllerComponentFields)

CDamageComponent = Object(CComponentFields)

CDamageTriggerConfig = Object({
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CDamageTriggerComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oConfig": CDamageTriggerConfig,
})

CDeathCameraCtrl = Object(CCameraCtrlFields)

CDefaultAction = Object(CActionInstanceFields)

CDemolitionBlockLifeComponent = Object(CDemolitionBlockLifeComponentFields := {
    **CLifeComponentFields,
    "wpOtherBlock": common_types.StrId,
})

CDemolitionBlockActivatableActorLifeComponent = Object({
    **CDemolitionBlockLifeComponentFields,
    "oActivatableObjController": common_types.StrId,
})

CDemolitionBlockComponent = Object({
    **CActivatableComponentFields,
    "vObjsToEnable": base_global_CRntVector_CGameLink_CEntity__,
    "vObjsToDisable": base_global_CRntVector_CGameLink_CEntity__,
})

CDemolitionBlockSonarTargetComponent = Object(CSonarTargetComponentFields)

CDirLightComponent = Object({
    **CBaseLightComponentFields,
    "vDir": common_types.CVector3D,
    "fAnimFrame": common_types.Float,
    "bCastShadows": construct.Flag,
})

CDizzeanSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields)

CDoorLifeComponent = Object(CDoorLifeComponentFields := {
    **CItemLifeComponentFields,
    "fMaxDistanceOpened": common_types.Float,
    "wpLeftDoorShieldEntity": common_types.StrId,
    "wpRightDoorShieldEntity": common_types.StrId,
    "fMinTimeOpened": common_types.Float,
    "bStayOpen": construct.Flag,
    "bStartOpened": construct.Flag,
    "bOnBlackOutOpened": construct.Flag,
    "bDoorIsWet": construct.Flag,
    "bFrozenDuringColdown": construct.Flag,
    "iAreaLeft": common_types.Int,
    "iAreaRight": common_types.Int,
    "aVignettes": base_global_CRntVector_CGameLink_CActor__,
    "sShieldEntity": common_types.StrId,
})

CDoorCentralUnitLifeComponent = Object({
    **CDoorLifeComponentFields,
    "eMode": construct_CCentralUnitComponent_ECentralUnitMode,
})

CDoorEmmyFXComponent = Object(CComponentFields)

CDoorGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CDoorLifeComponent_CTunableDoorLifeComponent = Object({
    **base_tunable_CTunableFields,
    "fPhaseDisplacementFactorOverride": common_types.Float,
    "fOneWayDoorCloseDistance": common_types.Float,
    "fIceBlockOffSet": common_types.Float,
    "bForceAllDoorsOpened": construct.Flag,
})


class CDoorLifeComponent_SState(enum.IntEnum):
    NONE = 0
    Opened = 1
    Closed = 2
    Locked = 3
    Invalid = 2147483647


construct_CDoorLifeComponent_SState = StrictEnum(CDoorLifeComponent_SState)

CDredhedAIComponent = Object(CBehaviorTreeAIComponentFields)

CDredhedAttackComponent = Object(CAIAttackComponentFields)

CDredhedDiveAttack = Object(CAttackFields)

CDrop = Object(CGameObjectFields)

CDropComponent = Object(CComponentFields)

CDropComponent_CTunableDropComponent = Object({
    **base_tunable_CTunableFields,
    "fTimeToFade": common_types.Float,
    "bUseCrazyWeaponBoostConfiguration": construct.Flag,
    "bForceNoDrop": construct.Flag,
    "bForceXParasiteDrop": construct.Flag,
    "bForceXParasiteSelfSpawnLoop": construct.Flag,
    "bIgnoreXParasiteDrop": construct.Flag,
    "fLowHealthRuleMaxLife": common_types.Float,
    "fCriticalHealthRuleMaxLife": common_types.Float,
    "bSkipCriticalHealthRuleTakingCurrentDropsIntoAccount": construct.Flag,
    "bApplyLowHealthRuleCountingPreviousDrops": construct.Flag,
    "fXParasiteOrangeReductionOnFullPowerBombAmmo": common_types.Float,
    "fXParasiteOrangeRelativeProbabilityOnOtherResourcesFull": common_types.Float,
})

CDroppableComponent = Object(CDroppableComponentFields := {
    **CComponentFields,
    "fMaxTimeAlive": common_types.Float,
})

CDroppableComponent_CTunableDroppable = Object({
    **base_tunable_CTunableFields,
    "fSpawnSpeedFactor": common_types.Float,
    "fMaxSpawnVelocity": common_types.Float,
})

CDroppableLifeComponent = Object({
    **CDroppableComponentFields,
    "fAmount": common_types.Float,
})

CDroppableMissileComponent = Object({
    **CDroppableComponentFields,
    "sItemMax": common_types.StrId,
    "sItemCurrent": common_types.StrId,
})

CDroppablePowerBombComponent = Object({
    **CDroppableComponentFields,
    "sItemMax": common_types.StrId,
    "sItemCurrent": common_types.StrId,
})

CDroppableSpecialEnergyComponent = Object({
    **CDroppableComponentFields,
    "fAmount": common_types.Float,
})

CDropterAIComponent = Object(CBehaviorTreeAIComponentFields)

CDropterDiveAttack = Object(CAttackFields)

CDummyAIComponent = Object(CAIComponentFields)

CDummyMovement = Object(CMovementComponentFields)

CDummyPullableGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CEditorPathSegment = Object({
    "vPos": common_types.CVector3D,
})

CEditorRailSegment = Object({
    "vPos": common_types.CVector3D,
})


class CElectricGeneratorComponent_EBlackOutZone(enum.IntEnum):
    Zone1 = 0
    Zone2 = 1
    Unknown = 2
    Invalid = 2147483647


construct_CElectricGeneratorComponent_EBlackOutZone = StrictEnum(CElectricGeneratorComponent_EBlackOutZone)

CElectricGeneratorComponent = Object({
    **CUsableComponentFields,
    "eBlackOutZone": construct_CElectricGeneratorComponent_EBlackOutZone,
    "sOnEnterUseLuaCallback": common_types.StrId,
    "vAffectedSubAreas": base_global_CRntVector_base_global_CStrId_,
})

CElectricReactionComponent = Object(CElectricReactionComponentFields := CComponentFields)

CElectrifyingAreaComponent = Object({
    **CComponentFields,
    "bShouldUpdateAreaOnStart": construct.Flag,
})

CElevatorCommanderUsableComponent = Object({
    **CUsableComponentFields,
    "sTargetSpawnPoint": common_types.StrId,
})

CEmergencyLightElectricReactionComponent = Object(CElectricReactionComponentFields)

std_unique_ptr_CEmmyOverrideDeathPositionDef_ = Pointer_CEmmyOverrideDeathPositionDef.create_construct()

base_global_CRntVector_std_unique_ptr_CEmmyOverrideDeathPositionDef__ = common_types.make_vector(std_unique_ptr_CEmmyOverrideDeathPositionDef_)

std_unique_ptr_CEmmyAutoForbiddenEdgesDef_ = Pointer_CEmmyAutoForbiddenEdgesDef.create_construct()

base_global_CRntVector_std_unique_ptr_CEmmyAutoForbiddenEdgesDef__ = common_types.make_vector(std_unique_ptr_CEmmyAutoForbiddenEdgesDef_)

std_unique_ptr_CEmmyAutoGlobalSmartLinkDef_ = Pointer_CEmmyAutoGlobalSmartLinkDef.create_construct()

base_global_CRntVector_std_unique_ptr_CEmmyAutoGlobalSmartLinkDef__ = common_types.make_vector(std_unique_ptr_CEmmyAutoGlobalSmartLinkDef_)

CEmmyAIComponent = Object(CEmmyAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "sCurrentPatrol": common_types.StrId,
    "bPerceptionFeedbackEnabled": construct.Flag,
    "bShowBehaviorDebug": construct.Flag,
    "fPhaseDisplacementFactor": common_types.Float,
    "fGrabQTEFailTime": common_types.Float,
    "bPlayerNoiseEnabled": construct.Flag,
    "fPatrolSearchMaxTime": common_types.Float,
    "fGrabZoomOffset": common_types.Float,
    "fGrabZoomTime": common_types.Float,
    "bTargetDetectionEnabled": construct.Flag,
    "bTargetInsideEmmyZone": construct.Flag,
    "tOverrideGrabPosition": base_global_CRntVector_std_unique_ptr_CEmmyOverrideDeathPositionDef__,
    "tOverrideDeathPosition": base_global_CRntVector_std_unique_ptr_CEmmyOverrideDeathPositionDef__,
    "tAutoForbiddenEdges": base_global_CRntVector_std_unique_ptr_CEmmyAutoForbiddenEdgesDef__,
    "tAutoGlobalSmartLinks": base_global_CRntVector_std_unique_ptr_CEmmyAutoGlobalSmartLinkDef__,
    "tLogicShapesToAvoidCornerReposition": base_global_CRntVector_CGameLink_CActor__,
})


class EMinimapMode(enum.IntEnum):
    Never = 0
    Always = 1
    Patrol2Search = 2
    ChaseAndSearchRange = 3
    Search = 4
    AlwaysExceptPatrol = 5
    Invalid = 2147483647


construct_EMinimapMode = StrictEnum(EMinimapMode)


class EIceMode(enum.IntEnum):
    Mode1 = 0
    Mode2 = 1
    Invalid = 2147483647


construct_EIceMode = StrictEnum(EIceMode)

CEmmyAIComponent_CTunableEmmyAIComponent = Object({
    **base_tunable_CTunableFields,
    "eEmmyOutsideRoomLPF": construct_base_snd_ELowPassFilter,
    "eMinimapMode": construct_EMinimapMode,
    "eIceMode": construct_EIceMode,
    "fChaseUnspawnEnemyDistance": common_types.Float,
    "bCloseEmmyDoorsDuringChase": construct.Flag,
    "fEmmyAutoFocusStartTime": common_types.Float,
    "fEmmyAutoFocusEndTime": common_types.Float,
    "fEmmyAutoFocusMaxZoomDistance": common_types.Float,
    "fFocusModeActivationRadius": common_types.Float,
    "fEmmyZoneChasePulseWaitTime": common_types.Float,
    "fEmmyZoneChasePulseSpeed": common_types.Float,
    "fEmmyZoneChasePhase2PulseWaitTime": common_types.Float,
    "fEmmyZoneChasePhase2PulseSpeed": common_types.Float,
    "fEmmyZoneSearch2PulseWaitTime": common_types.Float,
    "fEmmyZoneSearch2PulseSpeed": common_types.Float,
    "eEmmyOutsideRoomLowPassFilter": common_types.Int,
    "bEmmyOutsideRoomLowPassActive": construct.Flag,
    "bAfterGrabGotoSearch": construct.Flag,
    "fGrab2Probability": common_types.Float,
    "fTimeTargetOutOfEmmyZoneToEndSearch": common_types.Float,
    "bWantsChaseRedLight": construct.Flag,
    "fTunnelWalkTransitionSpeedChasePhase1": common_types.Float,
    "fTunnelWalkTransitionSpeedChasePhase2ProtectorOn": common_types.Float,
    "fTunnelWalkTransitionSpeedChasePhase2ProtectorDestroyed": common_types.Float,
    "bDarknessEnabled": construct.Flag,
    "iMinimapMode": common_types.Int,
    "fMinimapPatrol2SearchTime": common_types.Float,
    "bWaveInSearch": construct.Flag,
    "bWaveInChase": construct.Flag,
    "bWaveInWater": construct.Flag,
    "bWaveInPhase2ProtectorOn": construct.Flag,
    "bWaveInfiniteDetectionRadius": construct.Flag,
    "fWaveTimeBetweenFire": common_types.Float,
    "fWaveChargeTime": common_types.Float,
    "bWaveMaxRadiusToFireDebug": construct.Flag,
    "fWaveMaxRadiusToFire": common_types.Float,
    "fWaveTimeSinceWaveReactionToFire": common_types.Float,
    "bWaveShowFireFeedback": construct.Flag,
    "fWaveProjectileInitialRadius": common_types.Float,
    "fWaveProjectileRadius": common_types.Float,
    "fWaveIgnoreInputTime": common_types.Float,
    "fWaveProjectileSpeed": common_types.Float,
    "fWaveProjectileWaterSpeed": common_types.Float,
    "fWaveMinAtt": common_types.Float,
    "fWaveMaxAtt": common_types.Float,
    "fWaveMinTimeInSpaceJumpToFire": common_types.Float,
    "fWaveMaxTimeInSpaceJumpToFire": common_types.Float,
    "fWaveInSpaceJumpFireProjectileMaxSpeed": common_types.Float,
    "bIceUseInPatrol": construct.Flag,
    "bIceUseInWater": construct.Flag,
    "bIceInfiniteDetectionRadius": construct.Flag,
    "fIceIceConeRadius": common_types.Float,
    "fIceIceConeAperture": common_types.Float,
    "fIceIceConeChargeTime": common_types.Float,
    "fIceTimeBetweenFire": common_types.Float,
    "fIceIgnoreInputTimeMax": common_types.Float,
    "fIceIgnoreInputTimeMin": common_types.Float,
    "fTimeSearchForcedToGoAway": common_types.Float,
    "fTimeSearchForcedToGoAwayInSearch": common_types.Float,
    "fStaggerTimeGrab": common_types.Float,
    "fStaggerTimeHeadProtectorDestroyed": common_types.Float,
    "fStaggerTimeGrabTuto": common_types.Float,
    "bUseTurnsWithoutStopAndLook": construct.Flag,
    "bAlwaysWinQTE1": construct.Flag,
    "fCentralUnitAlarmVolumeOnGrab": common_types.Float,
    "fTimeInFrustumToMarkEmmySeen": common_types.Float,
})


class CEmmyAIComponent_ETargetPerceptionType(enum.IntEnum):
    NONE = 0
    Indirect = 1
    Direct = 2
    Invalid = 2147483647


construct_CEmmyAIComponent_ETargetPerceptionType = StrictEnum(CEmmyAIComponent_ETargetPerceptionType)

CEmmyAttackComponent = Object(CAIAttackComponentFields)

CEmmyAutoForbiddenEdgesDef = Object({
    "wpCheckSamusLogicShape": common_types.StrId,
    "wpCheckEmmyLogicShape": common_types.StrId,
    "tForbiddenLogicShapes": base_global_CRntVector_CGameLink_CActor__,
    "tWeightedLogicShapeIDs": base_global_CRntVector_base_global_CStrId_,
})

CEmmyAutoGlobalSmartLinkDef = Object({
    "wpStartLandmark": common_types.StrId,
    "tEndLandmarks": base_global_CRntVector_CGameLink_CActor__,
    "wpActivateLogicShape": common_types.StrId,
})

CEmmyCaveAIComponent = Object(CEmmyAIComponentFields)

CEmmyFloorSlideCameraCtrl = Object(CCameraCtrlFields)

CEmmyForestAIComponent = Object(CEmmyAIComponentFields)

CEmmyGrabSamusAttack = Object(CAttackFields)

CEmmyLabAIComponent = Object(CEmmyAIComponentFields)

CEmmyMagmaAIComponent = Object(CEmmyAIComponentFields)

CEnemyMovement = Object(CEnemyMovementFields := CCharacterMovementFields)

CEmmyMovement = Object(CEnemyMovementFields)

CEmmyOverrideDeathPositionDef = Object({
    "wpLandmark": common_types.StrId,
    "wpLogicShape": common_types.StrId,
})

CEmmyProtoAIComponent = Object({
    **CEmmyAIComponentFields,
    "sDirtMaterialConstantId": common_types.StrId,
})

CEmmySancAIComponent = Object({
    **CEmmyAIComponentFields,
    "tFast4LegTransformationMagnet": base_global_CRntVector_CGameLink_CActor__,
    "wpForceEmmyPerceptionVisionConeOffShape": common_types.StrId,
    "bZipLine004Behavior": construct.Flag,
    "wpPhase2HeatEnabledLogicShape": common_types.StrId,
})

CEmmyShipyardAIComponent = Object(CEmmyAIComponentFields)

CEmmySpawnPointComponent = Object(CSpawnPointComponentFields)


class CEmmyStateOverrideLogicAction_EMode(enum.IntEnum):
    ShowVisualCone = 0
    HideVisualCone = 1
    Invalid = 2147483647


construct_CEmmyStateOverrideLogicAction_EMode = StrictEnum(CEmmyStateOverrideLogicAction_EMode)

CEmmyStateOverrideLogicAction = Object({
    **CTriggerLogicActionFields,
    "eMode": construct_CEmmyStateOverrideLogicAction_EMode,
})

CEmmyValveComponent = Object(CComponentFields)

CEventPropComponent = Object(CEventPropComponentFields := CComponentFields)

CEmmyWakeUpComponent = Object({
    **CEventPropComponentFields,
    "wpCentralUnit": common_types.StrId,
})

CEmmyWaveMovementComponent = Object(CProjectileMovementFields)

CEnemyLifeComponent_CTunableEnemyLifeComponent = Object({
    **base_tunable_CTunableFields,
    "bEnemiesLifeLocked": construct.Flag,
    "fOverrideDamage": common_types.Float,
})

CEnemyPreset = Object({
    "sId": common_types.StrId,
    "fLife": common_types.Float,
    "sLifeTunable": common_types.StrId,
    "sLifeTunableVar": common_types.StrId,
})

CEnhanceWeakSpotComponent = Object(CEnhanceWeakSpotComponentFields := CComponentFields)

base_spatial_CAABox = Object({
    "Min": common_types.CVector3D,
    "Max": common_types.CVector3D,
})

CEntity = Object({
    **CActorFields,
    "oBBox": base_spatial_CAABox,
    "bIsInFrustum": construct.Flag,
})

CEnvironmentData_SFogPtr = Pointer_CEnvironmentData_SFog.create_construct()

CEnvironmentData_SVerticalFogPtr = Pointer_CEnvironmentData_SVerticalFog.create_construct()

base_global_CRntVector_CEnvironmentData_SFogTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_.create_construct()

CEnvironmentData_SAmbientPtr = Pointer_CEnvironmentData_SAmbient.create_construct()

base_global_CRntVector_CEnvironmentData_SAmbientTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_.create_construct()

CEnvironmentData_SDepthTintPtr = Pointer_CEnvironmentData_SDepthTint.create_construct()

base_global_CRntVector_CEnvironmentData_SDepthTintTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_.create_construct()

CEnvironmentData_SMaterialTintPtr = Pointer_CEnvironmentData_SMaterialTint.create_construct()

base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_.create_construct()

CEnvironmentData_SPlayerLightPtr = Pointer_CEnvironmentData_SPlayerLight.create_construct()

base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_.create_construct()

CEnvironmentData_SHemisphericalLightPtr = Pointer_CEnvironmentData_SHemisphericalLight.create_construct()

base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_.create_construct()

CEnvironmentData_SBloomPtr = Pointer_CEnvironmentData_SBloom.create_construct()

base_global_CRntVector_CEnvironmentData_SBloomTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_.create_construct()

base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_.create_construct()

CEnvironmentData_SCubeMapPtr = Pointer_CEnvironmentData_SCubeMap.create_construct()

base_global_CRntVector_CEnvironmentData_SCubeMapTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_.create_construct()

CEnvironmentData_SSSAOPtr = Pointer_CEnvironmentData_SSSAO.create_construct()

base_global_CRntVector_CEnvironmentData_SSSAOTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_.create_construct()

CEnvironmentData_SToneMappingPtr = Pointer_CEnvironmentData_SToneMapping.create_construct()

base_global_CRntVector_CEnvironmentData_SToneMappingTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_.create_construct()

CEnvironmentData_SIBLAttenuationPtr = Pointer_CEnvironmentData_SIBLAttenuation.create_construct()

base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_Ptr = Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_.create_construct()

CEnvironmentData = Object({
    "sID": common_types.StrId,
    "tFog": CEnvironmentData_SFogPtr,
    "tVerticalFog": CEnvironmentData_SVerticalFogPtr,
    "tFogTransitions": base_global_CRntVector_CEnvironmentData_SFogTransition_Ptr,
    "tAmbient": CEnvironmentData_SAmbientPtr,
    "tAmbientTransitions": base_global_CRntVector_CEnvironmentData_SAmbientTransition_Ptr,
    "tDepthTint": CEnvironmentData_SDepthTintPtr,
    "tDepthTintTransitions": base_global_CRntVector_CEnvironmentData_SDepthTintTransition_Ptr,
    "tMaterialTint": CEnvironmentData_SMaterialTintPtr,
    "tMaterialTintTransitions": base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_Ptr,
    "tPlayerLight": CEnvironmentData_SPlayerLightPtr,
    "tPlayerLightTransitions": base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_Ptr,
    "tHemisphericalLight": CEnvironmentData_SHemisphericalLightPtr,
    "tHemisphericalLightTransitions": base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_Ptr,
    "tBloom": CEnvironmentData_SBloomPtr,
    "tBloomTransitions": base_global_CRntVector_CEnvironmentData_SBloomTransition_Ptr,
    "tVerticalFogTransitions": base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_Ptr,
    "tCubeMap": CEnvironmentData_SCubeMapPtr,
    "tCubeMapTransitions": base_global_CRntVector_CEnvironmentData_SCubeMapTransition_Ptr,
    "tSSAO": CEnvironmentData_SSSAOPtr,
    "tSSAOTransitions": base_global_CRntVector_CEnvironmentData_SSSAOTransition_Ptr,
    "tToneMapping": CEnvironmentData_SToneMappingPtr,
    "tToneMappingTransitions": base_global_CRntVector_CEnvironmentData_SToneMappingTransition_Ptr,
    "tIBLAttenuation": CEnvironmentData_SIBLAttenuationPtr,
    "tIBLAttenuationTransitions": base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_Ptr,
})

CEnvironmentData_SAmbient = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
})

STransition = Object(STransitionFields := {})

CEnvironmentData_SAmbientTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
})

CEnvironmentData_SBloom = Object({
    "tBloom": common_types.CVector3D,
    "fBloomInterp": common_types.Float,
})

CEnvironmentData_SBloomTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fBloomInterp": common_types.Float,
})

CEnvironmentData_SCubeMap = Object({
    "fInterp": common_types.Float,
    "bEnabled": construct.Flag,
    "sTexturePath": common_types.StrId,
})

CEnvironmentData_SCubeMapTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fCubeMapInterp": common_types.Float,
})

CEnvironmentData_SDepthTint = Object({
    "fTintInterp": common_types.Float,
    "fLight": common_types.Float,
    "fCube": common_types.Float,
    "fDepth": common_types.Float,
    "fSaturation": common_types.Float,
    "fLightNear": common_types.Float,
    "fCubeNear": common_types.Float,
    "fDepthNear": common_types.Float,
    "fSaturationNear": common_types.Float,
})

CEnvironmentData_SDepthTintTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fTintInterp": common_types.Float,
})

CEnvironmentData_SFog = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fScale": common_types.Float,
    "fScaleInterp": common_types.Float,
    "tRange": common_types.CVector2D,
    "fRangeInterp": common_types.Float,
    "fWaveFreq": common_types.Float,
    "fWaveAmp": common_types.Float,
    "fWaveVelocity": common_types.Float,
    "fWaveInterp": common_types.Float,
})

CEnvironmentData_SFogTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fScaleInterp": common_types.Float,
    "fRangeInterp": common_types.Float,
    "fWaveInterp": common_types.Float,
})

CEnvironmentData_SHemisphericalLight = Object({
    "tColorUp": common_types.CVector3D,
    "fColorUpInterp": common_types.Float,
    "tColorDown": common_types.CVector3D,
    "fColorDownInterp": common_types.Float,
})

CEnvironmentData_SHemisphericalLightTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorUpInterp": common_types.Float,
    "fColorDownInterp": common_types.Float,
})

CEnvironmentData_SIBLAttenuation = Object({
    "fInterp": common_types.Float,
    "fCubeAttFactor": common_types.Float,
    "fZDistance": common_types.Float,
    "fGradientSize": common_types.Float,
})

CEnvironmentData_SIBLAttenuationTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

CEnvironmentData_SMaterialTint = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fBlend": common_types.Float,
    "fBlendInterp": common_types.Float,
})

CEnvironmentData_SMaterialTintTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fBlendInterp": common_types.Float,
})

CEnvironmentData_SPlayerLight = Object({
    "tDiffuse": common_types.CVector4D,
    "tSpecular0": common_types.CVector4D,
    "tSpecular1": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "tAttenuation": common_types.CVector2D,
    "fAttenuationInterp": common_types.Float,
})

CEnvironmentData_SPlayerLightTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fAttenuationInterp": common_types.Float,
})

CEnvironmentData_SSSAO = Object({
    "fFallOff": common_types.Float,
    "fIntensity": common_types.Float,
    "fBias": common_types.Float,
    "fRadius": common_types.Float,
    "fDepthFct": common_types.Float,
    "bEnabled": construct.Flag,
    "fInterp": common_types.Float,
    "fIntensityFactor": common_types.Float,
    "fFogFactor": common_types.Float,
})

CEnvironmentData_SSSAOTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

CEnvironmentData_SToneMapping = Object({
    "fInterp": common_types.Float,
    "fExposure": common_types.Float,
    "fGamma": common_types.Float,
    "fSaturationColor": common_types.Float,
    "fContrast": common_types.Float,
    "fBrightness": common_types.Float,
    "vColorTint": common_types.CVector4D,
    "fColorVibrance": common_types.Float,
    "bEnabled": construct.Flag,
})

CEnvironmentData_SToneMappingTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

CEnvironmentData_SVerticalFog = Object({
    "bEnabled": construct.Flag,
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fBase": common_types.Float,
    "fBaseInterp": common_types.Float,
    "tAttenuation": common_types.CVector2D,
    "fAttInterp": common_types.Float,
    "fNear": common_types.Float,
    "fNearInterp": common_types.Float,
    "fFar": common_types.Float,
    "fFarInterp": common_types.Float,
    "fWaveFreq": common_types.Float,
    "fWaveAmp": common_types.Float,
    "fWaveVelocity": common_types.Float,
    "fWaveInterp": common_types.Float,
})

CEnvironmentData_SVerticalFogTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fBaseInterp": common_types.Float,
    "fNearInterp": common_types.Float,
    "fFarInterp": common_types.Float,
    "fAttInterp": common_types.Float,
    "fWaveInterp": common_types.Float,
})

CEnvironmentVisualPresetsPtr = Pointer_CEnvironmentVisualPresets.create_construct()

CEnvironmentSoundPresetsPtr = Pointer_CEnvironmentSoundPresets.create_construct()

CEnvironmentMusicPresetsPtr = Pointer_CEnvironmentMusicPresets.create_construct()

CEnvironmentManager = Object({
    "pVisualPresets": CEnvironmentVisualPresetsPtr,
    "pSoundPresets": CEnvironmentSoundPresetsPtr,
    "pMusicPresets": CEnvironmentMusicPresetsPtr,
})

CEnvironmentManagerPtr = Pointer_CEnvironmentManager.create_construct()

sound_TMusicFile = Object({
    "sWav": common_types.StrId,
    "iLoops": common_types.Int,
    "iLoopStart": common_types.Int,
    "iLoopEnd": common_types.Int,
})

base_global_CRntVector_sound_TMusicFile_ = common_types.make_vector(sound_TMusicFile)

sound_TMusicTrack = Object({
    "iTrack": common_types.Int,
    "vFiles": base_global_CRntVector_sound_TMusicFile_,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "fDelay": common_types.Float,
    "fVol": common_types.Float,
    "iStartPos": common_types.Int,
    "eCrossFade": construct_EMusicFadeType,
    "bPauseOnPop": construct.Flag,
    "fEnvFactor": common_types.Float,
})

base_global_CRntVector_sound_TMusicTrack_ = common_types.make_vector(sound_TMusicTrack)

sound_TScenarioMusicPreset = Object({
    "sAlias": common_types.StrId,
    "vTracks": base_global_CRntVector_sound_TMusicTrack_,
})


class SMusicPlayFlag(enum.IntEnum):
    NONE = 0
    FORCE = 1
    CLEAR_STACKS = 2
    CLEAR_TRACKS = 3
    POP_CURRENT = 4
    PAUSE_CURRENT = 5
    IGNORE_PAUSE = 6
    SKIP_TO_LOOP = 7
    PAUSE_ON_POP = 8
    Invalid = 2147483647


construct_SMusicPlayFlag = StrictEnum(SMusicPlayFlag)

CEnvironmentMusicData_SMusicTransition = Object({
    "sPreset": common_types.StrId,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "eFadeType": construct_EMusicFadeType,
    "ePlayFlag": construct_SMusicPlayFlag,
})

base_global_CRntVector_CEnvironmentMusicData_SMusicTransition_ = common_types.make_vector(CEnvironmentMusicData_SMusicTransition)

CEnvironmentMusicData = Object({
    "sID": common_types.StrId,
    "tPreset": sound_TScenarioMusicPreset,
    "ePlayFlag": construct_SMusicPlayFlag,
    "tMusicTransitions": base_global_CRntVector_CEnvironmentMusicData_SMusicTransition_,
})

base_global_CRntDictionary_base_global_CStrId__CEnvironmentMusicData_ = common_types.make_dict(CEnvironmentMusicData, key=common_types.StrId)

sound_SStateFadeOut = Object({
    "eState": construct_EMusicManagerInGameState,
    "fFadeOut": common_types.Float,
})

base_global_CRntVector_sound_SStateFadeOut_ = common_types.make_vector(sound_SStateFadeOut)

sound_TBossMusicTrack = Object({
    "oTrack": sound_TMusicTrack,
    "vFadeOuts": base_global_CRntVector_sound_SStateFadeOut_,
})

base_global_CRntVector_sound_TBossMusicTrack_ = common_types.make_vector(sound_TBossMusicTrack)

sound_TBossMusicSubStateConfig = Object({
    "eState": common_types.StrId,
    "vTracks": base_global_CRntVector_sound_TBossMusicTrack_,
})

base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicSubStateConfig_ = common_types.make_dict(sound_TBossMusicSubStateConfig, key=common_types.StrId)

sound_TBossMusicSpawnGroupConfig = Object({
    "sSpawnGroup": common_types.StrId,
    "dicSubStatePresets": base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicSubStateConfig_,
})

base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicSpawnGroupConfig_ = common_types.make_dict(sound_TBossMusicSpawnGroupConfig, key=common_types.StrId)

sound_TBossMusicPreset = Object({
    "sBoss": common_types.StrId,
    "dicSpawnGroupConfigs": base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicSpawnGroupConfig_,
})

base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicPreset_ = common_types.make_dict(sound_TBossMusicPreset, key=common_types.StrId)

CEnvironmentMusicPresets = Object({
    "dicPresets": base_global_CRntDictionary_base_global_CStrId__CEnvironmentMusicData_,
    "dicBossPresets": base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicPreset_,
})

CEnvironmentSoundData_SSound = Object({
    "sToPreset": common_types.StrId,
    "fVolume": common_types.Float,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "fFadeInDelay": common_types.Float,
    "eReverb": construct_base_snd_EReverbIntensity,
})

base_global_CRntDictionary_base_global_CStrId__CEnvironmentSoundData_SSound_ = common_types.make_dict(CEnvironmentSoundData_SSound, key=common_types.StrId)

CEnvironmentSoundData = Object({
    "sID": common_types.StrId,
    "sSoundID": common_types.StrId,
    "tSound": CEnvironmentSoundData_SSound,
    "dctTransitions": base_global_CRntDictionary_base_global_CStrId__CEnvironmentSoundData_SSound_,
})

base_global_CRntDictionary_base_global_CStrId__CEnvironmentSoundData_ = common_types.make_dict(CEnvironmentSoundData, key=common_types.StrId)

CEnvironmentSoundPresets = Object({
    "dicPresets": base_global_CRntDictionary_base_global_CStrId__CEnvironmentSoundData_,
})

base_global_CRntDictionary_base_global_CStrId__CEnvironmentData_ = common_types.make_dict(CEnvironmentData, key=common_types.StrId)

CEnvironmentVisualPresets = Object({
    "dicPresets": base_global_CRntDictionary_base_global_CStrId__CEnvironmentData_,
})

CEscapeSequenceExplosionComponent = Object(CComponentFields)

CEvacuationCountDown = Object({
    **CEventPropComponentFields,
    "vEntitiesToPowerOff": base_global_CRntVector_CGameLink_CEntity__,
})

CEvacuationCountDown_CTunableEvacuationCountDown = Object({
    **base_tunable_CTunableFields,
    "fRumbleMinGain": common_types.Float,
    "fRumbleMaxGain": common_types.Float,
    "sRumbleEasingFunction": common_types.StrId,
    "fEscapeSequenceMaxTime": common_types.Float,
    "fCameraShakeMinShakeDist": common_types.Float,
    "fCameraShakeMaxShakeDist": common_types.Float,
    "sShakeEasingFunction": common_types.StrId,
    "fPercentActivationAmbientFXSoft": common_types.Float,
    "fPercentActivationAmbientFXMedium": common_types.Float,
    "fPercentActivationAmbientFXHard": common_types.Float,
    "iTimeToBlinkEvery10s": common_types.Int,
    "iTimeToBlinkEvery5s": common_types.Int,
    "iTimeToBlinkEverysecond": common_types.Int,
    "fMinInterPulseTime": common_types.Float,
    "fMaxInterPulseTime": common_types.Float,
    "sInterPulseTimeEasingFunction": common_types.StrId,
    "fMinPulseSpeed": common_types.Float,
    "fMaxPulseSpeed": common_types.Float,
    "sPulseSpeedEasingFunction": common_types.StrId,
    "fMinBaseColor": common_types.Float,
    "fMaxBaseColor": common_types.Float,
    "sBaseColorEasingFunction": common_types.StrId,
    "fMinEmberFlyingPercentage": common_types.Float,
    "fMaxEmberFlyingPercentage": common_types.Float,
    "sEmberFyingEasingFunction": common_types.StrId,
})

CEventScenarioComponent = Object({
    **CComponentFields,
    "vEventActors": base_global_CRntVector_CGameLink_CActor__,
    "sIdleAction": common_types.StrId,
    "sReactionAction": common_types.StrId,
    "sFinishedAction": common_types.StrId,
    "sRecoveryAction": common_types.StrId,
    "bPersistent": construct.Flag,
    "bDisableOnXParasite": construct.Flag,
    "bDisableOnCoolDown": construct.Flag,
    "bReactOnFireOnly": construct.Flag,
    "bReactOnEnemies": construct.Flag,
    "bReactToSamus": construct.Flag,
    "bIgnoreSamusWithOC": construct.Flag,
    "bReactToSamusFiring": construct.Flag,
    "bReactToFireImpact": construct.Flag,
    "fTimeForRecoveryOnStay": common_types.Float,
    "fTimeForRecoveryOnExit": common_types.Float,
    "fInitRelaxFrame": common_types.Float,
})


class CExplosionGfx_ETransitionOperationMode(enum.IntEnum):
    NONE = 0
    RGBA = 1
    RGB = 2
    A = 3
    End = 4
    Invalid = 2147483647


construct_CExplosionGfx_ETransitionOperationMode = StrictEnum(CExplosionGfx_ETransitionOperationMode)

CExplosionGfx = Object({
    "fLength": common_types.Float,
    "sParticlesPath": common_types.StrId,
    "sAdditionalParticlesPath": common_types.StrId,
    "sMeshPath": common_types.StrId,
    "fMainExplosionScale": common_types.Float,
    "vRandomScale": common_types.CVector2D,
    "uAmount": common_types.UInt,
    "fRadius": common_types.Float,
    "fRadiusAmplitude": common_types.Float,
    "fRandomArcAmplitude": common_types.Float,
    "vRandomDelay": common_types.CVector2D,
    "oConstantColor0TransitionInit": common_types.CVector4D,
    "oConstantColor0TransitionEnd": common_types.CVector4D,
    "eConstant0TransitionMode": construct_CExplosionGfx_ETransitionOperationMode,
    "fConstantColor0TransitionTime": common_types.Float,
    "oConstantColor1TransitionInit": common_types.CVector4D,
    "oConstantColor1TransitionEnd": common_types.CVector4D,
    "eConstant1TransitionMode": construct_CExplosionGfx_ETransitionOperationMode,
    "fConstantColor1TransitionTime": common_types.Float,
})

CFXComponent = Object({
    **CSceneComponentFields,
    "fSelectedHighRadius": common_types.Float,
    "fSelectedLowRadius": common_types.Float,
})

CFactionComponent = Object(CComponentFields)

CFadeScreenTrack = Object({
    **base_global_timeline_CTrackFields,
    "vColorStart": base_color_CColor4B_SRGB,
    "vColorEnd": base_color_CColor4B_SRGB,
})

CFakePhysicsMovement = Object(CMovementComponentFields)

CFanComponent = Object({
    **CBaseTriggerComponentFields,
    "fWindLength": common_types.Float,
    "fHurricaneLength": common_types.Float,
    "fBarrierLength": common_types.Float,
    "fWidth": common_types.Float,
    "fParticleScale": common_types.Float,
})

CFanCoolDownComponent = Object(CComponentFields)

CFingSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields)

CFireComponent = Object(CComponentFields)

CFixedCameraCtrl = Object(CCameraCtrlFields)

CFloatingPropActingComponent = Object(CComponentFields)

CShockWaveComponent = Object(CShockWaveComponentFields := CComponentFields)

CFloorShockWaveComponent = Object(CShockWaveComponentFields)

CFootstepPlatformComponent = Object({
    **CComponentFields,
    "wpActivableEntity": common_types.StrId,
    "wpPartnerFootStepPlatformEntity": common_types.StrId,
    "sCallbackOnOpened": common_types.StrId,
    "sCallbackOnClosed": common_types.StrId,
})


class navmesh_ENavMeshGroup(enum.IntEnum):
    DEFAULT = 0
    EMMY = 1
    EMMY_PROTO = 2
    EMMY_CAVE = 3
    EMMY_MAGMA = 4
    Invalid = 2147483647


construct_navmesh_ENavMeshGroup = StrictEnum(navmesh_ENavMeshGroup)


class CForbiddenEdgesLogicAction_EState(enum.IntEnum):
    Allowed = 0
    Forbidden = 1
    Invalid = 2147483647


construct_CForbiddenEdgesLogicAction_EState = StrictEnum(CForbiddenEdgesLogicAction_EState)

CForbiddenEdgesLogicAction = Object({
    **CTriggerLogicActionFields,
    "eNavMeshGroup": construct_navmesh_ENavMeshGroup,
    "wpSpawnPoint": common_types.StrId,
    "wpLogicShape": common_types.StrId,
    "eState": construct_CForbiddenEdgesLogicAction_EState,
})

CForceMovementLogicAction = Object({
    **CTriggerLogicActionFields,
    "bMovePlayer": construct.Flag,
    "v2Direction": common_types.CVector2D,
})


class CForcedMovementAreaComponent_EForcedDirection(enum.IntEnum):
    NONE = 0
    Right = 1
    Left = 2
    Invalid = 2147483647


construct_CForcedMovementAreaComponent_EForcedDirection = StrictEnum(CForcedMovementAreaComponent_EForcedDirection)

CForcedMovementAreaComponent = Object({
    **CActorComponentFields,
    "bForcedAreaOnce": construct.Flag,
    "eForcedDirection": construct_CForcedMovementAreaComponent_EForcedDirection,
})

CFreeAimTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpItemToDestroy": common_types.StrId,
})

CFreeCameraCtrl = Object(CCameraCtrlFields)

CFreezeRoomConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CFreezeRoomCoolConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CFreezeRoomComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oFreezeConfig": CFreezeRoomConfig,
    "oCoolConfig": CFreezeRoomCoolConfig,
    "sEnterZoneSound": common_types.StrId,
    "sVisualPresetOverride": common_types.StrId,
})

CFrozenComponent = Object(CFrozenComponentFields := CComponentFields)

CFrozenAsFrostbiteComponent = Object(CFrozenComponentFields)

CFrozenAsFrostbiteComponent_CTunableFrozenAsFrostbiteComponent = Object({
    **base_tunable_CTunableFields,
    "fFrostbiteColorR": common_types.Float,
    "fFrostbiteColorG": common_types.Float,
    "fFrostbiteColorB": common_types.Float,
    "fFrostbiteColorMinA": common_types.Float,
    "fFrostbiteColorMaxA": common_types.Float,
})

CFrozenAsPlatformComponent = Object(CFrozenComponentFields)

CFrozenComponent_CTunableFrozenComponent = Object({
    **base_tunable_CTunableFields,
    "bInfiniteFrozenTime": construct.Flag,
})

CFrozenPlatformComponent = Object({
    **CComponentFields,
    "wpWeightPlatform": common_types.StrId,
})

CFulmiteBellyMineAIComponent = Object(CBehaviorTreeAIComponentFields)

CFulmiteBellyMineAttackComponent = Object(CAIAttackComponentFields)

CFulmiteBellyMineMovementComponent = Object(CProjectileMovementFields)

CFusibleBoxComponent = Object(CComponentFields)

CGameBlackboard_TPropDeltaValues = base_global_CRntSmallDictionary_base_global_CStrId__float_

base_global_CRntSmallDictionary__base_global_CStrId__CGameBlackboard_TPropDeltaValues__ = common_types.make_dict(CGameBlackboard_TPropDeltaValues, key=common_types.StrId)

CGameBlackboard = Object({
    **CBlackboardFields,
    "dctDeltaValues": base_global_CRntSmallDictionary__base_global_CStrId__CGameBlackboard_TPropDeltaValues__,
})

CGameLink_CLogicCamera_ = Object({})

CGameManager_CTunableEnemies = Object(base_tunable_CTunableFields)

CGameManager_CTunableGameManager = Object({
    **base_tunable_CTunableFields,
    "iConfigMode": common_types.Int,
    "bForceHardMode": construct.Flag,
    "bPlayerPosDebug": construct.Flag,
    "bSamusCenterPointDebug": construct.Flag,
    "bCheatDetectedDebug": construct.Flag,
})

CGameManager_CTunableGraphicSettings = Object(base_tunable_CTunableFields)

CGameManager_CTunableMusicVolume = Object({
    **base_tunable_CTunableFields,
    "fVolumeInMenu": common_types.Float,
})

CGameObjectRef_CLogicCamera_ = Pointer_CLogicCamera.create_construct()


class EEntryType(enum.IntEnum):
    ML_INFO_ENTRY = 0
    ML_DIALOGUE_ENTRY = 1
    ML_TUTO_ENTRY = 2
    Invalid = 2147483647


construct_EEntryType = StrictEnum(EEntryType)

CGlobalEventManager_SMissionLogEntry = Object({
    "eEntryType": construct_EEntryType,
    "sLabelText": common_types.StrId,
    "vCaptionsIds": base_global_CRntVector_base_global_CStrId_,
})

CGobblerAIComponent = Object(CBehaviorTreeAIComponentFields)

CGobblerBiteAttack = Object(CAttackFields)

CGobblerSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "wpDoor": common_types.StrId,
    "wpWeb": common_types.StrId,
})

CGoliathAIComponent = Object(CGoliathAIComponentFields := CBaseBigFistAIComponentFields)

CGoliathAttack = Object(CGoliathAttackFields := CAttackFields)


class CGoliathAttack_EGoliathAttackState(enum.IntEnum):
    NONE = 0
    Started = 1
    PostAttackLoop = 2
    Recovering = 3
    Invalid = 2147483647


construct_CGoliathAttack_EGoliathAttackState = StrictEnum(CGoliathAttack_EGoliathAttackState)

CGoliathXAIComponent = Object({
    **CGoliathAIComponentFields,
    "wpCoreXSpawnPoint": common_types.StrId,
})

CGoliathXBurstProjectionBombMovement = Object(CBombMovementFields)

CGoliathXBurstProjectionBombsAttack = Object(CAttackFields)

CGoliathXSlamAttack = Object(CGoliathAttackFields)

CGooplotAIComponent = Object(CGooplotAIComponentFields := CBehaviorTreeAIComponentFields)

CGooplotJumpAttack = Object(CGooplotJumpAttackFields := CAttackFields)

CGooplotUndoJumpAttack = Object(CGooplotJumpAttackFields)

CGooshockerAIComponent = Object(CGooplotAIComponentFields)


class CGrabComponent_ELinkMode(enum.IntEnum):
    NONE = 0
    RootToDC_Grab = 1
    FeetToRoot = 2
    Invalid = 2147483647


construct_CGrabComponent_ELinkMode = StrictEnum(CGrabComponent_ELinkMode)

CGrabComponent = Object({
    **CComponentFields,
    "bIsInGrab": construct.Flag,
    "eLinkModeAsGrabber": construct_CGrabComponent_ELinkMode,
})

CGrappleBeamComponent = Object({
    **CWeaponMovementFields,
    "sIniFXId": common_types.StrId,
    "sEndFXId": common_types.StrId,
    "sGrappleFX": common_types.StrId,
})

CGrappleBeamComponent_CTunableGrappleBeamComponent = Object({
    **base_tunable_CTunableFields,
    "fAdvanceSpeed": common_types.Float,
    "fRetractSpeed": common_types.Float,
    "fMaxLength": common_types.Float,
    "fMaxLengthToStartRetract": common_types.Float,
})

CGrappleBeamGun = Object(CPrimaryGunFields)

CGrappleBeamGun_CTunableGrappleBeamGun = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fHeat": common_types.Float,
    "iSelectionMode": common_types.Int,
    "iSelectionInput": common_types.Int,
})


class CGrappleBeamGun_ESelectionInput(enum.IntEnum):
    LS = 0
    ZR = 1
    RS = 2
    Invalid = 4294967295


construct_CGrappleBeamGun_ESelectionInput = StrictEnum(CGrappleBeamGun_ESelectionInput)


class CGrappleBeamGun_ESelectionMode(enum.IntEnum):
    AIM_AUTOMATIC = 0
    AIM_AUTOMATIC_DESELECT_HOLDING_INPUT = 1
    AIM_MANUAL_SELECT_HOLDING_INPUT = 2
    NO_AIM_SELECT_HOLDING_INPUT = 3
    NO_AIM_TOGGLE_PRESSING_INPUT = 4
    Invalid = 4294967295


construct_CGrappleBeamGun_ESelectionMode = StrictEnum(CGrappleBeamGun_ESelectionMode)

CGroundShockerAIComponent = Object(CBaseGroundShockerAIComponentFields)

CGroundShockerAttack = Object(CAttackFields)


class CGroundShockerAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    Start2Init = 2
    InitLoop = 3
    Init2Hit = 4
    HitLoop = 5
    Aborting = 6
    End = 7
    Invalid = 2147483647


construct_CGroundShockerAttack_EState = StrictEnum(CGroundShockerAttack_EState)

CGun_CTunableGun = Object({
    **base_tunable_CTunableFields,
    "fCheckBackDefaultDistance": common_types.Float,
    "fCheckBackAnalogDistance": common_types.Float,
    "fCheckBackAnalogFallDistance": common_types.Float,
    "fCheckBackHangDistance": common_types.Float,
    "fTimeHitMissedModifierDuration": common_types.Float,
    "fVolumeHitMissedModifier": common_types.Float,
})

CGunComponent = Object(CGunComponentFields := CComponentFields)

CGunComponent_CTunableGunComponent = Object({
    **base_tunable_CTunableFields,
    "fPowerBombMinTimeToStartCharge": common_types.Float,
    "fNormalFireChargeMinTime": common_types.Float,
    "fNormalFireChargeMaxTime": common_types.Float,
    "fSPBFireChargeMinTime": common_types.Float,
    "fSPBFireChargeMaxTime": common_types.Float,
    "fDiffusionFireChargeMinTime": common_types.Float,
    "fDiffusionFireChargeMaxTime": common_types.Float,
    "fIgnoreFireAfterChargeReleasedTime": common_types.Float,
})

CHangableGrappleSurfaceComponent = Object(CHangableGrappleSurfaceComponentFields := CGrapplePointComponentFields)

CHangableGrappleMagnetSlidingBlockComponent = Object(CHangableGrappleSurfaceComponentFields)

CHangableGrapplePointComponent = Object(CGrapplePointComponentFields)

CSensor = Object(CSensorFields := {})

CHearingSensor = Object(CSensorFields)

CStimulusDef = Object(CStimulusDefFields := {
    "sId": common_types.StrId,
    "fMaxRange": common_types.Float,
    "fMaxTTL": common_types.Float,
})

CHearingStimulusDef = Object(CStimulusDefFields)

CHeatRoomConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "bActivationDelayTimeOnlyForFirstTime": construct.Flag,
})

CHeatRoomCoolConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "bActivationDelayTimeOnlyForFirstTime": construct.Flag,
})

CHeatRoomComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oHeatConfig": CHeatRoomConfig,
    "oCoolConfig": CHeatRoomCoolConfig,
    "sEnterZoneSound": common_types.StrId,
    "sVisualPresetOverride": common_types.StrId,
    "pEnvironmentFXActor": common_types.StrId,
    "vEnvironmentFXActors": base_global_CRntVector_CGameLink_CActor__,
})

CHeatableShieldComponent = Object(CComponentFields)

CHeatableShieldComponent_CTunableHeatableShield = Object({
    **base_tunable_CTunableFields,
    "sFunction": common_types.StrId,
    "fHeatRecoveredPerSecond": common_types.Float,
    "fTimeToStartHeatRecover": common_types.Float,
    "fHeatIncrementFactor": common_types.Float,
    "fMaxRGBColor": common_types.Float,
    "fStartEmmitingParticlesOnHeat": common_types.Float,
    "fStopEmmitingParticlesOnCooldown": common_types.Float,
})

CHeatableShieldEnhanceWeakSpotComponent = Object(CEnhanceWeakSpotComponentFields)

CHecathonAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "wpPatrolPath": common_types.StrId,
    "ePatrolPathType": construct_IPath_EType,
    "wpHarassPath": common_types.StrId,
    "eHarassPathType": construct_IPath_EType,
    "fTimeToGoPatrol": common_types.Float,
    "fSpeed": common_types.Float,
    "bIsEating": construct.Flag,
    "bCanEat": construct.Flag,
    "fPatrolEatDuration": common_types.Float,
    "fPatrolEatCooldown": common_types.Float,
    "uMask": common_types.UInt,
})

CHecathonLifeComponent = Object(CEnemyLifeComponentFields)

CHecathonPlanktonFXComponent = Object({
    **CSceneComponentFields,
    "sModelResPath": common_types.StrId,
})

CHoldPlayerDirectionOnSubAreaChangeLogicAction = Object({
    **CTriggerLogicActionFields,
    "bForce": construct.Flag,
})

CHomingMovement = Object(CProjectileMovementFields)

CHydrogigaAIComponent = Object({
    **CBossAIComponentFields,
    "wpPresentationCutscenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CHydrogigaAttack = Object(CHydrogigaAttackFields := CAttackFields)

CHydrogigaBraidAttack = Object(CHydrogigaAttackFields)

CHydrogigaGrabCameraCtrl = Object(CCameraCtrlFields)

CHydrogigaMaelstormAttack = Object(CHydrogigaAttackFields)

CHydrogigaPolypsAttack = Object(CHydrogigaAttackFields)

CHydrogigaTentacleBashAttack = Object(CHydrogigaAttackFields)

CHydrogigaTongueSwirlAttack = Object(CHydrogigaAttackFields)

CMagnetSlidingBlockComponent = Object(CMagnetSlidingBlockComponentFields := {
    **CComponentFields,
    "fTimePreparingToOpen": common_types.Float,
    "fTimeToCompleteMovementTowardsEnd": common_types.Float,
    "fTimeToCompleteMovementTowardsStart": common_types.Float,
    "bContinueMovingOnStopHang": construct.Flag,
    "wpRail": common_types.StrId,
    "wpDoorOpeningOnAnimatedCamera": common_types.StrId,
    "fTotalMetersToMoveY": common_types.Float,
    "fTimeToOpen": common_types.Float,
    "bAutoOpenAfterPreparing": construct.Flag,
})

CHydrogigaZiplineComponent = Object({
    **CMagnetSlidingBlockComponentFields,
    "lstLinkedMagnetSlidingBlocks": base_global_CRntVector_CGameLink_CEntity__,
})

CHydrogigaZiplineRailComponent = Object({
    **CComponentFields,
    "lstAttachedZiplines": base_global_CRntVector_CGameLink_CEntity__,
})

CHyperBeamBlockLifeComponent = Object(CItemLifeComponentFields)

CHyperBeamGun = Object(CBeamGunFields)

CHyperBeamGun_CTunableHyperBeam = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fMaximumHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
    "fSlowDownFactor": common_types.Float,
    "fFirstTimeChargeTime": common_types.Float,
    "fSingleFireChargeTime": common_types.Float,
    "fRepeatedlyFireChargeTime": common_types.Float,
    "fInterruptFireChargeTime": common_types.Float,
})

CSecondaryGun = Object(CSecondaryGunFields := CGunFields)

CMissileBaseGun = Object(CMissileBaseGunFields := CSecondaryGunFields)

CMissileGun = Object(CMissileGunFields := CMissileBaseGunFields)

CIceMissileGun = Object(CMissileGunFields)

CIceMissileGun_CTunableIceMissile = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fHeat": common_types.Float,
})

CMissileMovement = Object(CMissileMovementFields := {
    **CProjectileMovementFields,
    "sTrailFX": common_types.StrId,
    "sBurstFX": common_types.StrId,
    "sIgnitionFX": common_types.StrId,
    "sSPRNoDamageFX": common_types.StrId,
})

CIceMissileMovement = Object(CMissileMovementFields)

CIgnoreFloorSlideUpperBodySubmergedLogicAction = Object({
    **CTriggerLogicActionFields,
    "bActive": construct.Flag,
    "sId": common_types.StrId,
})

CInfesterAIComponent = Object(CBehaviorTreeAIComponentFields)

CInfesterBallAIComponent = Object(CBehaviorTreeAIComponentFields)

CInfesterBallAttackComponent = Object(CAIAttackComponentFields)

CInfesterBallLifeComponent = Object(CEnemyLifeComponentFields)

CInfesterBallMovementComponent = Object(CProjectileMovementFields)

CInfesterReloadAttack = Object(CAttackFields)

CInfesterShootAttack = Object(CAttackFields)


class CInfesterShootAttack_EState(enum.IntEnum):
    NONE = 0
    ShootState = 1
    End = 2
    Invalid = 2147483647


construct_CInfesterShootAttack_EState = StrictEnum(CInfesterShootAttack_EState)

CInputComponent = Object({
    **CComponentFields,
    "bInputIgnored": construct.Flag,
})

CInputComponent_CTunableInputComponent = Object({
    **base_tunable_CTunableFields,
    "iWalkInputMode": common_types.Int,
    "fNoWalkMusicVolume": common_types.Float,
    "fWalkMusicVolume": common_types.Float,
    "fNoWalkEnvironmentVolume": common_types.Float,
    "fWalkEnvironmentVolume": common_types.Float,
    "fWalkSamusMovementVolume": common_types.Float,
    "bWalkEmmySoundReverb": construct.Flag,
    "iInputPreset": common_types.Int,
})

CInterpolationComponent = Object(CComponentFields)

CInventoryComponent = Object(CComponentFields)

CInventoryComponent_CTunableInventoryComponent = Object({
    **base_tunable_CTunableFields,
    "iMaxNumMissiles": common_types.Int,
})

CItemDestructionLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpItemToDestroy": common_types.StrId,
    "wpObserver": common_types.StrId,
})

CKraidAIComponent = Object({
    **CBossAIComponentFields,
    "wpStage1ArenaShape": common_types.StrId,
    "wpStage2ArenaShape": common_types.StrId,
    "wpPhase2CutScenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
    "wpDeadFromZiplineOrMBCutscenePlayer": common_types.StrId,
})

CKraidAttack = Object(CKraidAttackFields := CAttackFields)

CKraidAcidBlobsAttack = Object(CKraidAttackFields)

CKraidAcidBlobsMovementComponent = Object(CProjectileMovementFields)

CKraidBackSlapAttack = Object(CKraidAttackFields)

CKraidBouncingCreaturesAttack = Object(CKraidAttackFields)

CKraidBouncingCreaturesMovementComponent = Object(CProjectileMovementFields)

CKraidFierceSwipeAttack = Object(CKraidAttackFields)

CKraidFlyingSpikesAttack = Object(CKraidAttackFields)

CKraidNailMovementComponent = Object(CProjectileMovementFields)

CKraidShockerSplashAttack = Object(CKraidAttackFields)

CKraidShockerSplashMovementComponent = Object(CProjectileMovementFields)

CMovablePlatformComponent = Object(CMovablePlatformComponentFields := CMovementComponentFields)

CKraidSpikeMovablePlatformComponent = Object(CMovablePlatformComponentFields)

CKraidSpinningNailsAttack = Object(CKraidAttackFields)


class ESpinningNailsState(enum.IntEnum):
    init = 0
    nail1 = 1
    nail2 = 2
    nail3 = 3
    nail4 = 4
    end = 5
    Invalid = 2147483647


construct_ESpinningNailsState = StrictEnum(ESpinningNailsState)


class ESpinningNailsSpeed(enum.IntEnum):
    fast = 0
    medium = 1
    slow = 2
    Invalid = 2147483647


construct_ESpinningNailsSpeed = StrictEnum(ESpinningNailsSpeed)

CKraidSpinningNailsDef = Object({
    "eState": construct_ESpinningNailsState,
    "eSpeed": construct_ESpinningNailsSpeed,
    "fAngle": common_types.Float,
})

CKraidTripleFlyingSpikesAttack = Object(CKraidAttackFields)

CLandmarkComponent = Object({
    **CActorComponentFields,
    "sLandmarkID": common_types.StrId,
})

CLanguageManager = Object({})

CLiquidPoolBaseComponent = Object(CLiquidPoolBaseComponentFields := {
    **CBaseDamageTriggerComponentFields,
    "sModelPath": common_types.StrId,
    "eLowPassFilter": construct_base_snd_ELowPassFilter,
    "eReverb": construct_base_snd_EReverbIntensity,
})

CLavaPoolConfig = Object({
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CLavaPoolComponent = Object({
    **CLiquidPoolBaseComponentFields,
    "oConfig": CLavaPoolConfig,
    "fChangeTime": common_types.Float,
})

CLavaPumpComponent = Object(CActivatableComponentFields)

CLavaPumpComponent_CTunableLavaPumpComponent = Object({
    **base_tunable_CTunableFields,
    "fInitialPlayRate": common_types.Float,
    "fActivationTime": common_types.Float,
})

CThermalReactionComponent = Object(CThermalReactionComponentFields := CComponentFields)

CLavapumpThermalReactionComponent = Object(CThermalReactionComponentFields)

CLifeRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})


class ELightType(enum.IntEnum):
    Directional = 0
    Omni = 1
    Spot = 2
    Seg = 3
    Invalid = 4294967295


construct_ELightType = StrictEnum(ELightType)


class ELightAttachment(enum.IntEnum):
    PosRot3D = 0
    Pos3D = 1
    Rot3D = 2
    PosRot2D = 3
    Pos2D = 4
    Rot2D = 5
    Invalid = 4294967295


construct_ELightAttachment = StrictEnum(ELightAttachment)

CLightInfo = Object({
    "eType": construct_ELightType,
    "eAttachment": construct_ELightAttachment,
    "sName": common_types.StrId,
    "sNode": common_types.StrId,
    "vPosOffset": common_types.CVector3D,
    "vRotOffset": common_types.CVector3D,
    "vColor": common_types.CVector4D,
    "vAtt": common_types.CVector4D,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
    "fIntensity": common_types.Float,
    "bCastShadows": construct.Flag,
    "bUseSpecular": construct.Flag,
    "bEnabled": construct.Flag,
})

base_global_CRntVector_CLightInfo_ = common_types.make_vector(CLightInfo)

CLightsDef = Object({
    **base_core_CAssetFields,
    "sPath": common_types.StrId,
    "vLights": base_global_CRntVector_CLightInfo_,
})

base_global_CRntDictionary_base_global_CFilePathStrId__CLightsDef_ = common_types.make_dict(CLightsDef, key=common_types.StrId)

CLightManager = Object({
    "dicLightDefs": base_global_CRntDictionary_base_global_CFilePathStrId__CLightsDef_,
})

CLightManagerPtr = Pointer_CLightManager.create_construct()

CLightingComponent = Object(CComponentFields)

CLineBombGun = Object(CSecondaryGunFields)

CLineBombGun_CTunableLineBomb = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "sDamageSource": common_types.StrId,
    "fHeat": common_types.Float,
})

CLineBombMovement = Object(CBombMovementFields)

CLineBombMovement_CTunableLineBombMovement = Object({
    **base_tunable_CTunableFields,
    "fExplosionRadius": common_types.Float,
    "fExplosionExpansionTime": common_types.Float,
    "fExplosionLifeTime": common_types.Float,
    "fCheckDistance": common_types.Float,
    "bSingleHit": construct.Flag,
    "bEachBombImpulsesPlayer": construct.Flag,
    "bStickyBomb": construct.Flag,
    "bOrientateToClosestSurfaceNormal": construct.Flag,
})

CLiquidSimulationComponent = Object(CComponentFields)

CLockOnMissileGun = Object(CMissileBaseGunFields)

CLockOnMissileGun_CTunableLockOnMissile = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "sDamageSource": common_types.StrId,
    "iMissilesPerShot": common_types.Int,
    "fHeat": common_types.Float,
    "bSwarmMode": construct.Flag,
    "bMachineGunMode": construct.Flag,
})

CLockOnMissileMovement = Object(CMissileMovementFields)

CLockOnMissileMovement_CTunableLockOnMissileMovement = Object({
    **base_tunable_CTunableFields,
    "vTrailColor": common_types.CVector3D,
    "fStabalizingSpeed": common_types.Float,
    "fSteeringSpeed": common_types.Float,
    "fStabalizingDistance": common_types.Float,
    "fEdgeCrossingDistance": common_types.Float,
    "fFromEdgeMaxDistance": common_types.Float,
    "fNoiseAmplitude": common_types.Float,
    "fNoiseFrequency": common_types.Float,
    "fDistanceFromScenario": common_types.Float,
    "fDistanceFromPath": common_types.Float,
    "fTrailVerticalSize": common_types.Float,
    "fTrailVerticalOffset": common_types.Float,
    "fTrailLength": common_types.Float,
    "bSwarmMovement": construct.Flag,
    "bTextureCycling": construct.Flag,
})


class CLockOnMissileMovement_SSubState(enum.IntEnum):
    NONE = 0
    Pooled = 1
    Traking = 2
    Invalid = 2147483647


construct_CLockOnMissileMovement_SSubState = StrictEnum(CLockOnMissileMovement_SSubState)

CLockRoomLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpAccessPoint": common_types.StrId,
    "sDoorsLockedLiteralID": common_types.StrId,
    "bInstantLock": construct.Flag,
})

CLogicActionTriggerComponent = Object({
    **CComponentFields,
    "vLogicActions": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
})

CLogicCamera = Object({
    **CGameObjectFields,
    "sID": common_types.StrId,
    "sControllerID": common_types.StrId,
    "bStatic": construct.Flag,
    "v3Position": common_types.CVector3D,
    "v3Dir": common_types.CVector3D,
    "fFovX": common_types.Float,
    "fMinExtraZDist": common_types.Float,
    "fMaxExtraZDist": common_types.Float,
    "fDefaultInterp": common_types.Float,
})

CLogicCameraComponent = Object({
    **CActorComponentFields,
    "rLogicCamera": CGameObjectRef_CLogicCamera_,
})

CLogicDroppedItemManager_CTunableDroppableBillboard = Object({
    **base_tunable_CTunableFields,
    "fSpawnSpeedFactor": common_types.Float,
    "fMaxSpawnVelocity": common_types.Float,
    "fMaxTimeAlive": common_types.Float,
    "fMiniXMaxTimeAlive": common_types.Float,
    "fTimeToStartBlinking": common_types.Float,
    "fMiniXTimeToStartBlinking": common_types.Float,
    "fBlinkPeriod": common_types.Float,
    "fMaxSqrDistanceToAbsorb": common_types.Float,
    "fLifeAmount": common_types.Float,
    "fLifeBigAmount": common_types.Float,
    "fMissileAmount": common_types.Float,
    "fMissileBigAmount": common_types.Float,
    "fPowerBombAmount": common_types.Float,
    "fPowerBombBigAmount": common_types.Float,
    "fMiniXLifeAmount": common_types.Float,
    "fMiniXMissileAmount": common_types.Float,
    "fTimeSpawning": common_types.Float,
    "fTimeSpawningMelee": common_types.Float,
    "fTimeToBeCollectible": common_types.Float,
    "fDropsRelaxMovementSize": common_types.Float,
    "iDropsRelaxMovementAnimationFrames": common_types.Int,
    "bDropsDoRelaxMovement": construct.Flag,
    "bAbsorbDissolvingPickables": construct.Flag,
    "fDefaultAttractionDistanceCm": common_types.Float,
    "fMiniXAttractionDistanceCm": common_types.Float,
    "fMiniXGreenMotionScale": common_types.Float,
    "fMiniXYellowMotionScale": common_types.Float,
    "fMiniXScaleMinFactor": common_types.Float,
    "fMiniXScaleMaxFactor": common_types.Float,
    "fMiniXScaleFrequency": common_types.Float,
    "uMiniXSmallGroupMaxSize": common_types.UInt,
    "uMiniXMediumGroupMaxSize": common_types.UInt,
    "sMiniXAbsorbSmallGroupPresetName": common_types.StrId,
    "sMiniXAbsorbMediumGroupPresetName": common_types.StrId,
    "sMiniXAbsorbLargeGroupPresetName": common_types.StrId,
    "sMiniXFlyPresetName": common_types.StrId,
    "bMissileBigDeprecated": construct.Flag,
    "bPowerBombBigDeprecated": construct.Flag,
    "sDropAbsorbLifePresetName": common_types.StrId,
    "sDropAbsorbLifeBigPresetName": common_types.StrId,
    "sDropAbsorbMissilePresetName": common_types.StrId,
    "sDropAbsorbPowerBombPresetName": common_types.StrId,
    "sAbsorbingSoundPresetName": common_types.StrId,
})

CLogicLookAtPlayerComponent = Object(CComponentFields)

SLogicPathNode = Object({
    **IPathNodeFields,
    "vPos": common_types.CVector3D,
    "fSwarmRadius": common_types.Float,
    "fDiversionChance": common_types.Float,
})

base_global_CRntVector_SLogicPathNode_ = common_types.make_vector(SLogicPathNode)

SLogicSubPath = Object({
    **ISubPathFields,
    "tNodes": base_global_CRntVector_SLogicPathNode_,
})

base_global_CRntVector_SLogicSubPath_ = common_types.make_vector(SLogicSubPath)

SLogicPath = Object({
    **IPathFields,
    "tSubPaths": base_global_CRntVector_SLogicSubPath_,
})

CLogicPathComponent = Object({
    **CActorComponentFields,
    "logicPath": SLogicPath,
})

CLogicPathNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CLogicPathNavMeshItemStage = Object(CNavMeshItemStageFields)

CLuaCallsLogicAction = Object({
    **CTriggerLogicActionFields,
    "sCallbackEntityName": common_types.StrId,
    "sCallback": common_types.StrId,
    "bCallbackEntity": construct.Flag,
    "bCallbackPersistent": construct.Flag,
})

CLuaLibraryManager = Object({})

CMagmaCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CMagmaCentralUnitComponentDef = Object(CCentralUnitComponentDefFields)

CMagmaKraidPistonPlatformComponent = Object(CComponentFields)

CMagmaKraidScenarioControllerComponent = Object({
    **CComponentFields,
    "wpBackGorundPipesEntity": common_types.StrId,
    "wpPistonEntity": common_types.StrId,
})

CMagmaKraidSpikeComponent = Object(CComponentFields)

CMagnetMovablePlatformComponent = Object(CMagnetMovablePlatformComponentFields := CMovablePlatformComponentFields)

CMagnetSlidingBlockCounterWeightMovablePlatformComponent = Object({
    **CMagnetMovablePlatformComponentFields,
    "wpReferenceEntity": common_types.StrId,
})

CMagnetSlidingBlockRailComponent = Object(CComponentFields)

CMagnetSlidingBlockWithCollisionsComponent = Object(CMagnetSlidingBlockComponentFields)

CMagnetSurfaceComponent = Object(CActorComponentFields)

CMagnetSurfaceHuskComponent = Object(CComponentFields)

CMapAcquisitionComponent = Object({
    **CUsableComponentFields,
    "sLiteralID": common_types.StrId,
})

CMassiveCaterzillaSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "fTimeToSpawn": common_types.Float,
    "fTimeToSpawnAfterDespawn": common_types.Float,
    "iNumCaterzillas": common_types.Int,
})

CMaterialFXComponent = Object(CSceneComponentFields)

CSynchronizedBlockCameraCtrl = Object(CSynchronizedBlockCameraCtrlFields := CCameraBoundaryCtrlFields)

CMeleeCameraCtrl = Object(CSynchronizedBlockCameraCtrlFields)

CMeleeComponent = Object({
    **CComponentFields,
    "sBlockSyncFX": common_types.StrId,
})

CMenuAnimationChangeComponent = Object(CComponentFields)

CMetroidCameraCtrl = Object(CCameraBoundaryCtrlFields)

CMetroidCameraCtrl_CTunableMetroidCameraCtrl = Object({
    **base_tunable_CTunableFields,
    "fZoomMinDistCamZ": common_types.Float,
    "fZoomMaxDistCamZ": common_types.Float,
    "fZoomMinCamDistToApplyOffsetX": common_types.Float,
    "fEmmyPhase1ChaseMinEmmyDist": common_types.Float,
    "fEmmyPhase1ChaseMaxEmmyDist": common_types.Float,
    "fEmmyPhase1ChaseMinEmmyDistCamZ": common_types.Float,
    "fEmmyPhase1ChaseMaxEmmyDistCamZ": common_types.Float,
    "fEmmyPhase1NoChaseMinEmmyDist": common_types.Float,
    "fEmmyPhase1NoChaseMaxEmmyDist": common_types.Float,
    "fEmmyPhase1NoChaseMinEmmyDistCamZ": common_types.Float,
    "fEmmyPhase1NoChaseMaxEmmyDistCamZ": common_types.Float,
    "fEmmyPhase2MinEmmyDist": common_types.Float,
    "fEmmyPhase2MaxEmmyDist": common_types.Float,
    "fEmmyPhase2MinEmmyDistCamZ": common_types.Float,
    "fEmmyPhase2MaxEmmyDistCamZ": common_types.Float,
    "fEmmyDistanceZoomWalkDefault": common_types.Float,
    "fEmmyDistanceZoomWalkMinEmmyDist": common_types.Float,
    "fEmmyDistanceZoomWalkMaxEmmyDist": common_types.Float,
    "fEmmyDistanceZoomWalkMinEmmyDistCamZ": common_types.Float,
    "fEmmyDistanceZoomWalkMaxEmmyDistCamZ": common_types.Float,
    "fEmmyDistanceZoomWalkOCStoppedCamZ": common_types.Float,
    "fEmmyDistanceZoomWalkOCStoppedCamMaxOffsetX": common_types.Float,
    "fEmmyDistanceZoomWalkDisableAutoFocusEmmyExtraDistance": common_types.Float,
    "fEmmyDistanceZoomWalkAutoFocusDistCamZ": common_types.Float,
})

base_global_CRntVector_unsigned_ = common_types.make_vector(common_types.UInt)

CMinimapGrid_SGridDef = Object({
    "sScenarioId": common_types.StrId,
    "vGridMin": common_types.CVector2D,
    "vGridMax": common_types.CVector2D,
    "aGridCellBlocks": base_global_CRntVector_unsigned_,
})

base_global_CRntVector_unsigned_short_ = common_types.make_vector(construct.Int16ul)

SGeoData = Object({
    "aVertex": base_global_CRntVector_base_math_CVector3D_,
    "aIndex": base_global_CRntVector_unsigned_short_,
})

base_global_CRntVector_SGeoData_ = common_types.make_vector(SGeoData)

base_global_CRntSmallDictionary_uint64__SGeoData_ = common_types.make_dict(SGeoData, key=construct.Int64ul)

CMinimapData_TColliderGeoDatasMap = base_global_CRntSmallDictionary_uint64__SGeoData_

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_TColliderGeoDatasMap_ = common_types.make_dict(CMinimapData_TColliderGeoDatasMap, key=common_types.StrId)

base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_ = common_types.make_dict(SGeoData, key=common_types.StrId)

base_spatial_SSegmentData = Object({
    "vPos": common_types.CVector3D,
})

base_global_CRntVector_base_spatial_SSegmentData_ = common_types.make_vector(base_spatial_SSegmentData)

base_spatial_CPolygon2D = Object({
    "bClosed": construct.Flag,
    "oSegmentData": base_global_CRntVector_base_spatial_SSegmentData_,
    "bOutwardsNormal": construct.Flag,
})

CMinimapData_SMagnetSurfaceData = Object({
    "oPolyLine": base_spatial_CPolygon2D,
})

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SMagnetSurfaceData_ = common_types.make_dict(CMinimapData_SMagnetSurfaceData, key=common_types.StrId)

CMinimapData_SMovingMagnetSurfaceData = Object({
    "sMoveEntityID": common_types.StrId,
    "iEntityType": common_types.Int,
    "oPathLine": SLogicSubPath,
    "bInverseNormal": construct.Flag,
    "fSurfaceLenght": common_types.Float,
    "vSurfaceStart": common_types.CVector2D,
    "vSurfaceEnd": common_types.CVector2D,
})

base_global_CRntVector_CMinimapData_SMovingMagnetSurfaceData_ = common_types.make_vector(CMinimapData_SMovingMagnetSurfaceData)

CMinimapData_STransportSignData = Object({
    "vPathStart": common_types.CVector2D,
    "vPathEnd": common_types.CVector2D,
    "sDestAreaId": common_types.StrId,
    "fZOffset": common_types.Float,
})

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_STransportSignData_ = common_types.make_dict(CMinimapData_STransportSignData, key=common_types.StrId)

base_spatial_CAABox2D = Object({
    "Min": common_types.CVector2D,
    "Max": common_types.CVector2D,
})

CMinimapData_SDoorData = Object({
    "vPos": common_types.CVector2D,
    "oBoxL": base_spatial_CAABox2D,
    "oBoxR": base_spatial_CAABox2D,
    "sLeftIconId": common_types.StrId,
    "sRightIconId": common_types.StrId,
    "aRoomIds": base_global_CRntVector_base_global_CStrId_,
    "sRoomId": common_types.StrId,
})

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SDoorData_ = common_types.make_dict(CMinimapData_SDoorData, key=common_types.StrId)

CMinimapData_SEntityData = Object({
    "vPos": common_types.CVector2D,
    "oBox": base_spatial_CAABox2D,
    "sIconId": common_types.StrId,
    "bFlipX": construct.Flag,
    "bFlipY": construct.Flag,
})

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_ = common_types.make_dict(CMinimapData_SEntityData, key=common_types.StrId)

CMinimapData_TOccludedIcons = base_global_CRntVector_base_global_CStrId_

base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_TOccludedIcons_ = common_types.make_dict(CMinimapData_TOccludedIcons, key=common_types.StrId)

CMinimapData = Object({
    **base_core_CAssetFields,
    "uDataVersion": common_types.UInt,
    "gridDef": CMinimapGrid_SGridDef,
    "aNavmeshGeos": base_global_CRntVector_SGeoData_,
    "mapOccluderGeos": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_TColliderGeoDatasMap_,
    "oEmmyRoomGeo": SGeoData,
    "mapEmmyRoomGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapHeatRoomGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapFreezeRoomGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapNoFreezeRoomGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapVignetteGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapHintGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapWaterPoolGeos": base_global_CRntSmallDictionary_base_global_CStrId__SGeoData_,
    "mapMagnetSurfaces": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SMagnetSurfaceData_,
    "aMovingMagnetSurfaces": base_global_CRntVector_CMinimapData_SMovingMagnetSurfaceData_,
    "mapTransportSigns": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_STransportSignData_,
    "mapDoors": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SDoorData_,
    "mapBlockages": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapUsables": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapItems": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapProps": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapCentralUnits": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapBosses": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_SEntityData_,
    "mapBossBattleLabels": base_global_CRntSmallDictionary_base_global_CStrId__base_global_CStrId_,
    "mapAbilityLabels": base_global_CRntSmallDictionary_base_global_CStrId__base_global_CStrId_,
    "mapVignetteOccludedIcons": base_global_CRntSmallDictionary_base_global_CStrId__CMinimapData_TOccludedIcons_,
})

CMinimapData_SGeneratorData = Object({
    "vPos": common_types.CVector2D,
    "aConnectedActors": base_global_CRntVector_base_global_CStrId_,
})

S9PatchConfig = Object({
    "fBorderT": common_types.Float,
    "fBorderD": common_types.Float,
    "fBorderL": common_types.Float,
    "fBorderR": common_types.Float,
})

SMapIconDef = Object({
    "uSpriteRow": common_types.UInt,
    "uSpriteCol": common_types.UInt,
    "sDisabledIconId": common_types.StrId,
    "sInspectorLabel": common_types.StrId,
    "sFemaleGenreLangs": common_types.StrId,
    "vAnchorOffset": common_types.CVector2D,
    "bAutoScale": construct.Flag,
    "bIsGlobal": construct.Flag,
    "bFullZoomScale": construct.Flag,
    "o9PatchConfig": S9PatchConfig,
})

base_global_CRntDictionary_base_global_CStrId__SMapIconDef_ = common_types.make_dict(SMapIconDef, key=common_types.StrId)

CMinimapDef_TMapIconDefs = base_global_CRntDictionary_base_global_CStrId__SMapIconDef_

SMapLabelDef = Object({
    "vPos": common_types.CVector2D,
    "vSize": common_types.CVector2D,
})

base_global_CRntDictionary_base_global_CStrId__SMapLabelDef_ = common_types.make_dict(SMapLabelDef, key=common_types.StrId)

CMinimapDef_TMapLabelDefs = base_global_CRntDictionary_base_global_CStrId__SMapLabelDef_

CMinimapDef = Object({
    **base_core_CDefinitionFields,
    "oMinimapIconsMatLink": common_types.StrId,
    "oIconsNoMipsMatLink": common_types.StrId,
    "oOverlayMatLink": common_types.StrId,
    "mapIconDefs": CMinimapDef_TMapIconDefs,
    "mapLabelDefs": CMinimapDef_TMapLabelDefs,
})


class EMinimapFowType(enum.IntEnum):
    CAMERA = 0
    CIRCLE = 1
    CLAMP_CIRCLE = 2
    Invalid = 2147483647


construct_EMinimapFowType = StrictEnum(EMinimapFowType)

CMinimapManager = Object({
    "eFOWType": construct_EMinimapFowType,
    "fFOWRadius": common_types.Float,
    "fFOWCellFadeTime": common_types.Float,
    "bFOWShowUnvisited": construct.Flag,
    "vViewPos": common_types.CVector2D,
    "fViewScale": common_types.Float,
    "fViewAlpha": common_types.Float,
    "fViewZoom": common_types.Float,
    "bAutoFadeEnabled": construct.Flag,
    "bMinimapExEnabled": construct.Flag,
    "bMinimapExPanning": construct.Flag,
})

CMinimapManager_CTunableMinimapManager = Object({
    **base_tunable_CTunableFields,
    "vOccluderColor": common_types.CVector3D,
    "vDefaultBorderColor": common_types.CVector3D,
    "vUnexploredBorderColor": common_types.CVector3D,
    "vNormalRoomColor": common_types.CVector3D,
    "vSpecialRoomColor": common_types.CVector3D,
    "vTransportRoomColor": common_types.CVector3D,
    "vDefaultColor": common_types.CVector3D,
    "vCooldownColor": common_types.CVector3D,
    "vCameraLimitsColor": common_types.CVector3D,
    "vHighlightColor": common_types.CVector3D,
    "vHighlightUnlockedColor": common_types.CVector3D,
    "vEmmyColor": common_types.CVector3D,
    "vEmmyDeadColor": common_types.CVector3D,
    "vEmmyZoneClosedColor": common_types.CVector3D,
    "vHeatColor": common_types.CVector3D,
    "vCooldownHeatColor": common_types.CVector3D,
    "vWaterColor": common_types.CVector3D,
    "vColdColor": common_types.CVector3D,
    "vLavaColor": common_types.CVector3D,
    "vDoorColor": common_types.CVector3D,
    "vBossColor": common_types.CVector3D,
    "vMagnetSurfaceColor": common_types.CVector3D,
    "vTileColorPowerbeam": common_types.CVector3D,
    "vTileColorBomb": common_types.CVector3D,
    "vTileColorMissile": common_types.CVector3D,
    "vTileColorSupermissile": common_types.CVector3D,
    "vTileColorPowerbomb": common_types.CVector3D,
    "vTileColorScrewattack": common_types.CVector3D,
    "vTileColorWeight": common_types.CVector3D,
    "vTileColorSpeedboost": common_types.CVector3D,
    "vMarkerColorA": common_types.CVector3D,
    "vMarkerColorB": common_types.CVector3D,
    "vMarkerColorC": common_types.CVector3D,
    "vMarkerColorD": common_types.CVector3D,
    "vMarkerColorE": common_types.CVector3D,
    "vColorRED": common_types.CVector3D,
    "vColorPURPLE": common_types.CVector3D,
    "vColorYELLOW": common_types.CVector3D,
    "vColorGREEN": common_types.CVector3D,
    "vColorDARKBLUE": common_types.CVector3D,
    "vColorBLUE": common_types.CVector3D,
    "vColorORANGE": common_types.CVector3D,
    "vColorPINK": common_types.CVector3D,
    "vCaveColor": common_types.CVector3D,
    "vMagmaColor": common_types.CVector3D,
    "vLabColor": common_types.CVector3D,
    "vAquaColor": common_types.CVector3D,
    "vForestColor": common_types.CVector3D,
    "vQuarantineColor": common_types.CVector3D,
    "vSanctuaryColor": common_types.CVector3D,
    "vShipyardColor": common_types.CVector3D,
    "vSkyColor": common_types.CVector3D,
    "fMinimapViewAlpha": common_types.Float,
    "fMinimapViewZoom": common_types.Float,
    "fAreaMapSnapVelMult": common_types.Float,
    "fAreaMapMoveVel": common_types.Float,
    "fAreaMapFastMoveVel": common_types.Float,
    "fAreaMapZoomMin": common_types.Float,
    "fAreaMapZoomMax": common_types.Float,
    "fAreaMapZoomDefault": common_types.Float,
    "fAreaMapZoomVel": common_types.Float,
    "bAutoFadeEnabled": construct.Flag,
})

CMinimapManager_SAreaIconInfo = Object({
    "sIconID": common_types.StrId,
    "vIconPos": common_types.CVector2D,
})


class EMarkerType(enum.IntEnum):
    MARKER_A = 0
    MARKER_B = 1
    MARKER_C = 2
    MARKER_D = 3
    MARKER_E = 4
    MARKER_F = 5
    MARKER_G = 6
    MARKER_H = 7
    MARKER_I = 8
    Invalid = 2147483647


construct_EMarkerType = StrictEnum(EMarkerType)

CMinimapManager_SMarkerData = Object({
    "nMarkerID": common_types.Int,
    "eType": construct_EMarkerType,
    "vPos": common_types.CVector2D,
    "sTargetID": common_types.StrId,
    "nTargetSlot": common_types.Int,
})

CMissileBaseGun_CTunableSPR = Object({
    **base_tunable_CTunableFields,
    "fHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
})

CMissileGun_CTunableMissile = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fHeat": common_types.Float,
    "fTimeInInitialSpeedInGrab": common_types.Float,
    "fTimeToReachSpeedInGrab": common_types.Float,
    "fRateOfFireInGrab": common_types.Float,
})

CModelInstanceComponent = Object({
    **CSceneComponentFields,
    "sModelPath": common_types.StrId,
    "vScale": common_types.CVector3D,
})

CModelUpdaterComponent = Object(CModelUpdaterComponentFields := {
    **CSceneComponentFields,
    "sDefaultModelPath": common_types.StrId,
})

CMorphBallLauncherComponent = Object({
    **CComponentFields,
    "wpLauncherExit": common_types.StrId,
    "sTravellingAction": common_types.StrId,
    "bManualActivation": construct.Flag,
})

CMorphBallLauncherExitComponent = Object({
    **CComponentFields,
    "vExpelDirection": common_types.CVector2D,
    "fExpelImpulseSize": common_types.Float,
    "fInputIgnoreTimeAfterExpelling": common_types.Float,
    "fFrictionIgnoreTimeAfterExpelling": common_types.Float,
    "bWantsRelocationAndExpelImpulse": construct.Flag,
    "bWantsAutomaticOpenOnStartLaunchProcess": construct.Flag,
})

CPlayerMovement = Object(CPlayerMovementFields := {
    **CCharacterMovementFields,
    "bForcedAnalogInput": construct.Flag,
    "fImpactImpulseX": common_types.Float,
    "fImpactImpulseY": common_types.Float,
    "fImpactAirImpulseY": common_types.Float,
    "fImpactHardImpulseX": common_types.Float,
    "fImpactHardImpulseY": common_types.Float,
    "fImpactHardAirImpulseY": common_types.Float,
})

CMorphBallMovement = Object({
    **CPlayerMovementFields,
    "bIsMorphBall": construct.Flag,
    "bIsSamus": construct.Flag,
    "fRunningSpeedX": common_types.Float,
    "fSpiderRunningSpeedX": common_types.Float,
    "fSpiderImpulseSpeedX": common_types.Float,
    "fAirRunningSpeedX": common_types.Float,
    "fSpeedY": common_types.Float,
    "fHighJumpBootSpeedY": common_types.Float,
    "fMinSpeedY": common_types.Float,
    "fMaxSpeedY": common_types.Float,
    "fTimeOnAirAllowingJump": common_types.Float,
    "fNoJumpingGravityFactor": common_types.Float,
    "fImpactIgnoreInputTime": common_types.Float,
    "fImpactIgnoreFrictionTime": common_types.Float,
    "sMovingFX": common_types.StrId,
    "sMovingOilFX": common_types.StrId,
    "sMovingOilSlidingFX": common_types.StrId,
    "sTransformationCustomMaterialFX": common_types.StrId,
    "sTransformationParticlesFX": common_types.StrId,
    "sImpulseFX": common_types.StrId,
    "sFallDustFX": common_types.StrId,
    "sFallOilFX": common_types.StrId,
    "fMinTimeInOilState": common_types.Float,
    "fTotalTimeIgnoringGoToSpider": common_types.Float,
    "sSpiderImpulseEndShake": common_types.StrId,
})

CMorphBallMovement_CTunableMorphBallMovement = Object({
    **base_tunable_CTunableFields,
    "fWaterBombFirstImpactFactor": common_types.Float,
    "fWaterBombSecondImpactFactor": common_types.Float,
    "fWaterBombThirdImpactFactor": common_types.Float,
    "fWaterBombFourthImpactFactor": common_types.Float,
    "fWaterBombFifthImpactFactor": common_types.Float,
    "fSqrDistanceToMakeSpiderJumpWithBomb": common_types.Float,
    "iForceSpiderBallAvailableMode": common_types.Int,
    "bForceSpringBallAvailable": construct.Flag,
    "fWalkingSpeedFactor": common_types.Float,
    "fTimeToIgnoreJumpAfterLandingOnSlope": common_types.Float,
    "fCornerAssistStoppedMaxOverlapFactor": common_types.Float,
    "fCornerAssistMovingMaxOverlapFactor": common_types.Float,
    "fCornerAssistHorizontalVelocityToConsiderMoving": common_types.Float,
    "fCornerAssistMovingAwayFromCornerThresholdFactor": common_types.Float,
    "fAirTimeBeforeSoundRelauch": common_types.Float,
})

CMovableGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CMultiLockOnBlockComponent = Object({
    **CComponentFields,
    "vMultiLockOnPoints": base_global_CRntVector_CGameLink_CEntity__,
})

CMultiLockOnBlockComponent_CTunableMultiLockOnBlockComponent = Object({
    **base_tunable_CTunableFields,
    "fMaxTimeActivate": common_types.Float,
})

CMultiLockOnPointComponent = Object({
    **CActivatableByProjectileComponentFields,
    "wpMultiLockOnBlock": common_types.StrId,
})

CMultiModelUpdaterComponent = Object(CMultiModelUpdaterComponentFields := {
    **CModelUpdaterComponentFields,
    "sModelAlias": common_types.StrId,
})

CMushroomPlatformComponent = Object({
    **CLifeComponentFields,
    "fAlertTimeToRetract": common_types.Float,
    "fRetractedTimeToRelax": common_types.Float,
})

CNailongAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "wpPatrolPath": common_types.StrId,
    "ePatrolPathType": construct_IPath_EType,
})


class CNailongAIComponent_EType(enum.IntEnum):
    Nailong = 0
    Nailugger = 1
    Depthorn = 2
    Invalid = 2147483647


construct_CNailongAIComponent_EType = StrictEnum(CNailongAIComponent_EType)

CNailongThornMovementComponent = Object(CProjectileMovementFields)

CNailongThornsAttack = Object(CAttackFields)


class CNailongThornsAttack_EState(enum.IntEnum):
    InitState = 0
    ChargeThornsState = 1
    WaitToNextAttackState = 2
    TransitionToNextAttackState = 3
    ReleaseThornsState = 4
    ReleaseEndThornsState = 5
    Invalid = 2147483647


construct_CNailongThornsAttack_EState = StrictEnum(CNailongThornsAttack_EState)

CNailuggerAcidBallMovementComponent = Object(CProjectileMovementFields)

CNailuggerAcidBallsAttack = Object(CAttackFields)


class CNailuggerAcidBallsAttack_EState(enum.IntEnum):
    InitState = 0
    ChargeAttackState = 1
    AttackLoopState = 2
    EndAttackState = 3
    Invalid = 2147483647


construct_CNailuggerAcidBallsAttack_EState = StrictEnum(CNailuggerAcidBallsAttack_EState)


class CNavMeshItemStage_ESide(enum.IntEnum):
    NONE = 0
    Left = 1
    Right = 2
    Invalid = 2147483647


construct_CNavMeshItemStage_ESide = StrictEnum(CNavMeshItemStage_ESide)

CNoFreezeRoomComponent = Object(CLogicShapeComponentFields)

CObsydomithonAIComponent = Object(CBehaviorTreeAIComponentFields)

CObsydomithonAttack = Object(CAttackFields)


class CObsydomithonAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    ChargeLoop = 2
    Charge2Attack = 3
    AttackLoop = 4
    AttackLoopEnd = 5
    Ending = 6
    Invalid = 2147483647


construct_CObsydomithonAttack_EState = StrictEnum(CObsydomithonAttack_EState)

COffset = Object({
    "fOffset": common_types.Float,
    "sBoneName": common_types.StrId,
    "fGravity": common_types.Float,
    "fSpeed": common_types.Float,
    "fTimeToNextOffset": common_types.Float,
})

COmniLightComponent = Object({
    **CBaseLightComponentFields,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
    "bCastShadows": construct.Flag,
    "bStaticShadows": construct.Flag,
    "fShadowScl": common_types.Float,
})

base_global_CRntVector_COffset_ = common_types.make_vector(COffset)

TPatterns = base_global_CRntVector_COffset_

CPattern = Object({
    "sPatternName": common_types.StrId,
    "tOffsets": TPatterns,
})

CPerceptionComponent = Object(CComponentFields)


class CPerceptionModifierLogicAction_EMode(enum.IntEnum):
    Add = 0
    Remove = 1
    Invalid = 2147483647


construct_CPerceptionModifierLogicAction_EMode = StrictEnum(CPerceptionModifierLogicAction_EMode)

CPerceptionModifierLogicAction = Object({
    **CTriggerLogicActionFields,
    "eMode": construct_CPerceptionModifierLogicAction_EMode,
    "wpPerceivedPosition": common_types.StrId,
    "eGroup": construct_CAIManager_EAIGroup,
})

CPersistenceComponent = Object(CComponentFields)

CPhotoModeCameraCtrl = Object(CCameraCtrlFields)

CPickable = Object(CGameObjectFields)

CPickableComponent = Object(CPickableComponentFields := {
    **CComponentFields,
    "sOnPickFX": common_types.StrId,
})

CPickableItemComponent = Object(CPickableItemComponentFields := {
    **CPickableComponentFields,
    "sBTType": common_types.StrId,
    "sBTHiddenSceneGroup": common_types.StrId,
    "fTimeToCanBePicked": common_types.Float,
    "sStartPoint": common_types.StrId,
})

CPickableSpringBallComponent = Object(CPickableItemComponentFields)

CPickableSuitComponent = Object(CPickableItemComponentFields)

CPlasmaBeamGun = Object(CPlasmaBeamGunFields := CBeamGunFields)

CPlasmaBeamGun_CTunablePlasmaBeam = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fMaximumHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
    "fDiffusionRadius": common_types.Float,
})

CPlatformTrapGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CPlayerInfo = Object({
    **CGameObjectFields,
    "sInputPreset": common_types.StrId,
    "iHazardousCount": common_types.Int,
    "iHeatZoneCount": common_types.Int,
})

CPlayerLifeComponent = Object({
    **CCharacterLifeComponentFields,
    "fImpactInvulnerableTime": common_types.Float,
    "sImpactHardAnim": common_types.StrId,
    "sHardImpactFX": common_types.StrId,
    "fLifeShards": common_types.Float,
})

CPlayerLifeComponent_CTunablePlayerLifeComponent = Object({
    **base_tunable_CTunableFields,
    "fVariaSuitDamageMult": common_types.Float,
    "fGravitySuitDamageMult": common_types.Float,
    "fHyperSuitDamageMult": common_types.Float,
    "fHardModeDamageMult": common_types.Float,
    "fMorphImplulseDefaultDamage": common_types.Float,
    "fOnDeathMusicsFade": common_types.Float,
    "fSlomoInterpTimeDead": common_types.Float,
    "fSlomoInterpTimeRevive": common_types.Float,
    "fPlayerMaxLifeOverride": common_types.Float,
    "bIgnoreImpact": construct.Flag,
})

CPlayerMovement_CTunablePlayerMovement = Object({
    **base_tunable_CTunableFields,
    "fSlowDownFactor": common_types.Float,
    "fSlowDownFactorMorphBall": common_types.Float,
    "fSlowDownImpulseFactor": common_types.Float,
    "fWalkingJumpVerticalMultiplier": common_types.Float,
    "fWalkingJumpHorizontalMultiplier": common_types.Float,
    "bStealthAbortsSpinJump": construct.Flag,
    "bStealthDuringSpinJumpChangesAnimation": construct.Flag,
    "bWalkingFireEnabled": construct.Flag,
    "bWalkingMeleeEnabled": construct.Flag,
    "bWalkingAnalogAimEnabled": construct.Flag,
    "bMoveDuringWalk": construct.Flag,
    "bParkourUpEnabled": construct.Flag,
    "bParkourDownEnabled": construct.Flag,
    "fParkourAnticipationDistance": common_types.Float,
    "fParkourAnticipationDistanceSpeedBooster": common_types.Float,
    "fParkourDownAnticipationDistance": common_types.Float,
    "fParkourWallMaxDistance": common_types.Float,
    "fParkourNearMaxDistance": common_types.Float,
    "bDetectRunNearWall": construct.Flag,
    "bFallTurnEnabled": construct.Flag,
    "fTimeToScheduleLandingJump": common_types.Float,
    "fTimeToStartFocusInOpticCamo": common_types.Float,
    "fFrozenDamage": common_types.Float,
    "fTimeToFrozenDamage": common_types.Float,
    "iFocusMode": common_types.Int,
    "fParkourMinAdaptiveAnticipationFactor": common_types.Float,
})

std_unique_ptr_CPlaythrough_SCheckpointData_ = Pointer_CPlaythrough_SCheckpointData.create_construct()

base_global_CRntDictionary_base_global_CStrId__std_unique_ptr_CPlaythrough_SCheckpointData__ = common_types.make_dict(std_unique_ptr_CPlaythrough_SCheckpointData_, key=common_types.StrId)

CPlaythrough_TDictCheckpointDatas = base_global_CRntDictionary_base_global_CStrId__std_unique_ptr_CPlaythrough_SCheckpointData__

CPlaythrough = Object({
    **base_core_CAssetFields,
    "sPlaythroughName": common_types.StrId,
    "oPlayDefLink": common_types.StrId,
    "dctCheckpointDatas": CPlaythrough_TDictCheckpointDatas,
})

CPlaythrough_SCheckpointData_SValidationInfo = Object({
    "nGameplayVersion": common_types.Int,
    "uFormatHash": construct.Int64ul,
    "uScenarioHash": construct.Int64ul,
})

CPlaythrough_SCheckpointData = Object({
    "sCheckpointDefID": common_types.StrId,
    "oValidationInfo": CPlaythrough_SCheckpointData_SValidationInfo,
})

std_unique_ptr_CPlaythroughDef_SCheckpointDef_ = Pointer_CPlaythroughDef_SCheckpointDef.create_construct()

base_global_CRntVector__std_unique_ptr_CPlaythroughDef_SCheckpointDef___ = common_types.make_vector(std_unique_ptr_CPlaythroughDef_SCheckpointDef_)

CPlaythroughDef = Object({
    **base_core_CAssetFields,
    "sName": common_types.StrId,
    "sLevelID": common_types.StrId,
    "aCheckpointDefs": base_global_CRntVector__std_unique_ptr_CPlaythroughDef_SCheckpointDef___,
})

CPlaythroughDef_SCheckpointDef = Object({
    "sScenarioID": common_types.StrId,
    "sCheckpointID": common_types.StrId,
    "strDesc": common_types.StrId,
    "sStartPoint": common_types.StrId,
    "strTags": common_types.StrId,
})

CPoisonFlyAIComponent = Object(CBehaviorTreeAIComponentFields)

CPoisonFlyDiveAttack = Object(CAttackFields)

CPolypFallPattern = Object({
    "fFarSpeed": common_types.Float,
    "fMiddleSpeed": common_types.Float,
    "CloseSpeed": common_types.Float,
})

base_global_CFilePathStrId_constPtr = Pointer_base_global_CFilePathStrId.create_construct()

CPositionalSoundComponent = Object({
    **CComponentFields,
    "fMinAtt": common_types.Float,
    "fMaxAtt": common_types.Float,
    "fVol": common_types.Float,
    "fPitch": common_types.Float,
    "fLaunchEvery": common_types.Float,
    "fHorizontalMult": common_types.Float,
    "fVerticalMult": common_types.Float,
    "bLoop": construct.Flag,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "sSound1": base_global_CFilePathStrId_constPtr,
    "sSound2": base_global_CFilePathStrId_constPtr,
    "sSound3": base_global_CFilePathStrId_constPtr,
    "sSound4": base_global_CFilePathStrId_constPtr,
})

CPowerBeamGun = Object(CPowerBeamGunFields := CBeamGunFields)

CPowerBeamGun_CTunablePowerBeam = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fMaximumHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
    "fDiffusionRadius": common_types.Float,
    "fWideTime": common_types.Float,
})

CPowerBombBlockLifeComponent = Object(CLifeComponentFields)

CPowerBombGun = Object(CSecondaryGunFields)

CPowerBombGun_CTunablePowerBomb = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "sDamageSource": common_types.StrId,
    "fHeat": common_types.Float,
})

CPowerBombMovement = Object({
    **CBombMovementFields,
    "fRadiusToAlertMorphball": common_types.Float,
})

CPowerBombMovement_CTunablePowerBombMovement = Object({
    **base_tunable_CTunableFields,
    "fColdDownPowerBombMinTime": common_types.Float,
    "fPowerBombExplosionMaxRadius": common_types.Float,
    "fPowerBombExplosionSpeed": common_types.Float,
    "fPowerBombImplosionSpeed": common_types.Float,
})

CPowerGeneratorComponent = Object({
    **CActivatableComponentFields,
    "wpPowerGeneratorUsable": common_types.StrId,
    "wpPowerGeneratorUsablePlatform": common_types.StrId,
})

CPowerUpLifeComponent = Object({
    **CItemLifeComponentFields,
    "wpCheckPointEntity": common_types.StrId,
    "sPowerupNameLabelID": common_types.StrId,
})

CProfessorDoorComponent = Object(CEventPropComponentFields)


class CPrologueMode_SState(enum.IntEnum):
    NONE = 0
    State0 = 1
    State1 = 2
    State2 = 3
    Invalid = 2147483647


construct_CPrologueMode_SState = StrictEnum(CPrologueMode_SState)

CProtoCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CProtoCentralUnitComponentDef = Object(CCentralUnitComponentDefFields)

CProtoEmmyChaseMusicTriggerComponent = Object(CBaseTriggerComponentFields)

CPullOffGrapplePointComponent = Object({
    **CPullableGrapplePointComponentFields,
    "oActivatableObj": common_types.StrId,
})

CPureFollowCameraCtrl = Object(CCameraCtrlFields)

CQuarentineDoorComponent = Object(CEventPropComponentFields)

CQuetzoaAIComponent = Object(CQuetzoaAIComponentFields := {
    **CBossAIComponentFields,
    "wpShortRangePath": common_types.StrId,
    "eShortRangePathType": construct_IPath_EType,
    "wpLongRangePath": common_types.StrId,
    "eLongRangePathType": construct_IPath_EType,
})

CQuetzoaChargeAttack = Object(CAttackFields)

CQuetzoaEnergyWaveAttack = Object(CAttackFields)

CQuetzoaEnergyWaveMovementComponent = Object(CProjectileMovementFields)

CQuetzoaMultiTargetProjectileMovementComponent = Object(CProjectileMovementFields)

CQuetzoaXAIComponent = Object({
    **CQuetzoaAIComponentFields,
    "wpCoreXSpawnPoint": common_types.StrId,
})

CQuetzoaXMultiTargetAttack = Object(CAttackFields)

CRailCameraCtrl = Object(CCameraBoundaryCtrlFields)

CReserveTankInfo = Object(CGameObjectFields)

CReserveTankInfo_CTunableReserveTanks = Object({
    **base_tunable_CTunableFields,
    "fLifeTankSize": common_types.Float,
    "fSETankSize": common_types.Float,
    "fMissileTankSize": common_types.Float,
})

CSmartObjectComponent = Object(CSmartObjectComponentFields := {
    **CComponentFields,
    "sOnUseStart": common_types.StrId,
    "sOnUseFailure": common_types.StrId,
    "sOnUseSuccess": common_types.StrId,
    "sUsableEntity": common_types.StrId,
    "sDefaultUseAction": common_types.StrId,
    "sDefaultAbortAction": common_types.StrId,
    "bStartEnabled": construct.Flag,
    "fInterpolationTime": common_types.Float,
})

CReturnAreaSmartObjectComponent = Object(CSmartObjectComponentFields)

CRinkaAIComponent = Object(CAIComponentFields)


class CRinkaUnitComponent_ERinkaType(enum.IntEnum):
    A = 0
    B = 1
    C = 2
    Invalid = 2147483647


construct_CRinkaUnitComponent_ERinkaType = StrictEnum(CRinkaUnitComponent_ERinkaType)

CRinkaUnitComponent = Object({
    **CComponentFields,
    "eRinkaType": construct_CRinkaUnitComponent_ERinkaType,
})

CRockDiverAIComponent = Object(CBehaviorTreeAIComponentFields)

CRockDiverSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "fTimeToSpawn": common_types.Float,
})

CRodotukAIComponent = Object(CRodotukAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "eType": construct_CCharClassRodotukAIComponent_SAbsorbConfig_EType,
})

CRodomithonXAIComponent = Object({
    **CRodotukAIComponentFields,
    "eFirePillarType": construct_CCharClassRodomithonXAIComponent_SFirePillarConfig_EType,
})

CRodotukSuckAttack = Object(CRodotukSuckAttackFields := CAttackFields)

CRodomithonXSuckAttack = Object(CRodotukSuckAttackFields)


class ERotationDirection(enum.IntEnum):
    RIGHT = 0
    LEFT = 1
    Invalid = 2147483647


construct_ERotationDirection = StrictEnum(ERotationDirection)

CRotationalPlatformComponent = Object({
    **CComponentFields,
    "wpDestructibleBlock": common_types.StrId,
    "eRotationDirection": construct_ERotationDirection,
})

CRumbleComponent = Object(CComponentFields)

CSPBGun = Object(CBeamGunFields)

CSPBGun_CTunableSPB = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fMaximumHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
})

CSPBTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnitDoor": common_types.StrId,
    "wpCentralUnit": common_types.StrId,
    "oSPRTuto.m_vAfterTutoLogicActions": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
})

CSPRTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnitDoor": common_types.StrId,
    "wpCentralUnit": common_types.StrId,
    "vAfterTutoLogicActions": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
})

CSabotoruAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "fMinTimeBetweenSearch": common_types.Float,
    "fMaxTimeBetweenSearch": common_types.Float,
    "fMinTimeSearching": common_types.Float,
    "fMaxTimeSearching": common_types.Float,
})

CSabotoruLifeComponent = Object(CEnemyLifeComponentFields)

CSabotoruSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "wpDoor": common_types.StrId,
    "wpHomeLandmark": common_types.StrId,
    "bRightSideDoor": construct.Flag,
})

CSabotoruTurnInDoorAttack = Object(CAttackFields)


class CSabotoruTurnInDoorAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    TurnState = 2
    TurnInDoorState = 3
    End = 4
    Invalid = 2147483647


construct_CSabotoruTurnInDoorAttack_EState = StrictEnum(CSabotoruTurnInDoorAttack_EState)

CSamusAction = Object(CSamusActionFields := CActionInstanceFields)

CSamusAimAction = Object(CSamusActionFields)

CSamusAimAngToFrameAction = Object(CSamusActionFields)

CStateParams = Object(CStateParamsFields := {})

CSamusMovementState_CParams = Object(CSamusMovementState_CParamsFields := CStateParamsFields)

CSamusAirMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusAirMovementState_CTunableSamusAirMovementState = Object({
    **base_tunable_CTunableFields,
    "bSpinDoubleJump": construct.Flag,
    "bWallDoubleJump": construct.Flag,
    "bAllowKickJumpWithSpaceJump": construct.Flag,
})

CSamusAlternativeActionPlayerComponent = Object(CAlternativeActionPlayerComponentFields)

CSamusAnalogAimMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusAnimationComponent = Object(CAnimationComponentFields)

CSamusAnimationComponent_CTunableSamusAnimationComponent = Object({
    **base_tunable_CTunableFields,
    "fToRecoilBlendTime": common_types.Float,
    "fFromRecoilBlendTime": common_types.Float,
    "fToAimBlendTime": common_types.Float,
    "fToDefaultBlendTime": common_types.Float,
    "fRecoilTime": common_types.Float,
})

CSamusGroundMovementState_CParams = Object(CSamusGroundMovementState_CParamsFields := CSamusMovementState_CParamsFields)

CSamusCrouchMovementState_CParams = Object(CSamusGroundMovementState_CParamsFields)

CSamusDeathMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusFloorSlideMovementState_CParams = Object(CSamusGroundMovementState_CParamsFields)

CSamusGrabMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusGrappleMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusGrappleMovementState_CTunableSamusGrappleMovementState = Object({
    **base_tunable_CTunableFields,
    "fGrappleInitHangDistance": common_types.Float,
    "fGrappleSwingShortDistance": common_types.Float,
    "fGrappleSwingLongDistance": common_types.Float,
    "fGoingToGrappleMinSpeed": common_types.Float,
    "fGoingToGrappleMaxSpeed": common_types.Float,
    "fGoingToSwingGrappleAccel": common_types.Float,
    "fGoingToSwingGrapplePerpendicularFriction": common_types.Float,
    "fGoingToHangGrappleAccel": common_types.Float,
    "fGoingToHangGrapplePerpendicularFriction": common_types.Float,
    "fGoingToHangPushOutOfCollisionImpulse": common_types.Float,
    "fHangGoingToGrappleArriveDesiredTime": common_types.Float,
    "fSwingGoingToGrappleArriveDesiredTime": common_types.Float,
    "fSwingProgressiveImpulseAccel": common_types.Float,
    "fSwingProgressiveMaxTime": common_types.Float,
    "fSwingMaxAngCos": common_types.Float,
    "fSwingShortPerpendicularFriction": common_types.Float,
    "fSwingLongPerpendicularFriction": common_types.Float,
    "fSwingLongPerpendicularFrictionInImpulse": common_types.Float,
    "fSwingLongPerpendicularFrictionInImpulseBraking": common_types.Float,
    "fSwingGrappleDirMaxSpeed": common_types.Float,
    "fSwingGrappleDirAccel": common_types.Float,
    "fSwingYawSpeed": common_types.Float,
    "fSwingInputDesiredDistanceTime": common_types.Float,
    "bSwingPlayAnimations": construct.Flag,
    "fSwingImpulsePreparationTime": common_types.Float,
    "fSwingKeepEnergyMaxAccel": common_types.Float,
    "fSwingMinSpeedToKeepDirection": common_types.Float,
    "fSwingExitImpulseMinSpeedX": common_types.Float,
    "fSwingExitImpulseMaxSpeedX": common_types.Float,
    "fSwingExitImpulseMinVelY": common_types.Float,
    "fToGrapplePerpFrictionInterpSpeed": common_types.Float,
    "fToGrappleTargetDistanceInterpSpeed": common_types.Float,
    "fGrappleDirMaxSpeedInterpSpeed": common_types.Float,
    "fGravityMultiplier": common_types.Float,
    "fMaxHeightRatioToStartBreakImpulse": common_types.Float,
})

CSamusGunComponent = Object({
    **CGunComponentFields,
    "sSpinAttackFX": common_types.StrId,
    "sScrewAttackFX": common_types.StrId,
})

CSamusGunComponent_CTunableSamusGunComponent = Object({
    **base_tunable_CTunableFields,
    "fScrewAttackDamage": common_types.Float,
    "fBurstChargeBeamActiveTime": common_types.Float,
    "fBurstChargeBeamIdleActiveTimeFactor": common_types.Float,
    "fBurstChargeBeamInitialBurstTime": common_types.Float,
})

CSamusHangMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusHangMovementState_CTunableSamusHangMovementState = Object({
    **base_tunable_CTunableFields,
    "bAnalogAimLimitAngles": construct.Flag,
    "bAllowPreInputResetClimbToMorphBall": construct.Flag,
    "fTimeToIgnoreFastClimbAfterMorphBall": common_types.Float,
})

CSamusImpactMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusInteractMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusMagnetGloveMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusMagnetGloveMovementState_CTunableSamusMagnetGloveMovementState = Object({
    **base_tunable_CTunableFields,
    "bAnalogAimLimitAngles": construct.Flag,
    "bAnalogAimSnapToAxisHorizontal": construct.Flag,
    "fAnalogAimSnapToAxisHorizontalAngleToleranceDegrees": common_types.Float,
    "bAnalogAimSnapToAxisVertical": construct.Flag,
    "fAnalogAimSnapToAxisVerticalAngleToleranceDegrees": common_types.Float,
    "fSurfaceHangMinInputMagnitude": common_types.Float,
    "fMinInputTowardsSurfaceNormalToHang": common_types.Float,
    "fMinInputTowardsDownToDrop": common_types.Float,
    "fTimeToIgnoreHangToMagnetAfterExit": common_types.Float,
    "fTimeToRequireStrictInputToHangLastSurface": common_types.Float,
    "fMinInputTowardsSurfaceNormalToHangLastSurface": common_types.Float,
    "fMaxAngleToKeepReferenceInputAfterTransition": common_types.Float,
    "fMinInputToMove": common_types.Float,
    "fTimeToEnableSpiderPose": common_types.Float,
    "bSpiderPoseRequiresRetap": construct.Flag,
    "fMagnetWallJumpIgnoreMovementTime": common_types.Float,
    "fOpticalCamouflageMagnetWallJumpIgnoreMovementTime": common_types.Float,
})

CSamusModelUpdaterComponent = Object(CMultiModelUpdaterComponentFields)

CSamusMorphBallMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusMovement = Object({
    **CPlayerMovementFields,
    "bIsMorphBall": construct.Flag,
    "bIsSamus": construct.Flag,
    "fFixedModelOffsetYGoingUp": common_types.Float,
    "fFixedModelOffsetYGoingDown": common_types.Float,
    "fFixedRightLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fFixedLeftLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fFixedRightLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fFixedLeftLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fFixedRightLegOffsetGoingUp": common_types.CVector3D,
    "fFixedLeftLegOffsetGoingUp": common_types.CVector3D,
    "fFixedRightLegOffsetGoingDown": common_types.CVector3D,
    "fFixedLeftLegOffsetGoingDown": common_types.CVector3D,
    "fModelOffsetYGoingUp": common_types.Float,
    "fModelOffsetYGoingDown": common_types.Float,
    "fRightLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fLeftLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fRightLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fLeftLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fRightLegOffsetGoingUp": common_types.CVector3D,
    "fLeftLegOffsetGoingUp": common_types.CVector3D,
    "fRightLegOffsetGoingDown": common_types.CVector3D,
    "fLeftLegOffsetGoingDown": common_types.CVector3D,
    "s_fModelOffsetRunningYGoingUp": common_types.Float,
    "s_fModelOffsetRunningYGoingDown": common_types.Float,
    "s_fModelOffsetRunningYOCGoingUp": common_types.Float,
    "s_fModelOffsetRunningYOCGoingDown": common_types.Float,
    "s_fModelOffsetRunningYSlowDownGoingUp": common_types.Float,
    "s_fModelOffsetRunningYSlowDownGoingDown": common_types.Float,
})

CSamusMovement_CTunableSamusMovement = Object({
    **base_tunable_CTunableFields,
    "fFallEndTransitionSpeedOut": common_types.Float,
    "fFloorSlideDistance": common_types.Float,
    "fFloorSlideSpeedBoosterDistance": common_types.Float,
    "fFloorSlideMinTunnelDistanceToExit": common_types.Float,
    "fFloorSlideSpeedBoosterMinTunnelDistanceToExit": common_types.Float,
    "fFloorSlide45JumpForbiddenTimeOnEnterFromAir": common_types.Float,
    "fFloorSlide45JumpForbiddenTimeOnEnterFromGround": common_types.Float,
    "fTimeToScheduleFloorSlide": common_types.Float,
    "fImpulseOnPushOutOfCorner": common_types.Float,
    "fImpulseOnIgnoredSlopeSupport": common_types.Float,
    "fJumpHorizontalImpulseFactor": common_types.Float,
    "fJumpUnderCornerDistanceCheckFromCapsule": common_types.Float,
    "fJumpUnderCornerImpulseOnlyOneSideCollided": common_types.Float,
    "fJumpUnderCornerImpulseCenterCollided": common_types.Float,
    "fJumpUnderCornerCenterCollisionThresholdDistance": common_types.Float,
    "bClimbToMorphBallAutoConvertToSamusOnTunnelExit": construct.Flag,
    "fMorphBallAutoConvertToSamusOnTunnelExitFromFloorSlideMaxTime": common_types.Float,
    "fMorphBallAutoConvertToSamusOnTunnelExitFromClimbMaxTime": common_types.Float,
    "fFallEndTransitionSpeed": common_types.Float,
    "fDistanceToLaunchRunEndBackward": common_types.Float,
    "fDistanceToLaunchRunInitBackward": common_types.Float,
    "bOverrideLegsNodes": construct.Flag,
    "bConvertToMorphBallOnWallNoLowerTunnel": construct.Flag,
    "bForceSnapRotationToSides": construct.Flag,
    "fTimeIgnoringKickJumpAfterWeightBlock": common_types.Float,
})

CSamusOverrideDistanceToBorderLogicAction = Object({
    **CTriggerLogicActionFields,
    "sId": common_types.StrId,
    "fLeftForwardDistance": common_types.Float,
    "fLeftBackwardDistance": common_types.Float,
    "fRightForwardDistance": common_types.Float,
    "fRightBackwardDistance": common_types.Float,
})

CSamusShinesparkMovementState_CParams = Object(CSamusMovementState_CParamsFields)

CSamusStandMovementState_CParams = Object(CSamusGroundMovementState_CParamsFields)

CSaveGameFromEmmyDoorLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpEmmyDoorActor": common_types.StrId,
    "bForce": construct.Flag,
    "bRestoreOriginalValue": construct.Flag,
})


class CSaveGameLogicAction_EDestination(enum.IntEnum):
    savedata = 0
    checkpoint = 1
    Invalid = 2147483647


construct_CSaveGameLogicAction_EDestination = StrictEnum(CSaveGameLogicAction_EDestination)

CSaveGameLogicAction = Object({
    **CTriggerLogicActionFields,
    "eDestination": construct_CSaveGameLogicAction_EDestination,
    "sCheckpointKey": common_types.StrId,
    "wpStartPoint": common_types.StrId,
    "bForce": construct.Flag,
})

CSaveGameToSnapshotLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSnapshotId": common_types.StrId,
})

CSaveSnapshotToCheckpointLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSnapshotId": common_types.StrId,
    "sCheckpointKey": common_types.StrId,
    "wpStartPoint": common_types.StrId,
    "bForce": construct.Flag,
})

CSaveStationUsableComponent = Object(CUsableComponentFields)

CSaveStationUsableComponent_CTunableSaveStationUsableComponent = Object({
    **base_tunable_CTunableFields,
    "fTimeMaxSaveInteract": common_types.Float,
})

base_global_CWeakPtr_game_logic_collision_CCollider_ = Pointer_game_logic_collision_CCollider.create_construct()

base_global_CRntVector_base_global_CWeakPtr_game_logic_collision_CCollider__ = common_types.make_vector(base_global_CWeakPtr_game_logic_collision_CCollider_)

CScenario = Object({
    **CGameObjectFields,
    "awpScenarioColliders": base_global_CRntVector_base_global_CWeakPtr_game_logic_collision_CCollider__,
    "sLevelID": common_types.StrId,
    "sScenarioID": common_types.StrId,
    "rEntitiesLayer": CActorLayer,
    "rSoundsLayer": CActorLayer,
    "rLightsLayer": CActorLayer,
    "vLayerFiles": base_global_CRntVector_base_global_CStrId_,
})

CScenarioPtr = Pointer_CScenario.create_construct()

CScenario_CTunableScenario = Object({
    **base_tunable_CTunableFields,
    "fAreaTextLabelX": common_types.Float,
    "fAreaTextLabelY": common_types.Float,
    "fAreaTextSpriteX": common_types.Float,
    "fAreaTextSpriteY": common_types.Float,
})

CScenarioLogicImporter = Object({})

CSceneModelAnimationComponent = Object({
    **CComponentFields,
    "sModelAnim": common_types.StrId,
})

CSclawkAIComponent = Object(CSclawkAIComponentFields := CBehaviorTreeAIComponentFields)

CSclawkLifeComponent = Object(CEnemyLifeComponentFields)

CScorpiusAIComponent = Object({
    **CBossAIComponentFields,
    "wpPhase2CutScenePlayer": common_types.StrId,
    "wpPhase3CutScenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CScorpiusAttack = Object(CScorpiusAttackFields := CAttackFields)

CScorpiusDefensiveSpikeBallPrickAttack = Object(CScorpiusAttackFields)

CScorpiusDraggedBallPrickAttack = Object(CScorpiusAttackFields)

CScorpiusFXComponent = Object(CSceneComponentFields)

CScorpiusPoisonousGasAttack = Object(CScorpiusPoisonousGasAttackFields := CScorpiusAttackFields)

CScorpiusMovingPoisonousGasAttack = Object(CScorpiusPoisonousGasAttackFields)

CScorpiusPoisonousSpitAttack = Object(CScorpiusAttackFields)

CScorpiusPoisonousSpitMovementComponent = Object(CProjectileMovementFields)

CScorpiusSpikeBallPrickAttack = Object(CScorpiusAttackFields)

CScorpiusTailSmashAttack = Object(CScorpiusAttackFields)

CScorpiusWhiplashAttack = Object(CScorpiusAttackFields)

CScourgeAIComponent = Object(CBehaviorTreeAIComponentFields)

CScourgeLifeComponent = Object(CEnemyLifeComponentFields)

CScourgeTongueSlashAttack = Object(CAttackFields)


class CScourgeTongueSlashAttack_EState(enum.IntEnum):
    NONE = 0
    Starting = 1
    Init = 2
    InitLoop = 3
    Stretch = 4
    Shrink = 5
    End = 6
    Invalid = 2147483647


construct_CScourgeTongueSlashAttack_EState = StrictEnum(CScourgeTongueSlashAttack_EState)

CScriptComponent = Object(CComponentFields)

CSegmentLightComponent = Object({
    **CBaseLightComponentFields,
    "vDir": common_types.CVector3D,
    "fSegmentLength": common_types.Float,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
})

CSensorDoorComponent = Object(CComponentFields)

CSetActorEnabledLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpActor": common_types.StrId,
    "bEnabled": construct.Flag,
})

CShakernautAIComponent = Object(CRobotAIComponentFields)

CShakernautDoubleGroundShockAttack = Object(CAttackFields)


class CShakernautDoubleGroundShockAttack_ESide(enum.IntEnum):
    NONE = 0
    Left = 1
    Right = 2
    Invalid = 2147483647


construct_CShakernautDoubleGroundShockAttack_ESide = StrictEnum(CShakernautDoubleGroundShockAttack_ESide)


class CShakernautDoubleGroundShockAttack_EState(enum.IntEnum):
    NONE = 0
    InitState = 1
    ChargeInitState = 2
    ShotInitFirstArmState = 3
    ShotInitSecondArmState = 4
    ChargeLoopFirstArmState = 5
    ChargeLoopSecondArmState = 6
    ShotFirstArmState = 7
    ShotSecondArmState = 8
    ShotEndFirstArmState = 9
    ShotEndSecondArmState = 10
    ChangeArmState = 11
    EndAttackState = 12
    Invalid = 2147483647


construct_CShakernautDoubleGroundShockAttack_EState = StrictEnum(CShakernautDoubleGroundShockAttack_EState)

CShakernautPiercingLaserAttack = Object(CAttackFields)


class CShakernautPiercingLaserAttack_ESide(enum.IntEnum):
    NONE = 0
    Left = 1
    Right = 2
    Invalid = 2147483647


construct_CShakernautPiercingLaserAttack_ESide = StrictEnum(CShakernautPiercingLaserAttack_ESide)


class CShakernautPiercingLaserAttack_EState(enum.IntEnum):
    NONE = 0
    ToRelaxInitState = 1
    InitState = 2
    ChargeShotState = 3
    FirstShotState = 4
    ShotLoopState = 5
    RelocateEyeState = 6
    EndState = 7
    Invalid = 2147483647


construct_CShakernautPiercingLaserAttack_EState = StrictEnum(CShakernautPiercingLaserAttack_EState)


class EShellState(enum.IntEnum):
    SHELTERED = 0
    UNSHELTERED = 1
    Invalid = 2147483647


construct_EShellState = StrictEnum(EShellState)

CShelmitAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "eShellState": construct_EShellState,
})

CShelmitPlasmaRayAttack = Object(CAttackFields)


class CShelmitPlasmaRayAttack_EAttackState(enum.IntEnum):
    STARTING = 0
    ON_HOLD_CHASE = 1
    CHASING = 2
    PREPARE_SHOOTING = 3
    INIT_SHOOTING = 4
    SHOOTING = 5
    END_SHOOTING = 6
    PREPARE_LAUNCH = 7
    INIT_LAUNCH = 8
    LAUNCHED = 9
    EXPLODING = 10
    ENDING = 11
    Invalid = 2147483647


construct_CShelmitPlasmaRayAttack_EAttackState = StrictEnum(CShelmitPlasmaRayAttack_EAttackState)

CShineonAIComponent = Object(CBehaviorTreeAIComponentFields)

CShipRechargeComponent = Object(CUsableComponentFields)

CShockWavePoolComponent = Object(CComponentFields)

SActivatabledOnEventInfo = Object({
    "pActivatable": common_types.StrId,
    "sIdActivation": common_types.StrId,
})

base_global_CRntVector_SActivatabledOnEventInfo_ = common_types.make_vector(SActivatabledOnEventInfo)

CShootActivatorComponent = Object(CShootActivatorComponentFields := {
    **CItemLifeComponentFields,
    "fInitialAccumulatedTime": common_types.Float,
    "fActivationTime": common_types.Float,
    "fTimePerShot": common_types.Float,
    "vTargetsToActivate": base_global_CRntVector_CGameLink_CActor__,
    "vTargetsToDeactivate": base_global_CRntVector_CGameLink_CActor__,
    "sOnUseEntityTimeline": common_types.StrId,
    "wpAtmosphereEntity": common_types.StrId,
    "vEntitiesActivatabledOnEvent": base_global_CRntVector_SActivatabledOnEventInfo_,
    "vEntitiesDeactivatabledOnEvent": base_global_CRntVector_SActivatabledOnEventInfo_,
})

CShootActivatorComponent_CTunableShootActivatorComponent = Object({
    **base_tunable_CTunableFields,
    "fVolumeMin": common_types.Float,
    "fDecreaseVolumeFactor": common_types.Float,
    "fPitchMin": common_types.Float,
})

CShootActivatorHidrogigaComponent = Object({
    **CShootActivatorComponentFields,
    "wpOtherActivator": common_types.StrId,
    "wpWaterNozzle": common_types.StrId,
})

CShootDCBones = Object({
    "sName": common_types.StrId,
    "tBoneNames": base_global_CRntVector_base_global_CStrId_,
})

base_global_CArray_base_global_CFilePathStrId__EnumClass_EWeaponState__Count__EWeaponState_ = common_types.make_vector(common_types.StrId)

CShotAudioWeaponStates = Object({
    "arrWeaponStateAssets": base_global_CArray_base_global_CFilePathStrId__EnumClass_EWeaponState__Count__EWeaponState_,
})

base_global_CArray_CShotAudioWeaponStates__EnumClass_EWeaponType__Count__EWeaponType_ = common_types.make_vector(CShotAudioWeaponStates)

CShotAudioWeaponPresets = Object({
    "arrAudioPresetsSources": base_global_CArray_CShotAudioWeaponStates__EnumClass_EWeaponType__Count__EWeaponType_,
})

CShotComponent = Object(CComponentFields)

CShotLaunchConfig = Object(CShotLaunchConfigFields := {
    "sID": PropertyEnum,
    "fMaxHitVerticalSpeed": common_types.Float,
    "fTrajectorySampleTimeInterval": common_types.Float,
})

CShotManager = Object({
    "oWeaponAudioPresets": CShotAudioWeaponPresets,
})

CShotManagerPtr = Pointer_CShotManager.create_construct()

CShotManager_CTunableShotManager = Object({
    **base_tunable_CTunableFields,
    "rPowerBeamNormalExplosion": CExplosionGfx,
    "rPowerBeamChargeExplosion": CExplosionGfx,
    "rPowerBeamDiffusionExplosion": CExplosionGfx,
    "rPlasmaBeamNormalExplosion": CExplosionGfx,
    "rPlasmaBeamChargeExplosion": CExplosionGfx,
    "rPlasmaBeamDiffusionExplosion": CExplosionGfx,
    "rWaveBeamNormalExplosion": CExplosionGfx,
    "rWaveBeamChargeExplosion": CExplosionGfx,
    "rWaveBeamDiffusionExplosion": CExplosionGfx,
    "rSPBExplosion": CExplosionGfx,
    "rSPBBlockExplosion": CExplosionGfx,
    "rHyperBeamExplosion": CExplosionGfx,
    "rNoDamageExplosion": CExplosionGfx,
    "rHeatedExplosion": CExplosionGfx,
    "fShotSpeed": common_types.Float,
})

CShotVariableAngleLaunchConfig = Object({
    **CShotLaunchConfigFields,
    "fGravity": common_types.Float,
    "fLaunchSpeed": common_types.Float,
    "fMinLaunchAngleDegs": common_types.Float,
    "fMaxLaunchAngleDegs": common_types.Float,
    "bMakeLaunchSpeedProportionalToDistance": construct.Flag,
    "fLaunchSpeedAtMinDistance": common_types.Float,
    "fDist4MinLaunchSpeed": common_types.Float,
    "fDist4MaxLaunchSpeed": common_types.Float,
})

CShotVariableSpeedLaunchConfig = Object({
    **CShotLaunchConfigFields,
    "fGravity": common_types.Float,
    "fLaunchFixedAngleDegs": common_types.Float,
    "fLaunchMinSpeed": common_types.Float,
    "fLaunchMaxSpeed": common_types.Float,
})

CShowPopUpCompositionLogicAction = Object({
    **CTriggerLogicActionFields,
    "vtexts": base_global_CRntVector_base_global_CStrId_,
})


class CSideEnemyMovement_EDir(enum.IntEnum):
    left = 0
    right = 1
    Invalid = 2147483647


construct_CSideEnemyMovement_EDir = StrictEnum(CSideEnemyMovement_EDir)

CSideEnemyMovement = Object({
    **CEnemyMovementFields,
    "eInitialDir": construct_CSideEnemyMovement_EDir,
})


class ESlidleOutSpawnPointDir(enum.IntEnum):
    ByDot = 0
    Front = 1
    Side = 2
    Invalid = 2147483647


construct_ESlidleOutSpawnPointDir = StrictEnum(ESlidleOutSpawnPointDir)

CSlidleSpawnPointComponent = Object({
    **CComponentFields,
    "eDespawnDir": construct_ESlidleOutSpawnPointDir,
})

CSlowNailongSpawnPointComponent = Object(CSpawnPointComponentFields)

CSluggerAcidBallMovementComponent = Object(CProjectileMovementFields)

CSluggerSpitAttack = Object(CAttackFields)


class CSluggerSpitAttack_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    Spit = 2
    RepeatAttack = 3
    End = 4
    Invalid = 2147483647


construct_CSluggerSpitAttack_EState = StrictEnum(CSluggerSpitAttack_EState)

CSoundListenerComponent = Object({
    **CComponentFields,
    "vLookAt": common_types.CVector3D,
})

CSoundProofTriggerComponent = Object({
    **CBaseTriggerComponentFields,
    "eLowPassFilterToApply": construct_base_snd_ELowPassFilter,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "bMuteActors": construct.Flag,
    "bFilterSpecificActors": construct.Flag,
    "vActorsToIgnore": base_global_CRntVector_CGameLink_CActor__,
})

CSpbSprActivator = Object({
    **CActivatableByProjectileComponentFields,
    "wpSpbSprpPlatform": common_types.StrId,
    "vTargetsToActivate": base_global_CRntVector_CGameLink_CActor__,
    "vTargetsToDeactivate": base_global_CRntVector_CGameLink_CActor__,
    "wpPoolPlatform": common_types.StrId,
})

CSpecialEnergyComponent = Object({
    **CComponentFields,
    "fMaxEnergy": common_types.Float,
    "fEnergy": common_types.Float,
    "bSpecialEnergyLocked": construct.Flag,
})

CSpecialEnergyComponent_CTunableSpecialEnergyComponent = Object({
    **base_tunable_CTunableFields,
    "fTimeToStartEnergyRecover": common_types.Float,
    "fTimeToRecoverAllEnergy": common_types.Float,
    "fTimeToRecoverAllEnergyGhostDash": common_types.Float,
    "fTimeToRecoverAllEnergyOpticalCamuflage": common_types.Float,
    "fTimeToRecoverAllEnergyOpticalCamuflageNotMoving": common_types.Float,
    "fTimeToRecoverAllEnergySonar": common_types.Float,
})

CSpitclawkAIComponent = Object(CSclawkAIComponentFields)

CVulkranMagmaBallMovementComponent = Object(CVulkranMagmaBallMovementComponentFields := CProjectileMovementFields)

CSpittailMagmaBallMovementComponent = Object(CVulkranMagmaBallMovementComponentFields)

CSpotLightComponent = Object({
    **CBaseLightComponentFields,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttIn": common_types.Float,
    "fAttOut": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
    "vDir": common_types.CVector3D,
    "fAnimFrame": common_types.Float,
    "bCastShadows": construct.Flag,
    "vShadowNearFar": common_types.CVector2D,
    "fShadowBias": common_types.Float,
    "bStaticShadows": construct.Flag,
    "fShadowScl": common_types.Float,
    "bHasProjectorTexture": construct.Flag,
    "sTexturePath": common_types.StrId,
    "vProjectorUVScroll": common_types.CVector4D,
})

SFXInstanceData = Object({
    "sFXPath": common_types.StrId,
    "v3Position": common_types.CVector3D,
    "v3Rotation": common_types.CVector3D,
    "v3Scale": common_types.CVector3D,
})

base_global_CRntVector_SFXInstanceData__false_ = common_types.make_vector(SFXInstanceData)

CStandaloneFXComponent = Object({
    **CSceneComponentFields,
    "vctFXInstances": base_global_CRntVector_SFXInstanceData__false_,
    "uPoolSize": common_types.UInt,
    "vScale": common_types.CVector3D,
    "sFXPath": common_types.StrId,
})

CStartCentralUnitCombatLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnit": common_types.StrId,
})

CStartPointComponent = Object({
    **CComponentFields,
    "sOnTeleport": common_types.StrId,
    "sOnTeleportLogicCamera": common_types.StrId,
    "bOnTeleportLogicCameraRaw": construct.Flag,
    "bProjectOnFloor": construct.Flag,
    "bMorphballMode": construct.Flag,
    "bSaveGameToCheckpoint": construct.Flag,
    "bIsBossStartPoint": construct.Flag,
})

CSteamJetComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "fDelayStart": common_types.Float,
    "fDamage": common_types.Float,
    "fLength": common_types.Float,
    "fWidth": common_types.Float,
    "fOnTime": common_types.Float,
    "fOffTime": common_types.Float,
    "fOnOffTime": common_types.Float,
    "fParticleScale": common_types.Float,
    "bCrossingAllowed": construct.Flag,
    "bForceReactionDirection": construct.Flag,
    "vReactionDirection": common_types.CVector2D,
    "wpNextSteamJet": common_types.StrId,
})

CSteeringMovement = Object(CMovementComponentFields)

base_global_CRntVector_std_unique_ptr_CSubareaSetup__constPtr = Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__.create_construct()

base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__constPtr = Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__.create_construct()

CSubAreaManager = Object({
    "vSubareaSetups": base_global_CRntVector_std_unique_ptr_CSubareaSetup__constPtr,
    "vCharclassGroups": base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__constPtr,
})

CSubAreaManagerPtr = Pointer_CSubAreaManager.create_construct()

CSubAreaManager_CTunableSubAreaManager = Object({
    **base_tunable_CTunableFields,
    "fMaxFadeOutTimeLights": common_types.Float,
    "fMaxFadeInTimeLights": common_types.Float,
    "bKillPlayerOutsideScenario": construct.Flag,
})


class CSubAreaManager_ETransitionType(enum.IntEnum):
    NONE = 0
    Camera = 1
    Fade = 2
    FakeFade = 3
    Invalid = 2147483647


construct_CSubAreaManager_ETransitionType = StrictEnum(CSubAreaManager_ETransitionType)

CSubareaCharclassGroup = Object({
    "sId": common_types.StrId,
    "vsCharClassesIds": base_global_CRntVector_base_global_CStrId_,
})

base_global_CArray_base_global_CStrId__EnumClass_ESubAreaItem__Count__ESubAreaItem_ = common_types.make_vector(common_types.StrId)

CSubareaInfo = Object({
    "sId": common_types.StrId,
    "sSetupId": common_types.StrId,
    "sPackSetId": common_types.StrId,
    "bDisableSubArea": construct.Flag,
    "fCameraZDistance": common_types.Float,
    "bIgnoreMetroidCameraOffsets": construct.Flag,
    "sCharclassGroupId": common_types.StrId,
    "asItemsIds": base_global_CArray_base_global_CStrId__EnumClass_ESubAreaItem__Count__ESubAreaItem_,
    "vsCameraCollisionsIds": base_global_CRntVector_base_global_CStrId_,
    "vsCutscenesIds": base_global_CRntVector_base_global_CFilePathStrId_,
})

std_unique_ptr_CSubareaInfo_ = Pointer_CSubareaInfo.create_construct()

base_global_CRntVector_std_unique_ptr_CSubareaInfo__ = common_types.make_vector(std_unique_ptr_CSubareaInfo_)

CSubareaSetup = Object({
    "sId": common_types.StrId,
    "vSubareaConfigs": base_global_CRntVector_std_unique_ptr_CSubareaInfo__,
})

CSubareaTransitionTypeLogicAction = Object({
    **CTriggerLogicActionFields,
    "eTransitionType": construct_CSubAreaManager_ETransitionType,
})

CSunnapAIComponent = Object(CRodotukAIComponentFields)

CSuperMissileGun = Object(CMissileGunFields)

CSuperMissileGun_CTunableSuperMissile = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fHeat": common_types.Float,
})

CSuperMissileMovement = Object(CMissileMovementFields)

CSwarmAttackComponent = Object(CAttackComponentFields)

CSwarmControllerComponent_CTunableSwarmDamage = Object({
    **base_tunable_CTunableFields,
    "fChargedImpactExtraRadius": common_types.Float,
    "fMissileColliderRadius": common_types.Float,
    "fMissileSplashDamageRadius": common_types.Float,
    "fSuperMissileSplashDamageRadius": common_types.Float,
    "fBeamRadius": common_types.Float,
})

CSwifterAIComponent = Object(CBehaviorTreeAIComponentFields)


class ESwifterSpawnGroupSpawnMode(enum.IntEnum):
    Water = 0
    Surface = 1
    Invalid = 2147483647


construct_ESwifterSpawnGroupSpawnMode = StrictEnum(ESwifterSpawnGroupSpawnMode)

CSwifterSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "eDirection": construct_ESwifterSpawnGroupDirection,
    "eMode": construct_ESwifterSpawnGroupSpawnMode,
    "fTimeToSpawn": common_types.Float,
})

CSwingableGrapplePointComponent = Object(CGrapplePointComponentFields)

CTakumakuAIComponent = Object(CBehaviorTreeAIComponentFields)

CTakumakuDashAttack = Object(CAttackFields)


class CTakumakuDashAttack_EState(enum.IntEnum):
    NONE = 0
    Starting = 1
    ChargeLoop = 2
    RunningLoop = 3
    Stopping = 4
    Invalid = 2147483647


construct_CTakumakuDashAttack_EState = StrictEnum(CTakumakuDashAttack_EState)

CTargetComponent = Object(CComponentFields)

CTeamManager_CTunableTeamManager = Object({
    **base_tunable_CTunableFields,
    "fCoordinatedAttacksMinTime": common_types.Float,
    "fCoordinatedAttacksMaxTime": common_types.Float,
})


class ETeleporterColorSphere(enum.IntEnum):
    BLUE = 0
    DARKBLUE = 1
    GREEN = 2
    ORANGE = 3
    PINK = 4
    PURPLE = 5
    RED = 6
    YELLOW = 7
    Invalid = 2147483647


construct_ETeleporterColorSphere = StrictEnum(ETeleporterColorSphere)

CTeleporterUsableComponent = Object({
    **CUsableComponentFields,
    "eLoadingScreen": construct_ELoadingScreen,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "eTeleporterColorSphere": construct_ETeleporterColorSphere,
    "wpFrozenPlatform": common_types.StrId,
})

SDoorInfo = Object({
    "wpThermalDoor": common_types.StrId,
    "sDoorState": construct_CDoorLifeComponent_SState,
})

base_global_CRntVector_SDoorInfo_ = common_types.make_vector(SDoorInfo)


class CThermalDeviceComponent_EPipeGroup(enum.IntEnum):
    Group0 = 0
    Group1 = 1
    Group2 = 2
    Group3 = 3
    Group4 = 4
    Group5 = 5
    Group6 = 6
    Group7 = 7
    Invalid = 2147483647


construct_CThermalDeviceComponent_EPipeGroup = StrictEnum(CThermalDeviceComponent_EPipeGroup)

CThermalDeviceComponent = Object({
    **CUsableComponentFields,
    "vThermalDoors": base_global_CRntVector_SDoorInfo_,
    "sOnEnterUseLuaCallback": common_types.StrId,
    "sOnSetupInitialStateLuaCallback": common_types.StrId,
    "sOnSetupUseStateLuaCallback": common_types.StrId,
    "sUseEndActionOverride": common_types.StrId,
    "bCheckpointBeforeUsage": construct.Flag,
    "ePipeGroup1": construct_CThermalDeviceComponent_EPipeGroup,
    "ePipeGroup2": construct_CThermalDeviceComponent_EPipeGroup,
})

CThermalRoomConnectionFX = Object({
    **CActivatableComponentFields,
    "vTargetToLink": common_types.StrId,
    "vHidderLink": common_types.StrId,
})

CThermalRoomFX = Object(CActivatableComponentFields)

CTimelineComponent = Object({
    **CComponentFields,
    "sInitAction": PropertyEnum,
    "eNextPolicy": construct_CTimelineComponent_ENextPolicy,
    "fMinDelayTime": common_types.Float,
    "fMaxDelayTime": common_types.Float,
})

CTimerComponent = Object(CComponentFields)

CTotalRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})


class ETrainDirection(enum.IntEnum):
    LEFT = 0
    RIGHT = 1
    Invalid = 2147483647


construct_ETrainDirection = StrictEnum(ETrainDirection)

CTrainUsableComponent = Object(CTrainUsableComponentFields := {
    **CUsableComponentFields,
    "eDirection": construct_ETrainDirection,
    "eLoadingScreen": construct_ELoadingScreen,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "sMapConnectionId": common_types.StrId,
    "bAquaLoadingScreen": construct.Flag,
})

CTrainUsableComponentCutScene = Object({
    **CTrainUsableComponentFields,
    "wpCutScenePlayer": common_types.StrId,
})

CTrainWithPortalUsableComponent = Object({
    **CTrainUsableComponentFields,
    "wpPortal": common_types.StrId,
})

CTriggerComponent_CTunableTriggerComponent = Object({
    **base_tunable_CTunableFields,
    "iWaterReverb": common_types.Int,
    "iWaterLowPassFilter": common_types.Int,
    "iLavaReverb": common_types.Int,
    "iLavaLowPassFilter": common_types.Int,
})


class CTriggerComponent_EEvent(enum.IntEnum):
    OnEnter = 0
    OnExit = 1
    OnAllExit = 2
    OnStay = 3
    OnEnable = 4
    OnDisable = 5
    TE_COUNT = 6
    Invalid = 2147483647


construct_CTriggerComponent_EEvent = StrictEnum(CTriggerComponent_EEvent)

CTriggerComponent_SActivationCondition = Object({
    "sID": common_types.StrId,
    "sCharclasses": common_types.StrId,
    "bEnabled": construct.Flag,
    "bAlways": construct.Flag,
    "bDone": construct.Flag,
    "fExecutesEvery": common_types.Float,
    "fExecutesEveryRandomRange": common_types.Float,
    "fLastExecution": common_types.Float,
    "eEvent": construct_CTriggerComponent_EEvent,
    "vLogicActions": base_global_CRntVector_std_unique_ptr_CTriggerLogicAction__,
})

CTriggerNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CTunableMenuHelperClass = Object(CGameObjectFields)

CTunnelTrapMorphballComponent = Object({
    **CComponentFields,
    "aVignettes": base_global_CRntVector_CGameLink_CActor__,
    "bDisableCloseTrapSensor": construct.Flag,
})

CTutoEnterLogicAction = Object({
    **CTriggerLogicActionFields,
    "sLiteralID": common_types.StrId,
    "bShowMessage": construct.Flag,
    "bWaitForInput": construct.Flag,
    "wpObserver": common_types.StrId,
    "sLuaCallbackOnMessageClosed": common_types.StrId,
    "sMissionLogTutoId": common_types.StrId,
})

CTutoExitLogicAction = Object({
    **CTriggerLogicActionFields,
    "sMissionLogTutoId": common_types.StrId,
    "wpTriggerToDisable": common_types.StrId,
})

CTypedProps = Object({})

CUnlockAreaSmartObjectComponent = Object(CSmartObjectComponentFields)

CUnlockAreaSmartObjectComponent_CTunableUnlockAreaSmartObjectComponent = Object({
    **base_tunable_CTunableFields,
    "fIgnoreInputTime": common_types.Float,
    "sDialogID": common_types.StrId,
})

CUsableComponent_CTunableUsableComponent = Object({
    **base_tunable_CTunableFields,
    "fOnLoadBackGroundTimeMax": common_types.Float,
    "fDistanceChannelMin": common_types.Float,
    "fDistanceChannelA": common_types.Float,
    "sForwardChannelA": common_types.StrId,
    "sBackwardChannelA": common_types.StrId,
    "fDistanceChannelB": common_types.Float,
    "sForwardChannelB": common_types.StrId,
    "sBackwardChannelB": common_types.StrId,
    "sForwardChannelC": common_types.StrId,
    "sBackwardChannelC": common_types.StrId,
})

CVideoManagerComponent = Object({
    **CComponentFields,
    "sVideo_1_Path": common_types.StrId,
    "sVideo_2_Path": common_types.StrId,
    "sVideoAux_1_Path": common_types.StrId,
    "sVideoAux_2_Path": common_types.StrId,
})

CVulkranAIComponent = Object(CBehaviorTreeAIComponentFields)

CVulkranAttackManager_CTunableVulkranAttackManager = Object({
    **base_tunable_CTunableFields,
    "fLockTime": common_types.Float,
})

CWarLotusAIComponent = Object(CBehaviorTreeAIComponentFields)

CWaterNozzleComponent = Object({
    **CComponentFields,
    "wpWaterPool": common_types.StrId,
})

CWaterNozzleComponent_CTunableWaterNozzle = Object({
    **base_tunable_CTunableFields,
    "fStopWaterJetDelayTime": common_types.Float,
})

CWaterPlatformUsableComponent = Object({
    **CUsableComponentFields,
    "fTotalMetersToFill": common_types.Float,
    "fSnapToMeters": common_types.Float,
    "fMetersToBreakValve": common_types.Float,
    "fTimeToBreakValve": common_types.Float,
    "fTimeToFillAfterValveBreaks": common_types.Float,
    "fPlatformMovementDelaySinceUseStart": common_types.Float,
})

base_global_CRntVector_float32_ = common_types.make_vector(common_types.Float)

CWaterPoolComponent_FloatingEntitiesInfo = Object({
    "wpFloatingEntity": common_types.StrId,
    "fLevelStopFloating": common_types.Float,
})

base_global_CRntVector_CWaterPoolComponent_FloatingEntitiesInfo_ = common_types.make_vector(CWaterPoolComponent_FloatingEntitiesInfo)

CWaterPoolComponent = Object({
    **CLiquidPoolBaseComponentFields,
    "vWaterLevelChanges": base_global_CRntVector_float32_,
    "tFloatingEntities": base_global_CRntVector_CWaterPoolComponent_FloatingEntitiesInfo_,
    "sOnActivatedLuaCallback": common_types.StrId,
    "bChangedLevelOnCooldownEvent": construct.Flag,
    "vFloatingEntities": base_global_CRntVector_CGameLink_CEntity__,
})

CWaterTriggerChangeComponent = Object({
    **CComponentFields,
    "wpOriginWaterTrigger": common_types.StrId,
    "wpTargetWaterTrigger": common_types.StrId,
    "fChangeTime": common_types.Float,
    "fDelay": common_types.Float,
    "bDeactivateOnFinished": construct.Flag,
    "wpOtherWaterTriggerChange": common_types.StrId,
    "fOriginChange": common_types.Float,
    "fTargetChange": common_types.Float,
    "sOnActivatedLuaCallback": common_types.StrId,
})

CWaveBeamGun = Object(CPlasmaBeamGunFields)

CWaveBeamGun_CTunableWaveBeam = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fMaximumHeat": common_types.Float,
    "fFractionOfHeatAddedPerShot": common_types.Float,
    "fDiffusionRadius": common_types.Float,
})

CWeightActivableMovablePlatformComponent = Object({
    **CMovablePlatformComponentFields,
    "sOnActivatedLuaCallback": common_types.StrId,
})

CWeightActivablePropComponent = Object(CComponentFields)

CWeightActivatedPlatformSmartObjectComponent = Object({
    **CSmartObjectComponentFields,
    "sDustFX": common_types.StrId,
    "bDisableWhenEmmyNearby": construct.Flag,
    "bDisableWhenUsed": construct.Flag,
})

CWideBeamGun = Object(CPowerBeamGunFields)

CWideBeamGun_CTunableWideBeam = Object({
    **base_tunable_CTunableFields,
    "fDamageAmount": common_types.Float,
    "fChargeDamageMult": common_types.Float,
    "fPerpendicularOffsetSize": common_types.Float,
    "fBackwardCheckLenght": common_types.Float,
    "fForwardCheckLenght": common_types.Float,
})

SWorldGraphNode = Object({
    "vPos": common_types.CVector3D,
    "sID": common_types.StrId,
    "bDeadEnd": construct.Flag,
    "tNeighboursIds": base_global_CRntVector_base_global_CStrId_,
})

base_global_CRntVector_SWorldGraphNode_ = common_types.make_vector(SWorldGraphNode)

CWorldGraph = Object({
    **CActorComponentFields,
    "tNodes": base_global_CRntVector_SWorldGraphNode_,
})

CXParasiteAIComponent = Object(CBehaviorTreeAIComponentFields)


class CXParasiteAIComponent_EXParasiteBehaviorType(enum.IntEnum):
    EDrop = 0
    EWanderThenFlee = 1
    EFlee = 2
    EStayOnPlace = 3
    EGoSpawn = 4
    EGoTransform = 5
    EGoToPlayer = 6
    EBeingAbsorbed = 7
    ESpawnOutOfCamera = 8
    Invalid = 2147483647


construct_CXParasiteAIComponent_EXParasiteBehaviorType = StrictEnum(CXParasiteAIComponent_EXParasiteBehaviorType)

CXParasiteBehavior = Object(CXParasiteBehaviorFields := {
    "bCanBeAbsorbed": construct.Flag,
    "fBehaviorProbability": common_types.Float,
    "fOverrideGreenTypeProbability": common_types.Float,
    "fOverrideYellowTypeProbability": common_types.Float,
    "fOverrideOrangeTypeProbability": common_types.Float,
    "fOverrideRedTypeProbability": common_types.Float,
})

std_unique_ptr_CXParasiteBehavior_ = Pointer_CXParasiteBehavior.create_construct()

base_global_CRntVector_std_unique_ptr_CXParasiteBehavior__ = common_types.make_vector(std_unique_ptr_CXParasiteBehavior_)

CXParasiteDropComponent = Object({
    **CComponentFields,
    "vectBehaviors": base_global_CRntVector_std_unique_ptr_CXParasiteBehavior__,
})

CXParasiteGoSpawnBehavior = Object({
    **CXParasiteBehaviorFields,
    "tSpawnPoints": base_global_CRntVector_CGameLink_CActor__,
})

CXParasiteGoTransformBehavior = Object({
    **CXParasiteBehaviorFields,
    "wpFromSpawnPoint": common_types.StrId,
    "tToSpawnPoints": base_global_CRntVector_CGameLink_CActor__,
})

CXParasiteStayOnPlaceBehavior = Object({
    **CXParasiteBehaviorFields,
    "wpStayPosLandmark": common_types.StrId,
})

CXParasiteWanderThenFleeBehavior = Object(CXParasiteBehaviorFields)

CYamplotXAIComponent = Object(CBehaviorTreeAIComponentFields)

CYamplotXBiteAttack = Object(CAttackFields)

CYamplotXStepAttack = Object(CAttackFields)

CharClassLaunchKraidMorphballGrabEvent = Object(base_global_timeline_CEventFields)

CharClassRechargePlayerAmmo = Object({
    **base_global_timeline_CEventFields,
    "fRefillTime": common_types.Float,
})

CharClassRechargePlayerLife = Object({
    **base_global_timeline_CEventFields,
    "fRefillTime": common_types.Float,
})


class EShieldAction(enum.IntEnum):
    Enable = 0
    Disable = 1
    Invalid = 2147483647


construct_EShieldAction = StrictEnum(EShieldAction)

CharClassSakaiModifyShieldEvent = Object({
    **base_global_timeline_CEventFields,
    "eAction": construct_EShieldAction,
})


class EActionPlayMode(enum.IntEnum):
    TIME = 0
    MANUAL = 1
    Invalid = 2147483647


construct_EActionPlayMode = StrictEnum(EActionPlayMode)


class EActionProps(enum.IntEnum):
    DCRootControlled = 0
    DCRootRotationControlled = 1
    DontBlend = 2
    ForceModelUpdate = 3
    IgnoreCullState = 4
    HasNextAction = 5
    HasEndPose = 6
    Invalid = 2147483647


construct_EActionProps = StrictEnum(EActionProps)


class EActionSegmentType(enum.IntEnum):
    Animation = 0
    BlendSpace = 1
    Wait = 2
    Invalid = 2147483647


construct_EActionSegmentType = StrictEnum(EActionSegmentType)


class EActorLayer(enum.IntEnum):
    Entities = 0
    Sounds = 1
    Lights = 2
    Invalid = 4294967295


construct_EActorLayer = StrictEnum(EActorLayer)


class EAmiibo(enum.IntEnum):
    CazadoraSamus = 0
    CazadoraEmmy = 1
    SmashBrosSamus = 2
    SmashBrosDarkSamus = 3
    SmashBrosZeroSamus = 4
    SmashBrosRidley = 5
    SamusReturnsSamus = 6
    SamusReturnsMetroid = 7
    Invalid = 2147483647


construct_EAmiibo = StrictEnum(EAmiibo)


class EEmmyAlertLevel(enum.IntEnum):
    Patrol = 0
    Search = 1
    Chase = 2
    Invalid = 2147483647


construct_EEmmyAlertLevel = StrictEnum(EEmmyAlertLevel)


class EEventProps(enum.IntEnum):
    Layer_0 = 0
    Layer_1 = 1
    Layer_2 = 2
    Layer_3 = 3
    Layer_4 = 4
    Layer_5 = 5
    Layer_6 = 6
    Layer_7 = 7
    Discardable = 8
    DiscardableOnSync = 9


construct_EEventProps = StrictEnum(EEventProps)


class EExecutionReturnValue(enum.IntEnum):
    STOP = 0
    CONTINUE = 1


construct_EExecutionReturnValue = StrictEnum(EExecutionReturnValue)


class EFollowInPathOrientation(enum.IntEnum):
    NONE = 0
    HorizontalOrientation = 1
    VerticalOrientation = 2
    HeuristicOrientation = 3
    Invalid = 2147483647


construct_EFollowInPathOrientation = StrictEnum(EFollowInPathOrientation)


class EGrabEmmySamusQTEMode(enum.IntEnum):
    VFX = 0
    HUD = 1
    Invalid = 2147483647


construct_EGrabEmmySamusQTEMode = StrictEnum(EGrabEmmySamusQTEMode)


class EInputAimDir(enum.IntEnum):
    eFront = 0
    eFrontUp = 1
    eFrontUpUp = 2
    eFrontUpDown = 3
    eFrontDown = 4
    eFrontDownUp = 5
    eFrontDownDown = 6
    Invalid = 2147483647


construct_EInputAimDir = StrictEnum(EInputAimDir)


class EMapTutoType(enum.IntEnum):
    HINT_ZONE = 0
    EMMY_ZONE = 1
    TELEPORTER_NET = 2
    Invalid = 2147483647


construct_EMapTutoType = StrictEnum(EMapTutoType)


class EOnActionEnd(enum.IntEnum):
    HOLD = 0
    LOOP = 1
    PLAY_ACTION = 2
    DEFAULT_LOOP = 3
    Invalid = 2147483647


construct_EOnActionEnd = StrictEnum(EOnActionEnd)


class EPickingMode(enum.IntEnum):
    INVALID = 0
    ENTITIES_PICKING = 1
    SOUNDS_PICKING = 2
    LIGHTS_PICKING = 3
    PATH_PICKING = 4
    WORLDGRAPH_PICKING = 5
    SUBAREA_PICKING = 6


construct_EPickingMode = StrictEnum(EPickingMode)


class ESubAreaItem(enum.IntEnum):
    ScenarioCollider = 0
    LightGroup = 1
    SoundGroup = 2
    SceneGroup = 3
    LogicEntityGroup = 4
    BreakableTileGroupGroup = 5
    EnvironmentPreset = 6
    EnvironmentSoundPreset = 7
    EnvironmentMusicPreset = 8
    Invalid = 4294967295


construct_ESubAreaItem = StrictEnum(ESubAreaItem)


class EThermalFreezeRoomType(enum.IntEnum):
    FREEZE = 0
    COOL_DOWN = 1
    Invalid = 2147483647


construct_EThermalFreezeRoomType = StrictEnum(EThermalFreezeRoomType)


class EThermalHeatRoomType(enum.IntEnum):
    HEAT = 0
    COOL_DOWN = 1
    Invalid = 2147483647


construct_EThermalHeatRoomType = StrictEnum(EThermalHeatRoomType)


class ETooltipCond(enum.IntEnum):
    Bomb = 0
    CentralUnit = 1
    ChargeBeam = 2
    ChozoWarrior = 3
    DiscoveredEmmyCave = 4
    DiscoveredEmmyZone = 5
    DiscoveredEmmyDoors = 6
    GhostDash = 7
    HiddenItemTutorial = 8
    IceMissile = 9
    LineBomb = 10
    Magnet = 11
    MapRoomUsed = 12
    MorphBall = 13
    OpticCamouflage = 14
    SpaceJump = 15
    SpeedBooster = 16
    TeleportUsed = 17
    TeleportWorldUnlocked = 18
    XParasite = 19
    Count = 20


construct_ETooltipCond = StrictEnum(ETooltipCond)


class ETooltipType(enum.IntEnum):
    Exploration = 0
    EmmyPhase1 = 1
    EmmyPhase2 = 2
    BossBattle = 3
    Invalid = 2147483647


construct_ETooltipType = StrictEnum(ETooltipType)


class EWalkInputMode(enum.IntEnum):
    NONE = 0
    ZLHold = 1
    LSHold = 2
    LSToggle = 3
    Invalid = 2147483647


construct_EWalkInputMode = StrictEnum(EWalkInputMode)


class EWeaponState(enum.IntEnum):
    Charging = 0
    Charged = 1
    ChargedLoop = 2
    Fire = 3
    FireCharged = 4
    Impact = 5
    ImpactCharged = 6
    ImpactDiffusion = 7
    Invalid = 4294967295


construct_EWeaponState = StrictEnum(EWeaponState)


class EWeaponType(enum.IntEnum):
    PowerBeam = 0
    WideBeam = 1
    PlasmaBeam = 2
    WaveBeam = 3
    SpecialEnergyBeam = 4
    HyperBeam = 5
    GrappleBeam = 6
    Missile = 7
    SuperMissile = 8
    IceMissile = 9
    LockOnMissile = 10
    SpecialEnergyMissile = 11
    Bomb = 12
    LineBomb = 13
    PowerBomb = 14
    Invalid = 4294967295


construct_EWeaponType = StrictEnum(EWeaponType)

GUI_CDisplayObject = Object(GUI_CDisplayObjectFields := {
    **CGameObjectFields,
    "sID": common_types.StrId,
    "Enabled": construct.Flag,
    "Visible": construct.Flag,
    "Focusable": construct.Flag,
    "DragDropEnabled": construct.Flag,
    "Autosize": construct.Flag,
    "StageID": common_types.StrId,
    "State": common_types.StrId,
    "ClickableAreaShapeID": common_types.StrId,
    "X": common_types.Float,
    "LeftX": common_types.Float,
    "RightX": common_types.Float,
    "CenterX": common_types.Float,
    "Y": common_types.Float,
    "TopY": common_types.Float,
    "BottomY": common_types.Float,
    "CenterY": common_types.Float,
    "Depth": common_types.Float,
    "ScaleX": common_types.Float,
    "ScaleY": common_types.Float,
    "Angle": common_types.Float,
    "ColorR": common_types.Float,
    "ColorG": common_types.Float,
    "ColorB": common_types.Float,
    "ColorA": common_types.Float,
    "SizeX": common_types.Float,
    "SizeY": common_types.Float,
    "BlinkColorR": common_types.Float,
    "BlinkColorG": common_types.Float,
    "BlinkColorB": common_types.Float,
    "BlinkColorA": common_types.Float,
    "Blink": common_types.Float,
    "TimeToDisableBlink": common_types.Float,
    "FadeColorR": common_types.Float,
    "FadeColorG": common_types.Float,
    "FadeColorB": common_types.Float,
    "FadeColorA": common_types.Float,
    "FadeTime": common_types.Float,
    "FocusIdx": common_types.Int,
    "sSkinName": common_types.StrId,
})

GUI_CDisplayObjectPtr = Pointer_GUI_CDisplayObject.create_construct()

base_global_CPooledList_GUI_CDisplayObjectPtr_ = common_types.make_vector(GUI_CDisplayObjectPtr)

GUI_CDisplayObjectContainer = Object(GUI_CDisplayObjectContainerFields := {
    **GUI_CDisplayObjectFields,
    "sChildToFocus": common_types.StrId,
    "lstChildren": base_global_CPooledList_GUI_CDisplayObjectPtr_,
})


class GUI_CButton_TextAlign(enum.IntEnum):
    Align_Centered = 0
    Align_Left = 1
    Align_Right = 2
    Invalid = 2147483647


construct_GUI_CButton_TextAlign = StrictEnum(GUI_CButton_TextAlign)

GUI_CButton = Object(GUI_CButtonFields := {
    **GUI_CDisplayObjectContainerFields,
    "ShowIcon": construct.Flag,
    "LabelText": common_types.StrId,
    "ActivationState": common_types.StrId,
    "OnActivatedSound": common_types.StrId,
    "OnSelectedSound": common_types.StrId,
    "eTextLabelAlignment": construct_GUI_CButton_TextAlign,
    "sOnActivatedSound": common_types.StrId,
    "sOnSelectedSound": common_types.StrId,
    "sTopNeighbour": common_types.StrId,
    "sBottomNeighbour": common_types.StrId,
    "sRightNeighbour": common_types.StrId,
    "sLeftNeighbour": common_types.StrId,
    "bDebugBehaviour": construct.Flag,
})

GUI_CChangeMenuStateButton = Object(GUI_CChangeMenuStateButtonFields := {
    **GUI_CButtonFields,
    "iNewStateIdx": common_types.Int,
})

GUI_CAmiiboButton = Object(GUI_CChangeMenuStateButtonFields)

GUI_CAmiiboComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CArchivesInspectorComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CBoolTunableButton = Object({
    **GUI_CButtonFields,
    "bTunableValue": construct.Flag,
    "sTunableCallback": common_types.StrId,
})

GUI_CChozoGalleryBase = Object(GUI_CChozoGalleryBaseFields := GUI_CDisplayObjectContainerFields)

GUI_CChozoArchivesComposition = Object(GUI_CChozoGalleryBaseFields)

GUI_CContinueGameButton = Object({
    **GUI_CButtonFields,
    "bShowConfirmation": construct.Flag,
})

GUI_CCopySlotButton = Object(GUI_CButtonFields)

GUI_CCreditsButton = Object(GUI_CButtonFields)

GUI_CCustomMarkersDialog = Object(GUI_CDisplayObjectContainerFields)

GUI_CItemRenderer = Object(GUI_CItemRendererFields := GUI_CDisplayObjectContainerFields)

GUI_CDebugMenuEntryItemRenderer = Object(GUI_CItemRendererFields)

GUI_CDebugTunableButton = Object(GUI_CButtonFields)

GUI_CDeleteSlotButton = Object(GUI_CButtonFields)

GUI_CDialogComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CDifficultyButton = Object({
    **GUI_CChangeMenuStateButtonFields,
    "iDifficulty": common_types.Int,
    "sDescription": common_types.StrId,
    "sImage": common_types.StrId,
})

std_unique_ptr_GUI_CTrackSet_ = Pointer_GUI_CTrackSet.create_construct()

GUI_CDisplayObjectAnimationDef = Object({
    "pTrackSet": std_unique_ptr_GUI_CTrackSet_,
})

GUI_CDisplayObjectStateDefPtr = Pointer_GUI_CDisplayObjectStateDef.create_construct()

base_global_CRntVector_GUI_CDisplayObjectStateDefPtr_ = common_types.make_vector(GUI_CDisplayObjectStateDefPtr)

GUI_CDisplayObjectDefPtr = Pointer_GUI_CDisplayObjectDef.create_construct()

base_global_CRntVector_GUI_CDisplayObjectDefPtr_ = common_types.make_vector(GUI_CDisplayObjectDefPtr)

GUI_CDisplayObjectDef = Object({
    **base_core_CBaseObjectFields,
    "sID": common_types.StrId,
    "lstpStates": base_global_CRntVector_GUI_CDisplayObjectStateDefPtr_,
    "lstpChildren": base_global_CRntVector_GUI_CDisplayObjectDefPtr_,
})

std_unique_ptr_GUI_CDisplayObjectAnimationDef_ = Pointer_GUI_CDisplayObjectAnimationDef.create_construct()

GUI_CDisplayObjectStateDef = Object({
    "sID": common_types.StrId,
    "pDOAnimationDef": std_unique_ptr_GUI_CDisplayObjectAnimationDef_,
})

GUI_CDisplayObjectTrackString_SKey = Object({
    "iFrame": common_types.Int,
    "Value": common_types.StrId,
})

GUI_CDisplayObjectTrack_base_global_CRntString__SKey = GUI_CDisplayObjectTrackString_SKey

GUI_CDisplayObjectTrackBool_SKey = Object({
    "iFrame": common_types.Int,
    "Value": construct.Flag,
})

GUI_CDisplayObjectTrack_bool__SKey = GUI_CDisplayObjectTrackBool_SKey

GUI_CDisplayObjectTrackFloat_SKey = Object({
    "iFrame": common_types.Int,
    "Value": common_types.Float,
})

GUI_CDisplayObjectTrack_float__SKey = GUI_CDisplayObjectTrackFloat_SKey

GUI_IDisplayObjectTrack = Object(GUI_IDisplayObjectTrackFields := {})

base_global_CRntVector_GUI_CDisplayObjectTrack_bool__SKey_ = common_types.make_vector(GUI_CDisplayObjectTrack_bool__SKey)

GUI_CDisplayObjectTrackBool = Object({
    **GUI_IDisplayObjectTrackFields,
    "aKeys": base_global_CRntVector_GUI_CDisplayObjectTrack_bool__SKey_,
    "sPropertyID": common_types.StrId,
    "iLoopStartFrame": common_types.Int,
})

base_global_CRntVector_GUI_CDisplayObjectTrack_float__SKey_ = common_types.make_vector(GUI_CDisplayObjectTrack_float__SKey)

GUI_CDisplayObjectTrackFloat = Object({
    **GUI_IDisplayObjectTrackFields,
    "aKeys": base_global_CRntVector_GUI_CDisplayObjectTrack_float__SKey_,
    "sPropertyID": common_types.StrId,
    "iLoopStartFrame": common_types.Int,
})

base_global_CRntVector_GUI_CDisplayObjectTrack_base_global_CRntString__SKey_ = common_types.make_vector(GUI_CDisplayObjectTrack_base_global_CRntString__SKey)

GUI_CDisplayObjectTrackString = Object({
    **GUI_IDisplayObjectTrackFields,
    "aKeys": base_global_CRntVector_GUI_CDisplayObjectTrack_base_global_CRntString__SKey_,
    "sPropertyID": common_types.StrId,
    "iLoopStartFrame": common_types.Int,
})

GUI_CEndingRewardsComposition = Object(GUI_CChozoGalleryBaseFields)

GUI_CExitToMainMenuButton = Object(GUI_CButtonFields)

GUI_CFloatTunableButton = Object({
    **GUI_CButtonFields,
    "fTunableValue": common_types.Float,
    "fTunableIncrement": common_types.Float,
    "fTunableMin": common_types.Float,
    "fTunableMax": common_types.Float,
    "sTunableCallback": common_types.StrId,
})

base_spatial_CPolygon2D_Ptr = Pointer_base_spatial_CPolygon2D.create_construct()

base_global_CRntDictionary_base_global_CStrId__base_spatial_CPolygon2D_Ptr_ = common_types.make_dict(base_spatial_CPolygon2D_Ptr, key=common_types.StrId)

GUI_CGUIManager_ShapeContainer = Object({
    "mapShapes": base_global_CRntDictionary_base_global_CStrId__base_spatial_CPolygon2D_Ptr_,
})

GUI_CSkinPtr = Pointer_GUI_CSkin.create_construct()

base_global_CRntVector_GUI_CSkinPtr_ = common_types.make_vector(GUI_CSkinPtr)

GUI_CGUIManager_SkinContainer = Object({
    "vecSkins": base_global_CRntVector_GUI_CSkinPtr_,
})

GUI_CSpriteSheetPtr = Pointer_GUI_CSpriteSheet.create_construct()

base_global_CRntDictionary_base_global_CStrId__GUI_CSpriteSheetPtr_ = common_types.make_dict(GUI_CSpriteSheetPtr, key=common_types.StrId)

GUI_CGUIManager_SpriteSheetContainer = Object({
    "mapSpriteSheets": base_global_CRntDictionary_base_global_CStrId__GUI_CSpriteSheetPtr_,
})

GUI_CGammaAdjustComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CGlobalMapArea = Object({
    **GUI_CDisplayObjectContainerFields,
    "sTopArea": common_types.StrId,
    "sBottomArea": common_types.StrId,
    "sLeftArea": common_types.StrId,
    "sRightArea": common_types.StrId,
    "sScenarioId": common_types.StrId,
})

GUI_CGlobalMapComposition = Object(GUI_CDisplayObjectContainerFields)


class GUI_CGlobalMapComposition_SState(enum.IntEnum):
    NONE = 0
    NORMAL = 1
    TRANSPORT_CONNECTION = 2
    TELEPORTER_TRAVELING = 3
    TELEPORTER_NET = 4
    AREA_TRAVEL = 5
    NEWAREA_PRESENTATION = 6
    Invalid = 2147483647


construct_GUI_CGlobalMapComposition_SState = StrictEnum(GUI_CGlobalMapComposition_SState)

GUI_CHUD = Object(GUI_CDisplayObjectContainerFields)

GUI_CHUD_SResourceAnimation = Object(GUI_CHUD_SResourceAnimationFields := {})

GUI_CHUD_CBombAnimation = Object(GUI_CHUD_SResourceAnimationFields)

GUI_CHUD_CEnergyAnimation = Object(GUI_CHUD_SResourceAnimationFields)

GUI_CHUD_CMissileAnimation = Object(GUI_CHUD_SResourceAnimationFields)

GUI_CIngameMenu = Object(GUI_CDisplayObjectContainerFields)

GUI_CIntTunableButton = Object({
    **GUI_CButtonFields,
    "iTunableValue": common_types.Int,
    "iTunableIncrement": common_types.Int,
    "iTunableMin": common_types.Int,
    "iTunableMax": common_types.Int,
    "sTunableCallback": common_types.StrId,
})

GUI_CLabel = Object({
    **GUI_CDisplayObjectFields,
    "bApplyVerticalAlignment": construct.Flag,
    "bSequentialTyping": construct.Flag,
    "Outline": construct.Flag,
    "IgnoreTextWidthAutosize": construct.Flag,
    "Font": common_types.StrId,
    "EmbeddedSpritesSuffix": common_types.StrId,
    "Text": common_types.StrId,
    "TextAlignment": common_types.StrId,
    "TextVerticalAlignment": common_types.StrId,
    "MaxTextWidth": common_types.Float,
    "TextInt": common_types.Int,
    "MinCharWidth": common_types.Int,
    "CurrentPage": common_types.Int,
    "MaxVisibleLines": common_types.Int,
    "MaxLinesPerPage": common_types.Int,
    "LineHeightOverride": common_types.Int,
})

GUI_IDataSet = Object(GUI_IDataSetFields := CGameObjectFields)

GUI_CLegendMenuEntryDataSet = Object(GUI_IDataSetFields)

GUI_CLegendMenuEntryItemRenderer = Object(GUI_CItemRendererFields)

GUI_CList = Object({
    **GUI_CDisplayObjectContainerFields,
    "ItemSelectionLoops": construct.Flag,
    "SelectDisabledItems": construct.Flag,
    "ItemActivateOnSelected": construct.Flag,
    "Autoselect": construct.Flag,
    "ItemRendererType": common_types.StrId,
    "NumItemRenderers": common_types.Int,
    "eButtonsTextAlignment": construct_GUI_CButton_TextAlign,
    "iMaxItemNum": common_types.Int,
    "bDebugBehaviour": construct.Flag,
    "bVerticalLayout": construct.Flag,
})

GUI_CLoadCheckPointButton = Object(GUI_CButtonFields)

GUI_CMainMenu = Object(GUI_CDisplayObjectContainerFields)

GUI_CMainMenuComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CMapMenuController = Object(GUI_CDisplayObjectContainerFields)


class GUI_CMapMenuController_SState(enum.IntEnum):
    NONE = 0
    AreaMap = 1
    GlobalMap = 2
    Markers = 3
    Transition = 4
    Invalid = 2147483647


construct_GUI_CMapMenuController_SState = StrictEnum(GUI_CMapMenuController_SState)

GUI_CMenuEntryDataSet = Object(GUI_IDataSetFields)

GUI_CMissionLog = Object(GUI_CDisplayObjectContainerFields)

GUI_CModel3D = Object({
    **GUI_CDisplayObjectFields,
    "ApplyScaleToEntities": construct.Flag,
    "InlineDefModelPath": common_types.StrId,
    "InlineDefAnimPath": common_types.StrId,
    "EntityDefCharClass": common_types.StrId,
    "PosOffsetX": common_types.Float,
    "PosOffsetY": common_types.Float,
    "PosOffsetZ": common_types.Float,
    "MinModelDistance": common_types.Float,
    "MaxModelDistance": common_types.Float,
    "CurrentModelDistance": common_types.Float,
    "HeightInterpSpeed": common_types.Float,
    "DistanceInterpSpeed": common_types.Float,
    "RotationInterpSpeed": common_types.Float,
    "AutorotateVelocity": common_types.Float,
    "DefaultCenterToFloorDist": common_types.Float,
})

GUI_CNewGameButton = Object(GUI_CButtonFields)

GUI_CPopUpComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CPowerDescriptionButton = Object({
    **GUI_CButtonFields,
    "sLabelName": common_types.StrId,
    "sPowerName": common_types.StrId,
    "sPowerDescription": common_types.StrId,
    "sPowerImage": common_types.StrId,
})

GUI_CPowerDescriptionComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CProfileButton = Object({
    **GUI_CChangeMenuStateButtonFields,
    "iProfileIdx": common_types.Int,
})

GUI_CRumbleTunableButton = Object(GUI_CButtonFields)

GUI_CSamusMenuComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CScene3D = Object({
    **GUI_CDisplayObjectFields,
    "ProcessInput": construct.Flag,
    "CameraPathAnimation": common_types.StrId,
    "CameraTargetNode": common_types.StrId,
    "GUIScene": common_types.StrId,
    "CameraDepthOffset": common_types.Float,
    "CameraPathAnimationSpeed": common_types.Float,
    "ManualRotationSpeed": common_types.Float,
    "ManualZoomSpeed": common_types.Float,
    "PitchInterpSpeed": common_types.Float,
    "DepthInterpSpeed": common_types.Float,
})

GUI_CScrollMenuEntryItemRenderer = Object(GUI_CItemRendererFields)

GUI_CSkin = Object({
    "sID": common_types.StrId,
    "vecDisplayObjDefs": base_global_CRntVector_GUI_CDisplayObjectDefPtr_,
})

GUI_CSlotInfoComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CSlotOptionsComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CSlotSelectedComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CSprite = Object({
    **GUI_CDisplayObjectFields,
    "ProgramPreset": common_types.UInt,
    "GenericConstID": common_types.Int,
    "GenericConstValue": common_types.CVector4D,
    "FlipX": construct.Flag,
    "FlipY": construct.Flag,
    "SpriteScaleTilesTexture": construct.Flag,
    "SpriteSheetItem": common_types.StrId,
    "BlendMode": common_types.StrId,
    "USelMode": common_types.StrId,
    "VSelMode": common_types.StrId,
})

GUI_CSpriteGrid = Object({
    **GUI_CDisplayObjectFields,
    "Image": common_types.StrId,
    "CellDefaultSpriteSheetItem": common_types.StrId,
    "GridSizeX": common_types.Int,
    "GridSizeY": common_types.Int,
    "CellSizeX": common_types.Float,
    "CellSizeY": common_types.Float,
    "BlendMode": common_types.StrId,
})

GUI_CSpriteSheetItemPtr = Pointer_GUI_CSpriteSheetItem.create_construct()

base_global_CRntVector_GUI_CSpriteSheetItemPtr_ = common_types.make_vector(GUI_CSpriteSheetItemPtr)

GUI_CSpriteSheet = Object({
    "sTexturePath": common_types.StrId,
    "uTextureWidth": common_types.UInt,
    "uTextureHeight": common_types.UInt,
    "vecItems": base_global_CRntVector_GUI_CSpriteSheetItemPtr_,
})

GUI_CSpriteSheetItem_STexUV = Object({
    "v2Offset": common_types.CVector2D,
    "v2Scale": common_types.CVector2D,
})

GUI_CSpriteSheetItem = Object({
    "sID": common_types.StrId,
    "oTexUVs": GUI_CSpriteSheetItem_STexUV,
})

GUI_CSubtitleComposition = Object(GUI_CDisplayObjectContainerFields)

GUI_CText = Object({
    **GUI_CDisplayObjectFields,
    "Font": common_types.StrId,
    "TextString": common_types.StrId,
    "TextAlignment": common_types.StrId,
    "Text": common_types.Int,
})

GUI_IDisplayObjectTrackPtr = Pointer_GUI_IDisplayObjectTrack.create_construct()

base_global_CRntVector_GUI_IDisplayObjectTrackPtr_ = common_types.make_vector(GUI_IDisplayObjectTrackPtr)

GUI_CTrackSet = Object({
    "vpTracks": base_global_CRntVector_GUI_IDisplayObjectTrackPtr_,
})

GUI_CTutorialComposition = Object(GUI_CDisplayObjectContainerFields)


class SLinkType_ELinkType(enum.IntEnum):
    ACTOR = 0
    ENTITY = 1
    SPAWN_GROUP_ACTOR = 2
    SPAWN_POINT_ACTOR = 3
    LOGIC_SHAPE_ACTOR = 4
    CUTSCENE_ACTOR = 5
    LANDMARK = 6
    AI_SMART_OBJECT = 7
    CAMERA_RAIL = 8
    STEAMJET = 9
    ACTIVATABLE = 10
    MORPH_BALL_LAUNCHER_EXIT = 11
    DEMOLITIONBLOCK_LIFE_ACTOR = 12
    ANY = 13
    INVALID = 14


construct_SLinkType_ELinkType = StrictEnum(SLinkType_ELinkType)


class SLoadScenarioRequest_EMode(enum.IntEnum):
    Game = 0
    Debug = 1
    Editor = 2


construct_SLoadScenarioRequest_EMode = StrictEnum(SLoadScenarioRequest_EMode)


class SMusicManagerState(enum.IntEnum):
    NONE = 0
    NO_MUSIC = 1
    MAINMENU = 2
    INGAME = 3
    INGAME_MENU = 4
    MAP_MENU = 5
    CREDITS = 6
    PROLOGUE = 7
    Invalid = 2147483647


construct_SMusicManagerState = StrictEnum(SMusicManagerState)


class SMusicStopFlag(enum.IntEnum):
    NONE = 0
    PLAY_NEXT = 1
    CLEAR_STACK = 2
    REMOVE_MUSIC_FROM_STACK = 3
    Invalid = 2147483647


construct_SMusicStopFlag = StrictEnum(SMusicStopFlag)

TCheckpointOffset = Object({
    **CCharClassStartPointComponentFields,
    "strCheckpointID": common_types.StrId,
    "vOffsetPos": common_types.CVector3D,
    "vOffsetAng": common_types.CVector3D,
})

std_unique_ptr_sound_CSoundEventsDef_SSoundEventsRule_ = Pointer_sound_CSoundEventsDef_SSoundEventsRule.create_construct()

base_global_CRntVector_std_unique_ptr_sound_CSoundEventsDef_SSoundEventsRule__ = common_types.make_vector(std_unique_ptr_sound_CSoundEventsDef_SSoundEventsRule_)

TSoundEventRules = base_global_CRntVector_std_unique_ptr_sound_CSoundEventsDef_SSoundEventsRule__

animtree_CAnimTreeElement = Object(animtree_CAnimTreeElementFields := CGameObjectFields)

animtree_CAnimTreeControl = Object(animtree_CAnimTreeControlFields := animtree_CAnimTreeElementFields)

animtree_CAnimTreeElementDef = Object(animtree_CAnimTreeElementDefFields := {
    "sName": common_types.StrId,
})

std_unique_ptr_animtree_CAnimTreeElementDef_ = Pointer_animtree_CAnimTreeElementDef.create_construct()

base_global_CRntVector_std_unique_ptr_animtree_CAnimTreeElementDef__ = common_types.make_vector(std_unique_ptr_animtree_CAnimTreeElementDef_)

animtree_CAnimTreeDef_TAnimTreeLinkDef = Object({
    "pNode": common_types.StrId,
    "pParent": common_types.StrId,
})

base_global_CRntVector_animtree_CAnimTreeDef_TAnimTreeLinkDef_ = common_types.make_vector(animtree_CAnimTreeDef_TAnimTreeLinkDef)

animtree_CAnimTreeDef = Object({
    **animtree_CAnimTreeElementDefFields,
    "sRootNode": common_types.StrId,
    "aNodes": base_global_CRntVector_std_unique_ptr_animtree_CAnimTreeElementDef__,
    "aControls": base_global_CRntVector_std_unique_ptr_animtree_CAnimTreeElementDef__,
    "aLinks": base_global_CRntVector_animtree_CAnimTreeDef_TAnimTreeLinkDef_,
})

animtree_CAnimTreeNode = Object(animtree_CAnimTreeNodeFields := animtree_CAnimTreeElementFields)

animtree_CAnimTreeRes = Object({
    **base_core_CAssetFields,
    "oAnimTreeDef": animtree_CAnimTreeDef,
})

animtree_CAnimatedNode = Object(animtree_CAnimTreeNodeFields)


class animtree_CAnimatedNodeDef_EAnimNodeType(enum.IntEnum):
    SkelAnimationPoseBlend = 0
    SkelAnimation = 1
    Invalid = 2147483647


construct_animtree_CAnimatedNodeDef_EAnimNodeType = StrictEnum(animtree_CAnimatedNodeDef_EAnimNodeType)

animtree_CAnimatedNodeDef = Object({
    **animtree_CAnimTreeElementDefFields,
    "eNodeType": construct_animtree_CAnimatedNodeDef_EAnimNodeType,
    "fEventsWeightThreshold": common_types.Float,
    "bLaunchEvents": construct.Flag,
    "bAllowRootMotion": construct.Flag,
    "vBones": base_global_CRntVector_base_global_CStrId_,
    "vBoneHierarchies": base_global_CRntVector_base_global_CStrId_,
})

animtree_CBlendNode = Object(animtree_CAnimTreeNodeFields)

animtree_CBlendNodeDef = Object(animtree_CAnimTreeElementDefFields)

animtree_CBoneControl = Object(animtree_CBoneControlFields := animtree_CAnimTreeControlFields)


class base_math_ETransformSpace(enum.IntEnum):
    WORLD = 0
    LOCAL = 1
    MODEL = 2
    Invalid = 2147483647


construct_base_math_ETransformSpace = StrictEnum(base_math_ETransformSpace)

animtree_CBoneControlDef = Object(animtree_CBoneControlDefFields := {
    **animtree_CAnimTreeElementDefFields,
    "sBone": common_types.StrId,
    "eSpace": construct_base_math_ETransformSpace,
    "bAdditive": construct.Flag,
    "bApplyTranslation": construct.Flag,
    "fBlendInTime": common_types.Float,
    "fBlendOutTime": common_types.Float,
})

animtree_CBoneFilterNode = Object(animtree_CAnimTreeNodeFields)

animtree_CBoneFilterNodeDef = Object({
    **animtree_CAnimTreeElementDefFields,
    "vBones": base_global_CRntVector_base_global_CStrId_,
    "vBoneHierarchies": base_global_CRntVector_base_global_CStrId_,
})

animtree_CCallbackBoneControl = Object(animtree_CCallbackBoneControlFields := animtree_CAnimTreeControlFields)

animtree_CCallbackBoneControlDef = Object(animtree_CCallbackBoneControlDefFields := animtree_CAnimTreeElementDefFields)

animtree_CLayerNode = Object(animtree_CAnimTreeNodeFields)

animtree_CLayerNodeDef = Object({
    **animtree_CAnimTreeElementDefFields,
    "fFactor": common_types.Float,
})

animtree_CLookAtPosControl = Object(animtree_CLookAtPosControlFields := animtree_CBoneControlFields)

animtree_CLookAtEntityControl = Object(animtree_CLookAtPosControlFields)


class base_math_EMaxAxis(enum.IntEnum):
    NONE = 0
    X = 1
    Y = 2
    Z = 3
    NEG_X = 4
    NEG_Y = 5
    NEG_Z = 6
    Invalid = 2147483647


construct_base_math_EMaxAxis = StrictEnum(base_math_EMaxAxis)

animtree_CLookAtPosControlDef = Object(animtree_CLookAtPosControlDefFields := {
    **animtree_CBoneControlDefFields,
    "eLookAxis": construct_base_math_EMaxAxis,
    "eUpAxis": construct_base_math_EMaxAxis,
    "fMinAttAngle": common_types.Float,
    "fMaxAttAngle": common_types.Float,
    "fWorldOffsetAngZ": common_types.Float,
})

animtree_CLookAtEntityControlDef = Object({
    **animtree_CLookAtPosControlDefFields,
    "sEntity": common_types.StrId,
})

animtree_CPoseNode = Object(animtree_CAnimTreeNodeFields)

animtree_CPoseNodeDef = Object(animtree_CAnimTreeElementDefFields)

animtree_CSamusLegsBoneControl = Object(animtree_CCallbackBoneControlFields)

animtree_CSamusLegsBoneControlDef = Object({
    **animtree_CCallbackBoneControlDefFields,
    "sThigh": PropertyEnum,
    "sCalf": PropertyEnum,
    "sFoot": PropertyEnum,
    "fMaxRotationFootUp": common_types.Float,
    "fMaxRotationFootDown": common_types.Float,
    "sMaxFootCorrectionDist": common_types.Float,
})

base_animation_ISkeletonTransformer = Object(base_animation_ISkeletonTransformerFields := {})

base_animation_CAnimationSkeletonTransformer = Object(base_animation_CAnimationSkeletonTransformerFields := base_animation_ISkeletonTransformerFields)

base_animation_CAnimationBlendSkeletonTransformer = Object(base_animation_CAnimationSkeletonTransformerFields)

base_animation_CAnimationResource = Object(base_core_CAssetFields)

base_animation_ISkeletalPoseProvider = Object(base_animation_ISkeletalPoseProviderFields := {})

base_animation_CBlendSpace1D = Object(base_animation_ISkeletalPoseProviderFields)

base_animation_CBlendSpaceResource_SBlendTarget = Object({
    "fSample": common_types.Float,
    "fPlayRate": common_types.Float,
    "sAnimationResource": common_types.StrId,
})

base_global_CRntVector_base_animation_CBlendSpaceResource_SBlendTarget_ = common_types.make_vector(base_animation_CBlendSpaceResource_SBlendTarget)

base_animation_CBlendSpaceResource = Object({
    **base_core_CAssetFields,
    "sVarName": common_types.StrId,
    "vTargets": base_global_CRntVector_base_animation_CBlendSpaceResource_SBlendTarget_,
})

base_animation_CSkeletalAnimation = Object(base_animation_ISkeletalPoseProviderFields)


class base_animation_EBlendFunction(enum.IntEnum):
    Linear = 0
    Smoothstep = 1
    Invalid = 2147483647


construct_base_animation_EBlendFunction = StrictEnum(base_animation_EBlendFunction)

base_color_CColor3F = Object({})

base_color_CColor4B = Object({})

base_color_CColor4F = Object({})

base_core_AssetID = Object({
    "sType": common_types.StrId,
    "sPath": common_types.StrId,
})

base_core_AssetName = Object({
    "sType": common_types.StrId,
    "sName": common_types.StrId,
})

base_curves_CCurveResource = Object(base_core_CAssetFields)


class base_curves_EInterpMode(enum.IntEnum):
    Linear = 0
    Cubic = 1
    Constant = 2
    Invalid = 2147483647


construct_base_curves_EInterpMode = StrictEnum(base_curves_EInterpMode)


class base_curves_ETimeType(enum.IntEnum):
    Uint16 = 0
    Uint8 = 1
    F32 = 2
    Invalid = 2147483647


construct_base_curves_ETimeType = StrictEnum(base_curves_ETimeType)

base_file_IDevice = Object(base_file_IDeviceFields := {})

base_file_CDeviceQueue = Object(base_file_IDeviceFields)

base_file_CFileCacheDevice = Object(base_file_IDeviceFields)

base_file_CPack = Object({})

base_file_CPackManagerDevice = Object(base_file_IDeviceFields)

base_file_CPackSetManager = Object({})

base_file_CThreadSafeDevice = Object(base_file_IDeviceFields)

base_file_nx_CDeviceNX = Object(base_file_IDeviceFields)

sound_CAudioMaterial = Object({
    "vFiles": base_global_CRntVector_base_global_CFilePathStrId_,
})

base_global_CArray_sound_CAudioMaterial__EnumClass_base_snd_EMaterial__Count__base_snd_EMaterial_ = common_types.make_vector(sound_CAudioMaterial)

base_global_CLut = Object({})


class base_snd_ESndPlayerId(enum.IntEnum):
    SFX = 0
    MUSIC = 1
    SPEECH = 2
    GRUNT = 3
    GUI = 4
    ENVIRONMENT_STREAMS = 5
    SFX_EMMY = 6
    CUTSCENE = 7
    Invalid = 2147483647


construct_base_snd_ESndPlayerId = StrictEnum(base_snd_ESndPlayerId)


class base_snd_ESndLogicId(enum.IntEnum):
    DEFAULT = 0
    SHIELD_IMPACT = 1
    FLESH_IMPACT = 2
    WALL_IMPACT = 3
    DOOR_FAIL = 4
    BOSS_DISCOVER = 5
    PHASEDISPLACEMENT = 6
    ENERSHIELDENTER = 7
    ENERSHIELDEXIT = 8
    SAMUS_MOVEMENT = 9
    EMMY_ALARM = 10
    Invalid = 2147483647


construct_base_snd_ESndLogicId = StrictEnum(base_snd_ESndLogicId)


class base_snd_EAttenuationCurve(enum.IntEnum):
    Logarithmic = 0
    Linear = 1
    Invalid = 2147483647


construct_base_snd_EAttenuationCurve = StrictEnum(base_snd_EAttenuationCurve)

sound_CAudioPreset = Object({
    **base_core_CAssetFields,
    "sUniqueId": common_types.StrId,
    "sNodeToAttach": common_types.StrId,
    "arrMatFiles": base_global_CArray_sound_CAudioMaterial__EnumClass_base_snd_EMaterial__Count__base_snd_EMaterial_,
    "ePlayerId": construct_base_snd_ESndPlayerId,
    "eLogicId": construct_base_snd_ESndLogicId,
    "eAttCurve": construct_base_snd_EAttenuationCurve,
    "ePositional": construct_base_snd_EPositionalType,
    "iInstanceLimit": common_types.Int,
    "fInBetweenTime": common_types.Float,
    "fAttMaxRange": common_types.Float,
    "fAttMinRange": common_types.Float,
    "fVolume": common_types.Float,
    "fVolumeRange": common_types.Float,
    "fPitch": common_types.Float,
    "fPitchRange": common_types.Float,
    "fPan": common_types.Float,
    "fPanRange": common_types.Float,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "fEmptyPercentage": common_types.Float,
    "fStartDelayed": common_types.Float,
    "bLoop": construct.Flag,
    "bAttachToActor": construct.Flag,
    "bStpChgAnim": construct.Flag,
    "bStpEntDead": construct.Flag,
    "bManaged": construct.Flag,
    "bRumbleSync": construct.Flag,
    "fRumbleGainOverride": common_types.Float,
    "fDimRelativeVolume": common_types.Float,
    "fDimTime": common_types.Float,
    "fDimFadeTime": common_types.Float,
    "fDimRecoverTime": common_types.Float,
})

base_global_CRntDictionary_base_global_CStrId__sound_CAudioPreset_ = common_types.make_dict(sound_CAudioPreset, key=common_types.StrId)

base_global_CRntPooledDictionary_base_global_CStrId__CBreakableTileManager_STileGroupGroup_ = common_types.make_dict(CBreakableTileManager_STileGroupGroup, key=common_types.StrId)

base_tunable_CTunablePtr = Pointer_base_tunable_CTunable.create_construct()

base_global_CRntSmallDictionary_base_global_CRntString__base_tunable_CTunablePtr_ = common_types.make_dict(base_tunable_CTunablePtr, key=common_types.StrId)

base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_ = common_types.make_dict(CActorComponentPtr, key=common_types.StrId)

base_global_CRntSmallDictionary_base_global_CStrId__base_core_CAssetLink_ = common_types.make_dict(common_types.StrId, key=common_types.StrId)

base_global_CRntVector_CEnvironmentData_SAmbientTransition_ = common_types.make_vector(CEnvironmentData_SAmbientTransition)

base_global_CRntVector_CEnvironmentData_SBloomTransition_ = common_types.make_vector(CEnvironmentData_SBloomTransition)

base_global_CRntVector_CEnvironmentData_SCubeMapTransition_ = common_types.make_vector(CEnvironmentData_SCubeMapTransition)

base_global_CRntVector_CEnvironmentData_SDepthTintTransition_ = common_types.make_vector(CEnvironmentData_SDepthTintTransition)

base_global_CRntVector_CEnvironmentData_SFogTransition_ = common_types.make_vector(CEnvironmentData_SFogTransition)

base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_ = common_types.make_vector(CEnvironmentData_SHemisphericalLightTransition)

base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_ = common_types.make_vector(CEnvironmentData_SIBLAttenuationTransition)

base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_ = common_types.make_vector(CEnvironmentData_SMaterialTintTransition)

base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_ = common_types.make_vector(CEnvironmentData_SPlayerLightTransition)

base_global_CRntVector_CEnvironmentData_SSSAOTransition_ = common_types.make_vector(CEnvironmentData_SSSAOTransition)

base_global_CRntVector_CEnvironmentData_SToneMappingTransition_ = common_types.make_vector(CEnvironmentData_SToneMappingTransition)

base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_ = common_types.make_vector(CEnvironmentData_SVerticalFogTransition)

base_global_CRntVector_base_spatial_CPolygon2D_ = common_types.make_vector(base_spatial_CPolygon2D)

engine_scene_CSceneSlotPtr = Pointer_engine_scene_CSceneSlot.create_construct()

base_global_CRntVector_engine_scene_CSceneSlotPtr_ = common_types.make_vector(engine_scene_CSceneSlotPtr)

navmesh_CDynamicSmartLinkGroup_SDynamicSmartLinkRulesSet = Object({
    "sLinkResource": common_types.StrId,
})

base_global_CRntVector_navmesh_CDynamicSmartLinkGroup_SDynamicSmartLinkRulesSet_ = common_types.make_vector(navmesh_CDynamicSmartLinkGroup_SDynamicSmartLinkRulesSet)

std_unique_ptr_CSubareaCharclassGroup_ = Pointer_CSubareaCharclassGroup.create_construct()

base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__ = common_types.make_vector(std_unique_ptr_CSubareaCharclassGroup_)

std_unique_ptr_CSubareaSetup_ = Pointer_CSubareaSetup.create_construct()

base_global_CRntVector_std_unique_ptr_CSubareaSetup__ = common_types.make_vector(std_unique_ptr_CSubareaSetup_)

base_input_CRumbleManager_CTunableRumbleManager = Object({
    **base_tunable_CTunableFields,
    "fMainGain": common_types.Float,
})

base_input_TRumbleFileData = Object({})

base_reflection_CType = Object(base_reflection_CTypeFields := {
    "sName": common_types.StrId,
    "sBaseTypeName": common_types.StrId,
})

base_reflection_CClass = Object(base_reflection_CTypeFields)

base_reflection_CCollectionType = Object(base_reflection_CTypeFields)

base_reflection_CEnumConstRef = Object({})

base_reflection_CEnumRef = Object({})

base_reflection_CEnumType = Object(base_reflection_CTypeFields)

base_reflection_CFlagsetConstRef = Object({})

base_reflection_CFlagsetRef = Object({})

base_reflection_CFlagsetType = Object(base_reflection_CTypeFields)

base_reflection_CFunction = Object({})

base_reflection_CPointerType = Object(base_reflection_CTypeFields)

base_reflection_CVariable = Object({})


class base_reflection_EAttributeTarget(enum.IntEnum):
    Type = 0
    Variable = 1
    Function = 2
    FunctionParameter = 3


construct_base_reflection_EAttributeTarget = StrictEnum(base_reflection_EAttributeTarget)


class base_reflection_ECollectionAccessMode(enum.IntEnum):
    NONE = 0
    Indexed = 1
    Associative = 2


construct_base_reflection_ECollectionAccessMode = StrictEnum(base_reflection_ECollectionAccessMode)

base_res_CRes = Object(base_res_CResFields := base_core_CAssetFields)

base_serialization_CTypedRefWriter_SCollectionContext = Object({})


class base_serialization_EDeserializeCollectionElementMode(enum.IntEnum):
    UpdateOnly = 0
    InsertOnly = 1
    UpdateOrInsert = 2
    Invalid = 2147483647


construct_base_serialization_EDeserializeCollectionElementMode = StrictEnum(base_serialization_EDeserializeCollectionElementMode)


class base_serialization_EPersistence(enum.IntEnum):
    Transient = 0
    Persistent = 1
    Invalid = 2147483647


construct_base_serialization_EPersistence = StrictEnum(base_serialization_EPersistence)

base_snd_CSoundGroupManager = Object({})

base_snd_CSoundSystem = Object({})

base_snd_CSoundSystem_CTunableSoundSystem = Object({
    **base_tunable_CTunableFields,
    "bSFXEnabled": construct.Flag,
    "bMUSICEnabled": construct.Flag,
    "bSPEECHEnabled": construct.Flag,
    "bGRUNTEnabled": construct.Flag,
    "bGUIEnabled": construct.Flag,
    "bENVIRONMENT_STREAMSEnabled": construct.Flag,
    "bSFX_EMMYEnabled": construct.Flag,
})

base_snd_CSoundSystemATK = Object({})

base_snd_CSoundSystemATK_CTunableSoundSystemATK = Object({
    **base_tunable_CTunableFields,
    "fMainVolume": common_types.Float,
    "fSfxVolume": common_types.Float,
    "fMusicVolume": common_types.Float,
    "fSpeechVolume": common_types.Float,
    "fGruntVolume": common_types.Float,
    "fGUIVolume": common_types.Float,
    "fEnvironmentStreamsVolume": common_types.Float,
})


class base_snd_ESoundGroupIds(enum.IntEnum):
    DEFAULT = 0
    SHIELD_IMPACT = 1
    FLESH_IMPACT = 2
    WALL_IMPACT = 3
    DOOR_FAIL = 4
    BOSS_DISCOVER = 5
    PHASEDISPLACEMENT = 6
    ENERSHIELDENTER = 7
    ENERSHIELDEXIT = 8
    SAMUS_MOVEMENT = 9
    EMMY_ALARM = 10
    Invalid = 2147483647


construct_base_snd_ESoundGroupIds = StrictEnum(base_snd_ESoundGroupIds)


class base_snd_ESoundSystemImGuiTabs(enum.IntEnum):
    Info = 0
    Players = 1
    Invalid = 2147483647


construct_base_snd_ESoundSystemImGuiTabs = StrictEnum(base_snd_ESoundSystemImGuiTabs)

base_spatial_CEditorSegment = Object({
    "vPos": common_types.CVector3D,
})

base_spatial_COBox2D = Object({
    "vCenter": common_types.CVector2D,
    "vExtent": common_types.CVector2D,
    "fRotation": common_types.Float,
})

base_spatial_CPolygonCollection2D = Object({
    "vPolys": base_global_CRntVector_base_spatial_CPolygon2D_,
})

base_tunable_CTunableManager = Object({
    "hashTunables": base_global_CRntSmallDictionary_base_global_CRntString__base_tunable_CTunablePtr_,
})

behaviortree_CBehavior = Object(behaviortree_CBehaviorFields := CGameObjectFields)

behaviortree_CBaseAction = Object(behaviortree_CBaseActionFields := behaviortree_CBehaviorFields)

behaviortree_CAgitateInNervousnessAction = Object({
    **behaviortree_CBaseActionFields,
    "bKeepCalmAndGoPatrol": construct.Flag,
    "fTimeToCalm": common_types.Float,
    "sNervousAction": common_types.StrId,
})

behaviortree_CAttackAction = Object({
    **behaviortree_CBaseActionFields,
    "sAttack": common_types.StrId,
    "sAttackBlc": common_types.StrId,
    "bWaitOnAbort": construct.Flag,
})

behaviortree_CAutclastComputeAttackPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "sAttackPos": common_types.StrId,
    "sAttackUp": common_types.StrId,
})

behaviortree_CAutectorExecuteJumpAction = Object(behaviortree_CBaseActionFields)

behaviortree_CAutoolFollowPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CAutoolGoToRepairPointAction = Object(behaviortree_CBaseActionFields)


class behaviortree_SStatus_Enum(enum.IntEnum):
    NONE = 0
    Invalid = 1
    Running = 2
    Aborting = 3
    Suspended = 4
    Success = 5
    Failed = 6
    Aborted = 7
    Count = 8


construct_behaviortree_SStatus_Enum = StrictEnum(behaviortree_SStatus_Enum)

behaviortree_CBaseCondition = Object(behaviortree_CBaseConditionFields := {
    **behaviortree_CBehaviorFields,
    "bNegate": construct.Flag,
    "eReturnStatusSuccess": construct_behaviortree_SStatus_Enum,
    "eReturnStatusFailed": construct_behaviortree_SStatus_Enum,
})

behaviortree_CBatalloonGoToTargetAction = Object({
    **behaviortree_CBaseActionFields,
    "fAcceleration": common_types.Float,
    "fSpeedMultiplier": common_types.Float,
    "fHareDistance": common_types.Float,
    "bLookAtMoveDir": construct.Flag,
    "bIgnoreCollisionInPath": construct.Flag,
    "bUseSteering": construct.Flag,
    "bRestartnOnPush": construct.Flag,
    "bUseDesiredViewDirAsInitialDir": construct.Flag,
    "bUpdatePath": construct.Flag,
})

behaviortree_CBehaviorTree = Object(CGameObjectFields)

behaviortree_CBigFistChangeToCombatAction = Object(behaviortree_CBaseActionFields)

behaviortree_CBigFistChangeToFleeAction = Object(behaviortree_CBaseActionFields)

behaviortree_CBigFistChangeToPatrolAction = Object(behaviortree_CBaseActionFields)

behaviortree_CBigFistChaseAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "fDesiredChaseDistance": common_types.Float,
})

behaviortree_CBoolCondition = Object({
    **behaviortree_CBaseConditionFields,
    "bValue": construct.Flag,
    "sValue": common_types.StrId,
    "sBlcSection": common_types.StrId,
    "bUseGlobalBlc": construct.Flag,
})

behaviortree_CCanAttackCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sAttack": common_types.StrId,
    "bCheckRotation": construct.Flag,
    "bIgnoreDistance": construct.Flag,
    "bUseSuitableAttack": construct.Flag,
})

behaviortree_CCanDoAttackCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sAttack": common_types.StrId,
})

behaviortree_CCanFleeCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CCanUseHyperDashCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CCentralUnitActivateWeaponAction = Object({
    **behaviortree_CBaseActionFields,
    "iSpawnPointIndex": common_types.Int,
})

behaviortree_CCentralUnitAttackAction = Object({
    **behaviortree_CBaseActionFields,
    "iSpawnPointIndex": common_types.Int,
})

behaviortree_CCentralUnitDeactivateWeaponAction = Object({
    **behaviortree_CBaseActionFields,
    "iSpawnPointIndex": common_types.Int,
})

behaviortree_CChangeAutsniperDirAction = Object(behaviortree_CBaseActionFields)

behaviortree_CChaseTargetAction = Object(behaviortree_CChaseTargetActionFields := {
    **behaviortree_CBaseActionFields,
    "bMaintainViewDirOnReached": construct.Flag,
    "bIgnoreTargetAccesible": construct.Flag,
    "bAccessibleIfReachable": construct.Flag,
    "bCheckTargetAccesibleStandingAbovePath": construct.Flag,
    "fTargetAccesibleMaxHeight": common_types.Float,
    "bGotoMovingIfNotInFrustum": construct.Flag,
    "bAllowTargetToJumpOver": construct.Flag,
    "fMovingToIdleLimitsOffset": common_types.Float,
    "bIgnoreNextAttackTimeOnIdle": construct.Flag,
    "bFaceObstacleFreeTargetSide": construct.Flag,
    "bUseRandomCenter": construct.Flag,
})

behaviortree_CCheckAttackOrderAction = Object(behaviortree_CBaseActionFields)

behaviortree_CCheckCancelAttackOrderAction = Object({
    **behaviortree_CBaseActionFields,
    "bCheckRotation": construct.Flag,
})

behaviortree_CChozoRobotSoldierGotoShootingPositionAction = Object(behaviortree_CBaseActionFields)

behaviortree_CChozoRobotSoldierIsMeleeEntityCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CChozoRobotSoldierIsRangedEntityCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CChozoRobotSoldierPathToTargetWithSmartLinksCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CChozoRobotSoldierPatrolAction = Object(behaviortree_CBaseActionFields)

behaviortree_CComposite = Object(behaviortree_CCompositeFields := behaviortree_CBehaviorFields)

behaviortree_CComputeAttackPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "sPos": common_types.StrId,
    "sClockwise": common_types.StrId,
})

behaviortree_CComputeTargetPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
})

behaviortree_CComputeTargetPositionInPathAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
})

behaviortree_CCopyBlcValueAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropFromName": common_types.StrId,
    "sPropToName": common_types.StrId,
})

behaviortree_CCurrentActionCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sAction": common_types.StrId,
})

behaviortree_CDaivoBackToPositionAction = Object(behaviortree_CBaseActionFields)

behaviortree_CDaivoEnoughAttackSpaceCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CDaivoGoToPlatformEdgeAction = Object(behaviortree_CBaseActionFields)

behaviortree_CDebugAttackAction = Object({
    **behaviortree_CBaseActionFields,
    "sAttack": common_types.StrId,
})

behaviortree_CDecorator = Object(behaviortree_CDecoratorFields := behaviortree_CBehaviorFields)

behaviortree_CDoNothingAction = Object({
    **behaviortree_CBaseActionFields,
    "bWait": construct.Flag,
    "bWaitForever": construct.Flag,
})

behaviortree_CEmmyStateAction = Object(behaviortree_CEmmyStateActionFields := behaviortree_CBaseActionFields)

behaviortree_CEmmyChaseAction = Object(behaviortree_CEmmyStateActionFields)

behaviortree_CEmmyPatrolBaseAction = Object(behaviortree_CEmmyPatrolBaseActionFields := behaviortree_CEmmyStateActionFields)

behaviortree_CEmmyPatrolAction = Object(behaviortree_CEmmyPatrolBaseActionFields)

behaviortree_CEmmyPatrolSearchingAction = Object(behaviortree_CEmmyPatrolBaseActionFields)

behaviortree_CEmmySearchingAction = Object(behaviortree_CEmmyStateActionFields)

behaviortree_CFleeFromTargetAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "bSuccessOnFinish": construct.Flag,
    "bForceGotoSide": construct.Flag,
    "ePathLimitMode": construct_CAIComponent_PathLimitSelectionMode,
    "eAlternativePathLimitMode": construct_CAIComponent_PathLimitSelectionMode,
    "bLookAtDir": construct.Flag,
    "fMinDistance2NewFleePoint": common_types.Float,
    "bForceUseNavmeshPath": construct.Flag,
    "sEndAnim": common_types.StrId,
})

behaviortree_CFleeInPathAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "bSuccessOnFinish": construct.Flag,
    "bSetAnimOnReach": construct.Flag,
    "sAnimOnReach": common_types.StrId,
})


class behaviortree_SCompareOperator_Enum(enum.IntEnum):
    NONE = 0
    LESS = 1
    LESSEQUAL = 2
    EQUAL = 3
    GREATEREQUAL = 4
    GREATER = 5
    Count = 6


construct_behaviortree_SCompareOperator_Enum = StrictEnum(behaviortree_SCompareOperator_Enum)

behaviortree_CFloatCondition = Object({
    **behaviortree_CBaseConditionFields,
    "fValueA": common_types.Float,
    "sValueA": common_types.StrId,
    "sTunableA": common_types.StrId,
    "sTunableVarA": common_types.StrId,
    "fValueB": common_types.Float,
    "sValueB": common_types.StrId,
    "sTunableB": common_types.StrId,
    "sTunableVarB": common_types.StrId,
    "eCompareOperator": construct_behaviortree_SCompareOperator_Enum,
})

behaviortree_CFlyingChaseTargetAction = Object(behaviortree_CChaseTargetActionFields)

behaviortree_CFlyingFollowPathAction = Object({
    **behaviortree_CBaseActionFields,
    "fAcceleration": common_types.Float,
    "fSpeedMultiplier": common_types.Float,
    "fHareDistance": common_types.Float,
    "bLookAtMoveDir": construct.Flag,
    "bIgnoreCollisionInPath": construct.Flag,
    "sPatrolAnim": common_types.StrId,
    "bShouldSetPatrolAnim": construct.Flag,
    "bUseSteering": construct.Flag,
    "bRestartnOnPush": construct.Flag,
    "bUseDesiredViewDirAsInitialDir": construct.Flag,
})

behaviortree_CFollowRouteAction = Object(behaviortree_CBaseActionFields)

behaviortree_CGoToPointAction = Object({
    **behaviortree_CBaseActionFields,
    "sTargetPos": common_types.StrId,
    "bUpdateEachTick": construct.Flag,
    "fReachedDistance": common_types.Float,
    "bLookAtDir": construct.Flag,
    "bForceStop": construct.Flag,
    "bResetParams": construct.Flag,
    "bCheckIfSmartLink": construct.Flag,
    "bGeneratePathOnly": construct.Flag,
})

behaviortree_CGoToSideAction = Object({
    **behaviortree_CBaseActionFields,
    "sDesiredClockwise": common_types.StrId,
})

behaviortree_CGoToTargetAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "bUpdatePath": construct.Flag,
})

behaviortree_CGoToWallFronPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CGroundShockerFollowPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CHasAttackOrderCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CHasLineOfSightCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CHasPathAssigned = Object(behaviortree_CBaseConditionFields)

behaviortree_CHasPathToTargetCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CHasTrackAtCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sTrack": common_types.StrId,
})

behaviortree_CHecathonFollowPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CHyperDashAttackAction = Object({
    **behaviortree_CBaseActionFields,
    "sAttack": common_types.StrId,
    "sAttackBlc": common_types.StrId,
    "bWaitOnAbort": construct.Flag,
})

behaviortree_CIdleAction = Object({
    **behaviortree_CBaseActionFields,
    "bUpdateViewDirection": construct.Flag,
})

behaviortree_CIf = Object(behaviortree_CCompositeFields)

behaviortree_CIgnorePlayerCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CInFuryPatrolAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "bStopInAbort": construct.Flag,
    "sAnim": common_types.StrId,
    "sReturnActionDisp": common_types.StrId,
})

behaviortree_CInIdleNavigationAction = Object(behaviortree_CBaseActionFields)

behaviortree_CInPathPatrolAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "sGrazeInitAction": common_types.StrId,
    "sGrazeEndAction": common_types.StrId,
    "sMinTimeBetweenGrazings": common_types.StrId,
    "sMaxTimeBetweenGrazings": common_types.StrId,
    "sMinTimeGrazing": common_types.StrId,
    "sMaxTimeGrazing": common_types.StrId,
    "bStopInAbort": construct.Flag,
    "bWantsModifyPathIfTargetNear": construct.Flag,
    "bCheckDirToMove": construct.Flag,
    "bAlwaysInDir": construct.Flag,
    "fMaxDistToModifyPath": common_types.Float,
    "fMinDist2GoAway": common_types.Float,
})

behaviortree_CInfesterFleeFromTargetAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "bCalculateFleePointFromTargetPos": construct.Flag,
    "bSuccessOnFinish": construct.Flag,
    "bInFury": construct.Flag,
})

behaviortree_CInfesterIsLoadedCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CInverter = Object(behaviortree_CDecoratorFields)

behaviortree_CIsAIIgnored = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsAtDistanceXCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sFirstPos": common_types.StrId,
    "sSecondPos": common_types.StrId,
    "fDistance": common_types.Float,
    "fHightDistance": common_types.Float,
})

behaviortree_CIsAttackOnCDCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsAttacking = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsDamagedCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsDead = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsFacingTarget = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsFacingToPos = Object({
    **behaviortree_CBaseConditionFields,
    "sPos": common_types.StrId,
})

behaviortree_CIsFrozen = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsGooplotOnThePath = Object({
    **behaviortree_CBaseConditionFields,
    "bClockwise": construct.Flag,
    "fDist": common_types.Float,
})

behaviortree_CIsGrappled = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsInGrab = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsInHightPositionCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsOnPathEdge = Object({
    **behaviortree_CBaseConditionFields,
    "bClockwise": construct.Flag,
    "fDist": common_types.Float,
})

behaviortree_CIsTargetAtDistanceCondition = Object({
    **behaviortree_CBaseConditionFields,
    "fDistance": common_types.Float,
})

behaviortree_CIsTargetDetectedCondition = Object({
    **behaviortree_CBaseConditionFields,
    "bShouldHaveDirectVision": construct.Flag,
})

behaviortree_CIsTargetHangingCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsTargetInPathCondition = Object({
    **behaviortree_CBaseConditionFields,
    "fMaxHeight": common_types.Float,
    "fHorizontalExtraDistance": common_types.Float,
    "bWantsFalseIfTargetHangingAbove": construct.Flag,
})

behaviortree_CIsTargetInsideAreaOfInterestCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsTargetReachableCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsThereFreeOffsetCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsVulkranFrenziedCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CIsZoneReachableCondition = Object({
    **behaviortree_CBaseConditionFields,
    "fMaxTimeToLoseDetection": common_types.Float,
})

behaviortree_CKreepStoreHomePosAction = Object(behaviortree_CBaseActionFields)

behaviortree_CLogAction = Object({
    **behaviortree_CBaseActionFields,
    "iCount": common_types.Int,
    "sText": common_types.StrId,
})

behaviortree_CMoveToTargetLastKnownPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
    "fRefreshRate": common_types.Float,
    "bShouldLookAtDir": construct.Flag,
})

behaviortree_CMultiplyBlackboardValueAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
    "fMultiplier": common_types.Float,
})

behaviortree_CNailongFollowPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CObsydomithonActivationAction = Object(behaviortree_CBaseActionFields)


class behaviortree_CParallel_EPolicy(enum.IntEnum):
    RequireOne = 0
    RequireAll = 1
    Invalid = 2147483647


construct_behaviortree_CParallel_EPolicy = StrictEnum(behaviortree_CParallel_EPolicy)

behaviortree_CParallel = Object({
    **behaviortree_CCompositeFields,
    "eSuccessPolicy": construct_behaviortree_CParallel_EPolicy,
    "eFailurePolicy": construct_behaviortree_CParallel_EPolicy,
})

behaviortree_CParticleEnableEmission = Object({
    **behaviortree_CBaseActionFields,
    "sFX": common_types.StrId,
    "bEnable": construct.Flag,
    "bDisableOnEmpty": construct.Flag,
    "bWaitEmissionStop": construct.Flag,
})

behaviortree_CPathToTargetWithSmartLinksCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CPoisonFlyChasePlayerAction = Object({
    **behaviortree_CBaseActionFields,
    "fReachedDistance": common_types.Float,
})

behaviortree_CPoisonFlyOnSamusDetectedAction = Object(behaviortree_CBaseActionFields)

behaviortree_CPoisonFlyRequestAttackOffset = Object(behaviortree_CBaseActionFields)

behaviortree_CQuetzoaAvailableAttackPositionCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CQuetzoaFollowInPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CQuetzoaFollowPathAction = Object({
    **behaviortree_CBaseActionFields,
    "bFlee": construct.Flag,
    "fSpeedMultiplier": common_types.Float,
})

behaviortree_CRandomCondition = Object({
    **behaviortree_CBaseConditionFields,
    "fValue": common_types.Float,
    "sValue": common_types.StrId,
})

behaviortree_CRepeat = Object({
    **behaviortree_CDecoratorFields,
    "bWait": construct.Flag,
})

behaviortree_CRepeatIfFailed = Object({
    **behaviortree_CDecoratorFields,
    "bWait": construct.Flag,
})

behaviortree_CRepeatIfSuccess = Object({
    **behaviortree_CDecoratorFields,
    "bWait": construct.Flag,
})

behaviortree_CRinkaRandomShootAction = Object({
    **behaviortree_CBaseActionFields,
    "iSpawnPointIndex": common_types.Int,
    "fRinkaTypeAProbability": common_types.Float,
    "fRinkaTypeBProbability": common_types.Float,
    "fRinkaTypeCProbability": common_types.Float,
})

behaviortree_CRinkaShootAction = Object({
    **behaviortree_CBaseActionFields,
    "iSpawnPointIndex": common_types.Int,
    "eRinkaType": construct_CRinkaUnitComponent_ERinkaType,
})

behaviortree_CRotateToPlayer = Object({
    **behaviortree_CBaseActionFields,
    "bKeepRunning": construct.Flag,
    "bRotateOnlyHorizontally": construct.Flag,
})

behaviortree_CSabotoruIsFarFromCornerCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CSabotoruIsSamusInsideDoorCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CScaredAction = Object({
    **behaviortree_CBaseActionFields,
    "fMaxTimeScared": common_types.Float,
})


class behaviortree_CScaredAction_EState(enum.IntEnum):
    NONE = 0
    Started = 1
    Init = 2
    Loop = 3
    Ending = 4
    Finished = 5
    Invalid = 2147483647


construct_behaviortree_CScaredAction_EState = StrictEnum(behaviortree_CScaredAction_EState)

behaviortree_CScorpiusRegereratingMaskAction = Object(behaviortree_CBaseActionFields)

behaviortree_CScourgeComputeAttackPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "sPos": common_types.StrId,
    "sClockwise": common_types.StrId,
    "sUsePos": common_types.StrId,
})

behaviortree_CSelector = Object(behaviortree_CCompositeFields)

behaviortree_CSequence = Object(behaviortree_CCompositeFields)

behaviortree_CSetAnimAction = Object({
    **behaviortree_CBaseActionFields,
    "sAnim": common_types.StrId,
    "sAnimProp": common_types.StrId,
    "sTimelineStart": common_types.StrId,
    "sTimelineEnd": common_types.StrId,
    "bForce": construct.Flag,
    "bUpdateModel": construct.Flag,
    "bWaitAnimEnd": construct.Flag,
    "bWaitIfFrozen": construct.Flag,
    "bSyncWithCurrent": construct.Flag,
    "iMinRandSuffix": common_types.Int,
    "iMaxRandSuffix": common_types.Int,
})

behaviortree_CSetAnimDependsOnDirAction = Object({
    **behaviortree_CBaseActionFields,
    "sInDirAnim": common_types.StrId,
    "sInDirAnimProp": common_types.StrId,
    "sNotInDirAnim": common_types.StrId,
    "sNotInDirAnimProp": common_types.StrId,
    "sInDirIdleAnim": common_types.StrId,
    "sInDirIdleAnimProp": common_types.StrId,
    "sTargetPos": common_types.StrId,
    "bForceViewDir": construct.Flag,
    "bInvertViewDir": construct.Flag,
    "bForce": construct.Flag,
    "bUpdateModel": construct.Flag,
    "bWaitAnimEnd": construct.Flag,
    "bWaitIfFrozen": construct.Flag,
    "bSyncWithCurrent": construct.Flag,
    "iMinRandSuffix": common_types.Int,
    "iMaxRandSuffix": common_types.Int,
    "bCheckInSmartlink": construct.Flag,
    "bCheckInTurn": construct.Flag,
    "sReturnActionDisp": common_types.StrId,
    "bFailIfSmartlink": construct.Flag,
})

behaviortree_CSetAnimationForImpact = Object({
    **behaviortree_CBaseActionFields,
    "sFrontImpact": common_types.StrId,
    "sBackImpact": common_types.StrId,
    "bWaitAnimEnd": construct.Flag,
    "bWaitIfFrozen": construct.Flag,
})

behaviortree_CSetClockwiseDirBlcValueAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
    "fMultiplier": common_types.Float,
})

behaviortree_CSetEndAnimAction = Object(behaviortree_CSetEndAnimActionFields := {
    **behaviortree_CBaseActionFields,
    "bForce": construct.Flag,
    "bWaitAnimEnd": construct.Flag,
    "bWaitIfFrozen": construct.Flag,
    "bSyncWithCurrent": construct.Flag,
})

behaviortree_CSetCrazyEndAnimAction = Object(behaviortree_CSetEndAnimActionFields)

behaviortree_CSetFXAction = Object({
    **behaviortree_CBaseActionFields,
    "sFX": common_types.StrId,
    "bSet": construct.Flag,
    "bEnd": construct.Flag,
})

behaviortree_CSetRotationAction = Object({
    **behaviortree_CBaseActionFields,
    "bSetX": construct.Flag,
    "bSetY": construct.Flag,
    "bSetZ": construct.Flag,
    "fXValue": common_types.Float,
    "fYValue": common_types.Float,
    "fZValue": common_types.Float,
})

behaviortree_CSetStickySideWalkAnim = Object({
    **behaviortree_CBaseActionFields,
    "sSideWalkAnim": common_types.StrId,
})

behaviortree_CSetTimelineAction = Object({
    **behaviortree_CBaseActionFields,
    "sTimeline": common_types.StrId,
    "bSet": construct.Flag,
})

behaviortree_CSetWantsEnabledAction = Object({
    **behaviortree_CBaseActionFields,
    "sComponentName": common_types.StrId,
    "bEnabled": construct.Flag,
})

behaviortree_CShakernautChaseTargetAction = Object({
    **behaviortree_CBaseActionFields,
    "bMaintainViewDirOnReached": construct.Flag,
    "bIgnoreTargetAccesible": construct.Flag,
    "bGotoMovingIfNotInFrustum": construct.Flag,
    "bAllowTargetToJumpOver": construct.Flag,
    "fMovingToIdleLimitsOffset": common_types.Float,
    "bIgnoreNextAttackTimeOnIdle": construct.Flag,
    "fMinDist": common_types.Float,
    "fMaxDist": common_types.Float,
    "fCenterDistance": common_types.Float,
})

behaviortree_CShakernautIsTargetDetectedPartiallyCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CShelmitChargeAction = Object(behaviortree_CBaseActionFields)

behaviortree_CShelmitIsChargedCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CShelmitIsShelteredCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CShineonFollowPathAction = Object(behaviortree_CBaseActionFields)

behaviortree_CSluggerGoToPlatformEdgeAction = Object(behaviortree_CBaseActionFields)

behaviortree_CStopInIdleAction = Object({
    **behaviortree_CBaseActionFields,
    "fTimeWaitting": common_types.Float,
    "sAnim": common_types.StrId,
    "sAnimProp": common_types.StrId,
})

behaviortree_CStopWatchAction = Object({
    **behaviortree_CBaseActionFields,
    "sElapsedTime": common_types.StrId,
    "fMinTime": common_types.Float,
    "fMaxTime": common_types.Float,
    "sMinTime": common_types.StrId,
    "sMaxTime": common_types.StrId,
    "bResetElapsedTimeOnSuccess": construct.Flag,
    "eReturnStatusFailed": construct_behaviortree_SStatus_Enum,
})

behaviortree_CStoreBoolInBlcAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
    "bValue": construct.Flag,
})

behaviortree_CStoreFloatInBlcAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
    "fValue": common_types.Float,
})

behaviortree_CStorePosInBlcAction = Object({
    **behaviortree_CBaseActionFields,
    "sEntityNameBlc": common_types.StrId,
    "sPropName": common_types.StrId,
})

behaviortree_CStoreSamusDirectionAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
})

behaviortree_CStoreStringInBlcAction = Object({
    **behaviortree_CBaseActionFields,
    "sPropName": common_types.StrId,
    "sValue": common_types.StrId,
})

behaviortree_CStringEqualsCondition = Object({
    **behaviortree_CBaseConditionFields,
    "sRawValue": common_types.StrId,
    "sBlackboardValue": common_types.StrId,
})

behaviortree_CSuppressDecorator = Object({
    **behaviortree_CDecoratorFields,
    "eReturnStatus": construct_behaviortree_SStatus_Enum,
})

behaviortree_CSwitchBetweenAIModesAction = Object({
    **behaviortree_CBaseActionFields,
    "sAnim": common_types.StrId,
    "sAnimProp": common_types.StrId,
    "sTurnAnim": common_types.StrId,
    "ePrefixToAdd": construct_CAnimationPrefix_SPrefix_Enum,
    "ePrefixToRemove": construct_CAnimationPrefix_SPrefix_Enum,
    "bWaitUntilActionEnds": construct.Flag,
    "eStatusIfCantSetAction": construct_behaviortree_SStatus_Enum,
    "sTimelineStart": common_types.StrId,
    "sTimelineEnd": common_types.StrId,
    "bCheckIfSmartLink": construct.Flag,
    "bSetAction": construct.Flag,
    "bMaintainFrame": construct.Flag,
})

behaviortree_CTakumakuChaseAction = Object(behaviortree_CBaseActionFields)

behaviortree_CTakumakuSpikeBumpAction = Object(behaviortree_CBaseActionFields)

behaviortree_CTargetIsInHightPositionCondition = Object(behaviortree_CBaseConditionFields)

behaviortree_CTimeBetweenImpactsGreaterThan = Object({
    **behaviortree_CBaseConditionFields,
    "fTime": common_types.Float,
    "sTime": common_types.StrId,
})

behaviortree_CTunableBoolCondition = Object({
    **behaviortree_CBaseConditionFields,
    "bValue": construct.Flag,
    "sCategory": common_types.StrId,
    "sVariable": common_types.StrId,
})

behaviortree_CTurnInDoorAction = Object(behaviortree_CBaseActionFields)

behaviortree_CVulkranActivationAction = Object(behaviortree_CBaseActionFields)

behaviortree_CVulkranChaseAction = Object(behaviortree_CBaseActionFields)

behaviortree_CWaitAction = Object(behaviortree_CWaitActionFields := {
    **behaviortree_CBaseActionFields,
    "fTime": common_types.Float,
    "sTime": common_types.StrId,
    "sTunable": common_types.StrId,
    "sTunableVar": common_types.StrId,
    "bWaitTick": construct.Flag,
    "bShouldHaveLOS": construct.Flag,
})

behaviortree_CWaitRandomAction = Object({
    **behaviortree_CWaitActionFields,
    "fRandomOffset": common_types.Float,
})

behaviortree_CWasImpacted = Object({
    **behaviortree_CBaseConditionFields,
    "fTime": common_types.Float,
    "bCheckTargetInTheBack": construct.Flag,
})

behaviortree_CXParasiteBehaviorCondition = Object({
    **behaviortree_CBaseConditionFields,
    "eBehaviorType": construct_CXParasiteAIComponent_EXParasiteBehaviorType,
})

behaviortree_CXParasiteChooseWanderPositionAction = Object({
    **behaviortree_CBaseActionFields,
    "fWanderRadius": common_types.Float,
})

behaviortree_CXParasiteGoToPointAction = Object({
    **behaviortree_CBaseActionFields,
    "sGoToPosBlackboard": common_types.StrId,
    "sGoToEntityBlackboard": common_types.StrId,
    "bStopOnArrive": construct.Flag,
    "bUseWaypoints": construct.Flag,
    "fMotionSpeed": common_types.Float,
    "fAccelerationForce": common_types.Float,
    "fBrakeForce": common_types.Float,
    "fBrakeDistance": common_types.Float,
    "fTurningForce": common_types.Float,
    "fMaxTurningAngle": common_types.Float,
})

behaviortree_CXParasiteSpawnAction = Object(behaviortree_CBaseActionFields)

behaviortree_CXParasiteTransformAction = Object({
    **behaviortree_CBaseActionFields,
    "sEntityNameBlackboard": common_types.StrId,
})

behaviortree_CtargetIsHangingInMyPlatformCondition = Object(behaviortree_CBaseConditionFields)

char = Object({})


class cutscene_ETakePlayMode(enum.IntEnum):
    Once = 0
    Loop = 1
    Wait = 2
    Invalid = 2147483647


construct_cutscene_ETakePlayMode = StrictEnum(cutscene_ETakePlayMode)


class darkness_EDarknessPreset(enum.IntEnum):
    DISABLED = 0
    ENABLED = 1
    CENTRAL_UNIT = 2


construct_darkness_EDarknessPreset = StrictEnum(darkness_EDarknessPreset)

double = Object({})

engine_render_anim_CSkeletalAnimTree = Object(base_animation_ISkeletonTransformerFields)

engine_scene_CScene = Object({})

engine_scene_CScenePtr = Pointer_engine_scene_CScene.create_construct()

engine_scene_CSceneManager = Object({
    "vSlots": base_global_CRntVector_engine_scene_CSceneSlotPtr_,
})

engine_scene_CSceneSlot = Object({
    "pScene": engine_scene_CScenePtr,
})

engine_scene_sceneItems_CSceneGroup = Object({
    "oName": common_types.StrId,
})


class engine_scene_sceneItems_EItemType(enum.IntEnum):
    SCENE_BLOCK = 0
    OBJECT = 1
    LIGHT = 2
    COUNT = 3
    INVALID = 4
    Invalid = 2147483647


construct_engine_scene_sceneItems_EItemType = StrictEnum(engine_scene_sceneItems_EItemType)


class game_curves_EProcessorType(enum.IntEnum):
    Base = 0
    PostProcess_DOF = 1
    Variables = 2
    SceneParam = 3
    MaterialProperty = 4
    MaterialColor = 5
    FxMaterialColor = 6
    FxMaterialProperty = 7
    SceneParamDirtMaskMult = 8
    SceneParamColorTint = 9
    PostProcess_BloomFactor = 10
    PostProcess_SelfIlumFactor = 11
    PostProcess_MotionBlur = 12
    LightIntensity = 13
    PostProcess_AnamorphicBloomFactor = 14
    AI = 15
    Invalid = 2147483647


construct_game_curves_EProcessorType = StrictEnum(game_curves_EProcessorType)

game_logic_collision_CShape = Object(game_logic_collision_CShapeFields := {
    "vPos": common_types.CVector3D,
    "bIsSolid": construct.Flag,
})

game_logic_collision_CAABoxShape2D = Object({
    **game_logic_collision_CShapeFields,
    "v2Min": common_types.CVector2D,
    "v2Max": common_types.CVector2D,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CBroadphaseObject = Object(game_logic_collision_CBroadphaseObjectFields := {
    **CGameObjectFields,
    "sId": common_types.UInt,
    "sStrId": common_types.StrId,
})

game_logic_collision_CCapsuleShape2D = Object({
    **game_logic_collision_CShapeFields,
    "fRadius": common_types.Float,
    "fHalfHeight": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CCircleShape2D = Object({
    **game_logic_collision_CShapeFields,
    "fRadius": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CShapePtr = Pointer_game_logic_collision_CShape.create_construct()

game_logic_collision_CCollider = Object({
    **game_logic_collision_CBroadphaseObjectFields,
    "pShape": game_logic_collision_CShapePtr,
})

game_logic_collision_CColliderGroup = Object(game_logic_collision_CBroadphaseObjectFields)

game_logic_collision_CCollisionImporter = Object({})

game_logic_collision_COBoxShape2D = Object({
    **game_logic_collision_CShapeFields,
    "v2Extent": common_types.CVector2D,
    "fDegrees": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CPolygonCollectionShape = Object({
    **game_logic_collision_CShapeFields,
    "oPolyCollection": base_spatial_CPolygonCollection2D,
})

game_logic_collision_CTrigger = Object(CGameObjectFields)

gameeditor_CGameModelQueryBoard = Object({
    "ActorLnk": common_types.StrId,
    "Int32": common_types.Int,
    "UInt32": common_types.UInt,
    "SizeT": construct.Int64ul,
    "Float32": common_types.Float,
})

sound_CSoundManagerPtr = Pointer_sound_CSoundManager.create_construct()

sound_CMusicManagerPtr = Pointer_sound_CMusicManager.create_construct()

gameeditor_CGameModelRoot = Object({
    "pScenario": CScenarioPtr,
    "pSubareaManager": CSubAreaManagerPtr,
    "pEnvironmentManager": CEnvironmentManagerPtr,
    "pSoundManager": sound_CSoundManagerPtr,
    "pShotManager": CShotManagerPtr,
    "pLightManager": CLightManagerPtr,
    "pMusicManager": sound_CMusicManagerPtr,
})


class gameeditor_EEditorModeDataFlow(enum.IntEnum):
    NONE = 0
    EDITOR_TO_GAME = 1
    GAME_TO_EDITOR = 2
    BIDIRECTIONAL = 3
    Invalid = 2147483647


construct_gameeditor_EEditorModeDataFlow = StrictEnum(gameeditor_EEditorModeDataFlow)


class gameeditor_EPersistenceTarget(enum.IntEnum):
    Logic = 0
    Logic_Layer_RAL = 1
    Logic_Sublayer_RASL = 2
    Logic_Folders_RLEI = 3
    Sublayer_Folders_RASLEI = 4
    Environment_Data = 5
    Subareas = 6
    Editor = 7
    Audio_Presets = 8
    Collision_Material_Data = 9
    Music_Presets_Data = 10
    Invalid = 2147483647


construct_gameeditor_EPersistenceTarget = StrictEnum(gameeditor_EPersistenceTarget)

gameeditor_TPropertyId = Object({})

long = Object({})

luaDisplayObject = Object({})

luaGameObject = Object({})

media_CMediaStream = Object(media_CMediaStreamFields := {})

media_CAtkSoundStream = Object(media_CMediaStreamFields)

media_CMovieStreamNx = Object(media_CMovieStreamNxFields := media_CMediaStreamFields)

media_CMovieAudioStreamNx = Object(media_CMovieStreamNxFields)

media_CMoviePlayer = Object({})

media_CMovieVideoStreamNx = Object(media_CMovieStreamNxFields)


class media_EMovieStatus(enum.IntEnum):
    Unknown = 0
    Success = 1
    InRequestedState = 2
    InvalidTransition = 3
    AsyncWork = 4
    Error = 5
    Invalid = 2147483647


construct_media_EMovieStatus = StrictEnum(media_EMovieStatus)

minimap_CAnimatedValue_SAnimConfig = Object({
    "fIniValue": common_types.Float,
    "fEndValue": common_types.Float,
    "fAnimTime": common_types.Float,
    "strInterpFunc": common_types.StrId,
})


class minimap_EIconAnimID(enum.IntEnum):
    SHOW = 0
    SELECT = 1
    SAMUS_GLOW = 2
    ITEM_SPHERE = 3
    ITEM_CUBE = 4
    ITEM_GLOW = 5
    TELEPORTER_GLOW = 6
    TRANSLUCID = 7
    INVISIBLE = 8
    EMMY_SHOW = 9
    EMMY_GLOW = 10
    HYPERBEAM_GLOW = 11
    Invalid = 2147483647


construct_minimap_EIconAnimID = StrictEnum(minimap_EIconAnimID)


class msapi_api_idx_EDataType(enum.IntEnum):
    E_DATATYPE_INVALID = 0
    E_BYTE = 1
    E_SHORT = 2
    E_INT = 3
    E_DATATYPE_COUNT = 4


construct_msapi_api_idx_EDataType = StrictEnum(msapi_api_idx_EDataType)


class msapi_api_idx_EPrimitiveType(enum.IntEnum):
    E_PRIMITIVE_INVALID = 0
    E_TRIANGLES = 1
    E_TRIANGLE_STRIP = 2
    E_TRIANGLE_FAN = 3
    E_LINES = 4
    E_LINE_STRIP = 5
    E_PRIMITIVE_COUNT = 6


construct_msapi_api_idx_EPrimitiveType = StrictEnum(msapi_api_idx_EPrimitiveType)


class msapi_api_rs_ERenderStateValue(enum.IntEnum):
    E_FALSE = 0
    E_TRUE = 1
    E_CULL_CW = 2
    E_CULL_CCW = 3
    E_CULL_NONE = 4
    E_CMP_LESS = 5
    E_CMP_NEVER = 6
    E_CMP_EQUA = 7
    E_CMP_LESSEQUAL = 8
    E_CMP_GREATER = 9
    E_CMP_NOTEQUAL = 10
    E_CMP_GREATEREQUAL = 11
    E_CMP_ALWAYS = 12
    E_STENCILCAPS_KEEP = 13
    E_STENCILCAPS_ZERO = 14
    E_STENCILCAPS_REPLACE = 15
    E_STENCILCAPS_INCRSAT = 16
    E_STENCILCAPS_DECRSAT = 17
    E_STENCILCAPS_INVERT = 18
    E_STENCILCAPS_INCR = 19
    E_STENCILCAPS_DECR = 20
    E_STENCILCAPS_2SIDED = 21
    E_STENCILOP_KEEP = 22
    E_STENCILOP_REPLACE = 23
    ERENDERSTATEVALUE_INVALID = 4294967295


construct_msapi_api_rs_ERenderStateValue = StrictEnum(msapi_api_rs_ERenderStateValue)


class msapi_api_tex_EArrangement(enum.IntEnum):
    E_ARRANGE_INVALID = 0
    E_ARRANGE_RAW_INTERLEAVED = 1
    E_ARRANGE_RAW_COMPONENTS = 2
    E_ARRANGE_COMPRESSED = 3
    EARRAGEMENT_INVALID = 4294967295


construct_msapi_api_tex_EArrangement = StrictEnum(msapi_api_tex_EArrangement)


class msapi_api_tex_EComponents(enum.IntEnum):
    E_COMPONENTS_INVALID = 0
    E_COMPONENTS_R8_G8_B8 = 1
    E_COMPONENTS_R8_G8_B8_A8 = 2
    E_COMPONENTS_A8 = 3
    E_COMPONENTS_L8 = 4
    E_COMPONENTS_L8_A8 = 5
    E_COMPONENTS_R5_G6_B5 = 6
    E_COMPONENTS_R5_G5_B5_A1 = 7
    E_COMPONENTS_R4_G4_B4_A4 = 8
    E_COMPONENTS_A4 = 9
    E_COMPONENTS_L4 = 10
    E_COMPONENTS_L4_A4 = 11
    E_COMPONENTS_U8_V8 = 12
    E_COMPONENTS_U16_V16 = 13
    E_COMPONENTS_R8_G8_B8_X8 = 14
    E_COMPONENTS_R32F = 16
    ECOMPONENTS_INVALID = 4294967295


construct_msapi_api_tex_EComponents = StrictEnum(msapi_api_tex_EComponents)


class msapi_api_tex_EFiltering(enum.IntEnum):
    E_FILTER_NEAREST = 0
    E_FILTER_LINEAR = 1
    E_FILTER_NEARESTMIPNEAREST = 2
    E_FILTER_NEARESTMIPLINEAR = 3
    E_FILTER_LINEARMIPNEAREST = 4
    E_FILTER_LINEARMIPLINEAR = 5
    EFILTER_INVALID = 4294967295


construct_msapi_api_tex_EFiltering = StrictEnum(msapi_api_tex_EFiltering)


class msapi_api_tex_ETiling(enum.IntEnum):
    E_TILING_CLAMP = 0
    E_TILING_CLAMPCOLOR = 1
    E_TILING_REPEAT = 2
    E_TILING_MIRROR = 3
    ETILING_INVALID = 4294967295


construct_msapi_api_tex_ETiling = StrictEnum(msapi_api_tex_ETiling)


class msapi_api_types_blendFactor_EBlendFactor(enum.IntEnum):
    E_BLENDFACTOR_ZERO = 0
    E_BLENDFACTOR_ONE = 1
    E_BLENDFACTOR_SRC_COLOR = 2
    E_BLENDFACTOR_INV_SRC_COLOR = 3
    E_BLENDFACTOR_DST_COLOR = 4
    E_BLENDFACTOR_INV_DST_COLOR = 5
    E_BLENDFACTOR_SRC_ALPHA = 6
    E_BLENDFACTOR_INV_SRC_ALPHA = 7
    E_BLENDFACTOR_DST_ALPHA = 8
    E_BLENDFACTOR_INV_DST_ALPHA = 9
    E_MAX_BLENDFACTOR_COUNT = 10
    EBLENDFACTOR_INVALID = 4294967295


construct_msapi_api_types_blendFactor_EBlendFactor = StrictEnum(msapi_api_types_blendFactor_EBlendFactor)


class msapi_api_types_blendOp_EBlendOp(enum.IntEnum):
    E_BLENDOP_ADD = 0
    E_BLENDOP_SUBDST = 1
    E_BLENDOP_SUBSRC = 2
    E_BLENDOP_MIN = 3
    E_BLENDOP_MAX = 4
    E_MAX_BLENDOP_COUNT = 5
    EBLENDOP_INVALID = 4294967295


construct_msapi_api_types_blendOp_EBlendOp = StrictEnum(msapi_api_types_blendOp_EBlendOp)


class msapi_api_types_cmpMode_ECmpMode(enum.IntEnum):
    E_CMPMODE_ALWAYS = 0
    E_CMPMODE_NEVER = 1
    E_CMPMODE_EQUAL = 2
    E_CMPMODE_NOTEQUAL = 3
    E_CMPMODE_LESS = 4
    E_CMPMODE_LESSEQUAL = 5
    E_CMPMODE_GREATER = 6
    E_CMPMODE_GREATEREQUAL = 7
    E_MAX_CMPMODE_COUNT = 8
    ECMPMODE_INVALID = 4294967295


construct_msapi_api_types_cmpMode_ECmpMode = StrictEnum(msapi_api_types_cmpMode_ECmpMode)


class msapi_api_types_cullMode_ECullMode(enum.IntEnum):
    E_CULLMODE_CW = 2
    E_CULLMODE_CCW = 3
    E_CULLMODE_NONE = 4
    E_MAX_CULLMODE_COUNT = 5
    ECULLMODE_INVALID = 4294967295


construct_msapi_api_types_cullMode_ECullMode = StrictEnum(msapi_api_types_cullMode_ECullMode)


class msapi_api_types_fillMode_EFillMode(enum.IntEnum):
    E_FILLMODE_SOLID = 0
    E_FILLMODE_WIRE = 1
    E_FILLMODE_INVALID = 4294967295


construct_msapi_api_types_fillMode_EFillMode = StrictEnum(msapi_api_types_fillMode_EFillMode)


class msapi_api_types_stencilOp_EStencilOp(enum.IntEnum):
    E_STENCILOP_KEEP = 0
    E_STENCILOP_ZERO = 1
    E_STENCILOP_REPLACE = 2
    E_STENCILOP_INCRSAT = 3
    E_STENCILOP_DECRSAT = 4
    E_STENCILOP_INVERT = 5
    E_STENCILOP_INCR = 6
    E_STENCILOP_DECR = 7
    E_MAX_STENCILOP_COUNT = 8
    ESTENCILOP_INVALID = 4294967295


construct_msapi_api_types_stencilOp_EStencilOp = StrictEnum(msapi_api_types_stencilOp_EStencilOp)


class msapi_api_types_textureAddress_ETextureAddress(enum.IntEnum):
    E_TEXTUREADDRESS_REPEAT = 2
    E_TEXTUREADDRESS_MIRROR = 3
    E_TEXTUREADDRESS_EDGE = 0
    E_TEXTUREADDRESS_BORDER = 1
    ETEXTUREADDRESS_INVALID = 4294967295


construct_msapi_api_types_textureAddress_ETextureAddress = StrictEnum(msapi_api_types_textureAddress_ETextureAddress)


class msapi_api_types_textureFilter_ETextureFilter(enum.IntEnum):
    E_TEXTUREFILTER_NONE = 0
    E_TEXTUREFILTER_POINT = 1
    E_TEXTUREFILTER_LINEAR = 2
    E_TEXTUREFILTER_ANISOTROPIC = 3
    ETEXTUREFILTER_INVALID = 4294967295


construct_msapi_api_types_textureFilter_ETextureFilter = StrictEnum(msapi_api_types_textureFilter_ETextureFilter)


class msapi_material_ETranslucencyType(enum.IntEnum):
    E_TRANSLUCENCY_NONE = 0
    E_TRANSLUCENCY_OPAQUE = 1
    E_TRANSLUCENCY_TRANSLUCENT = 2
    E_TRANSLUCENCY_SUBSTRACTIVE = 4
    E_TRANSLUCENCY_ADDITIVE = 8
    E_TRANSLUCENCY_OPAQUE_FWD = 16
    E_TRANSLUCENCY_ALL = 31
    E_TRANSLUCENCY_NOT_OPAQUE = 14
    ETRANSLUCENCY_INVALID = 4294967295


construct_msapi_material_ETranslucencyType = StrictEnum(msapi_material_ETranslucencyType)

msapi_material_CMaterial = Object({
    **base_core_CBaseObjectFields,
    "sId": common_types.StrId,
    "eType": construct_msapi_material_ETranslucencyType,
    "uRenderLayer": common_types.UInt,
    "sProgramName": common_types.StrId,
})

msapi_material_SAlpha = Object({
    **base_core_CBaseObjectFields,
    "bEnabled": construct.Flag,
    "eFunction": construct_msapi_api_types_cmpMode_ECmpMode,
    "fRef": common_types.Float,
})

msapi_material_SBlend = Object({
    **base_core_CBaseObjectFields,
    "bEnabled": construct.Flag,
    "eOp": construct_msapi_api_types_blendOp_EBlendOp,
    "eSrc": construct_msapi_api_types_blendFactor_EBlendFactor,
    "eDst": construct_msapi_api_types_blendFactor_EBlendFactor,
})

msapi_material_SConstant = Object({
    **base_core_CBaseObjectFields,
    "sId": common_types.StrId,
    "cType": char,
})

msapi_material_SCull = Object({
    **base_core_CBaseObjectFields,
    "eMode": construct_msapi_api_types_cullMode_ECullMode,
})

msapi_material_SDepth = Object({
    **base_core_CBaseObjectFields,
    "bTest": construct.Flag,
    "bWrite": construct.Flag,
    "eTestMode": construct_msapi_api_types_cmpMode_ECmpMode,
    "bZPrepass": construct.Flag,
})

msapi_material_SFill = Object({
    **base_core_CBaseObjectFields,
    "eFillMode": construct_msapi_api_types_fillMode_EFillMode,
})

msapi_material_SStage = Object({
    **base_core_CBaseObjectFields,
    "eType": construct_msapi_api_shdr_EShaderType,
})

msapi_material_SStencil = Object({
    **base_core_CBaseObjectFields,
    "bEnabled": construct.Flag,
    "uMask": common_types.UInt,
    "uRef": common_types.UInt,
    "eStencilFail": construct_msapi_api_types_stencilOp_EStencilOp,
    "eStencilPass": construct_msapi_api_types_stencilOp_EStencilOp,
    "eStencilDepthFail": construct_msapi_api_types_stencilOp_EStencilOp,
    "eStencilDepthPass": construct_msapi_api_types_stencilOp_EStencilOp,
    "eStencilCmpMode": construct_msapi_api_types_cmpMode_ECmpMode,
})

msapi_material_STexture = Object({
    **base_core_CBaseObjectFields,
    "sId": common_types.StrId,
    "sSampler": common_types.StrId,
    "sType": common_types.StrId,
    "iSlot": common_types.Int,
    "sAddress": common_types.StrId,
    "eMinFilter": construct_msapi_api_types_textureFilter_ETextureFilter,
    "eMagFilter": construct_msapi_api_types_textureFilter_ETextureFilter,
    "eMipFilter": construct_msapi_api_types_textureFilter_ETextureFilter,
    "eCompMode": construct_msapi_api_types_cmpMode_ECmpMode,
    "eWrapModeU": construct_msapi_api_types_textureAddress_ETextureAddress,
    "eWrapModeV": construct_msapi_api_types_textureAddress_ETextureAddress,
    "uBorderColor": common_types.UInt,
    "fMinLod": common_types.Float,
    "fLodBias": common_types.Float,
    "fAnisotropic": common_types.Float,
    "fMaxMipLevel": common_types.Float,
    "fMaxAnisotropy": common_types.Float,
})

msapi_res_CCameraAnimationResource = Object({})

msapi_res_CFontResource = Object({})

msapi_res_CGlyphTableResource = Object({})

msapi_res_CLightResource = Object({})

msapi_res_CModelResource = Object({})

msapi_res_CParticleSystemResource = Object({})

msapi_res_CProgramResource = Object({})

msapi_res_CRenderRes = Object(base_res_CResFields)

msapi_res_CTextureResource = Object({})

navmesh_CDynamicSmartLinkGroup = Object({
    **base_core_CAssetFields,
    "bGenerateInNavMesh": construct.Flag,
    "vLinkResources": base_global_CRntVector_navmesh_CDynamicSmartLinkGroup_SDynamicSmartLinkRulesSet_,
})

navmesh_CDynamicSmartLinkRule = Object(navmesh_CDynamicSmartLinkRuleFields := CGameObjectFields)

navmesh_CDynamicSmartLinkRules = Object(base_core_CAssetFields)

navmesh_CFixedDynamicSmartLinkRule = Object(navmesh_CDynamicSmartLinkRuleFields)

navmesh_CNavMesh = Object(CGameObjectFields)

navmesh_CNavMeshGenerator = Object(CGameObjectFields)

navmesh_SNavMeshPath = Object(IPathFields)

querysystem_CEvaluator = Object(querysystem_CEvaluatorFields := {
    "fWeight": common_types.Float,
    "sFunction": common_types.StrId,
})

querysystem_CChozoRobotSoldierHeightEvaluator = Object(querysystem_CEvaluatorFields)

querysystem_CFilter = Object(querysystem_CFilterFields := {
    "bNegate": construct.Flag,
})

querysystem_CChozoRobotSoldierIsInFrustumFilter = Object(querysystem_CFilterFields)

querysystem_CChozoRobotSoldierIsInMeleePathFilter = Object(querysystem_CFilterFields)

querysystem_CChozoRobotSoldierIsInShootingPositionPathFilter = Object(querysystem_CFilterFields)

querysystem_CChozoRobotSoldierLineOfFireFilter = Object(querysystem_CFilterFields)

querysystem_CMinTargetDistanceFilter = Object(querysystem_CMinTargetDistanceFilterFields := {
    **querysystem_CFilterFields,
    "fMinDistance": common_types.Float,
})

querysystem_CChozoRobotSoldierMinTargetDistanceFilter = Object(querysystem_CMinTargetDistanceFilterFields)

querysystem_CCurrentEvaluator = Object(querysystem_CEvaluatorFields)

querysystem_CDistanceEvaluator = Object({
    **querysystem_CEvaluatorFields,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
})

querysystem_CDistanceToTargetEvaluator = Object({
    **querysystem_CEvaluatorFields,
    "fMinDistance": common_types.Float,
    "fMaxDistance": common_types.Float,
})

querysystem_CFilterToEvaluator = Object({
    **querysystem_CEvaluatorFields,
    "pFilter": std_unique_ptr_querysystem_CFilter_,
    "fEvaluation": common_types.Float,
})

querysystem_CIsInFrustumFilter = Object({
    **querysystem_CFilterFields,
    "vOffset": common_types.CVector3D,
})

querysystem_CIsInNavigablePathFilter = Object({
    **querysystem_CFilterFields,
    "vOffset": common_types.CVector3D,
})

querysystem_CLookAtTargetFilter = Object({
    **querysystem_CFilterFields,
    "vOffset": common_types.CVector3D,
})

querysystem_CMaxDistanceFilter = Object({
    **querysystem_CFilterFields,
    "fMaxDistance": common_types.Float,
})

querysystem_CMaxTargetDistanceFilter = Object({
    **querysystem_CFilterFields,
    "fMaxTargetDistance": common_types.Float,
})

querysystem_CMinDistanceFilter = Object({
    **querysystem_CFilterFields,
    "fMinDistance": common_types.Float,
})

querysystem_CSameEntitySideFilter = Object({
    **querysystem_CFilterFields,
    "vOffset": common_types.CVector3D,
})

realloc = Object({})

sound_CAudioPresetModifier = Object({
    "fVolume": common_types.Float,
    "fPitch": common_types.Float,
})

sound_CAudioPresets = Object({
    "dicPresets": base_global_CRntDictionary_base_global_CStrId__sound_CAudioPreset_,
})

sound_CAudioPresetsPtr = Pointer_sound_CAudioPresets.create_construct()

sound_CMusicManager = Object({
    "dicGlobalMusicPresets": base_global_CRntDictionary_base_global_CStrId__CEnvironmentMusicData_,
    "dicGlobalBossMusicPresets": base_global_CRntDictionary_base_global_CStrId__sound_TBossMusicPreset_,
})

sound_CMusicManager_CTunableMusicManager = Object({
    **base_tunable_CTunableFields,
    "bNCLCurrentMusicDebugEnable": construct.Flag,
})

sound_CMusicVolumeOverride_CTunableMusicVolumeOverride = Object({
    **base_tunable_CTunableFields,
    "fAccessPoint": common_types.Float,
    "fAqua001": common_types.Float,
    "fAqua002": common_types.Float,
    "fBaseLab001": common_types.Float,
    "fBaseLabBlackOut": common_types.Float,
    "fBossCommander001": common_types.Float,
    "fBossCommander002": common_types.Float,
    "fBossCommander003": common_types.Float,
    "fBossCommanderPresentation": common_types.Float,
    "fBossCommanderX001": common_types.Float,
    "fBossCommanderX002": common_types.Float,
    "fBossCoolDownX": common_types.Float,
    "fBossCoolDownXPresentation": common_types.Float,
    "fBossDefeated": common_types.Float,
    "fBossKraid001": common_types.Float,
    "fBossKraid002": common_types.Float,
    "fBossKraidPresentation": common_types.Float,
    "fBossMidChozoRobotSoldier": common_types.Float,
    "fBossMidChozoWarriorX001": common_types.Float,
    "fBossMidChozoWarriorX002": common_types.Float,
    "fBossScorpius001": common_types.Float,
    "fBossScorpius002": common_types.Float,
    "fBossScorpiusPresentation": common_types.Float,
    "fCave001": common_types.Float,
    "fCave002": common_types.Float,
    "fCave003": common_types.Float,
    "fCaveCooldDown": common_types.Float,
    "fCaveThermalDevice": common_types.Float,
    "fCentralUnitPhase1": common_types.Float,
    "fCentralUnitPhase2": common_types.Float,
    "fCommanderOutro": common_types.Float,
    "fEmmyChase": common_types.Float,
    "fEmmyDefeated": common_types.Float,
    "fEmmyDefeatedBaselab": common_types.Float,
    "fEmmyDefeatedForest": common_types.Float,
    "fEmmyDefeatedMagma": common_types.Float,
    "fEmmyDefeatedSanctuary": common_types.Float,
    "fEmmyDefeatedShipyard": common_types.Float,
    "fEmmyPatrol": common_types.Float,
    "fEmmySearch": common_types.Float,
    "fEncounterProfessor": common_types.Float,
    "fEndGame": common_types.Float,
    "fEndScreen": common_types.Float,
    "fEscapeSequence": common_types.Float,
    "fForest001": common_types.Float,
    "fGameOver": common_types.Float,
    "fHydrogiga001": common_types.Float,
    "fHydrogiga002": common_types.Float,
    "fJingleItemGet": common_types.Float,
    "fJingleItemGetUnknown": common_types.Float,
    "fJinglePowerUpGet": common_types.Float,
    "fJingleTojo": common_types.Float,
    "fMagma001": common_types.Float,
    "fMagma002": common_types.Float,
    "fMagmaCoolDown": common_types.Float,
    "fMapStation": common_types.Float,
    "fOpening": common_types.Float,
    "fPowerBomb": common_types.Float,
    "fProfessorX": common_types.Float,
    "fQuarantine001": common_types.Float,
    "fSamusStory": common_types.Float,
    "fSancEmmyPresentation": common_types.Float,
    "fSancturary001": common_types.Float,
    "fSaveStation": common_types.Float,
    "fShipyard001": common_types.Float,
    "fSkybase001": common_types.Float,
    "fStaffRoll": common_types.Float,
    "fStatueRoom": common_types.Float,
    "fStrongReaction": common_types.Float,
    "fSuperGoliathX": common_types.Float,
    "fSuperQuetzoaX": common_types.Float,
    "fTitleScreen": common_types.Float,
    "fTrainStation": common_types.Float,
    "sName": common_types.StrId,
})

sound_CSoundEventsDef = Object({
    **base_core_CAssetFields,
    "aSoundEventRules": TSoundEventRules,
})

std_unique_ptr_sound_CSoundEventsDef_SSoundEventsSelector_ = Pointer_sound_CSoundEventsDef_SSoundEventsSelector.create_construct()

sound_CSoundEventsDef_SSoundEventsRule = Object({
    "pContextSelector": std_unique_ptr_sound_CSoundEventsDef_SSoundEventsSelector_,
    "mapSoundEvents": base_global_CRntSmallDictionary_base_global_CStrId__base_core_CAssetLink_,
})

sound_CSoundEventsDef_SSoundEventsSelector = Object(sound_CSoundEventsDef_SSoundEventsSelectorFields := {
    "strSelectorDesc": common_types.StrId,
})

sound_CSoundManager = Object({
    "pAudioPresets": sound_CAudioPresetsPtr,
})

sound_SGUISoundEventsSelector = Object({
    **sound_CSoundEventsDef_SSoundEventsSelectorFields,
    "strTargetFilter": common_types.StrId,
})

Pointer_CAcidBlobsLaunchPattern.add_option("CAcidBlobsLaunchPattern", CAcidBlobsLaunchPattern)

Pointer_CActor.add_option("CActor", CActor)
Pointer_CActor.add_option("CEntity", CEntity)

Pointer_CActorComponent.add_option("CActorComponent", CActorComponent)
Pointer_CActorComponent.add_option("CAIAttackComponent", CAIAttackComponent)
Pointer_CActorComponent.add_option("CAIComponent", CAIComponent)
Pointer_CActorComponent.add_option("CAIGrapplePointComponent", CAIGrapplePointComponent)
Pointer_CActorComponent.add_option("CAINavigationComponent", CAINavigationComponent)
Pointer_CActorComponent.add_option("CAISmartObjectComponent", CAISmartObjectComponent)
Pointer_CActorComponent.add_option("CAbilityComponent", CAbilityComponent)
Pointer_CActorComponent.add_option("CAccessPointCommanderComponent", CAccessPointCommanderComponent)
Pointer_CActorComponent.add_option("CAccessPointComponent", CAccessPointComponent)
Pointer_CActorComponent.add_option("CActionSwitcherComponent", CActionSwitcherComponent)
Pointer_CActorComponent.add_option("CActionSwitcherOnPullGrapplePointComponent", CActionSwitcherOnPullGrapplePointComponent)
Pointer_CActorComponent.add_option("CActivatableByProjectileComponent", CActivatableByProjectileComponent)
Pointer_CActorComponent.add_option("CActivatableComponent", CActivatableComponent)
Pointer_CActorComponent.add_option("CAimCameraEnabledVisibleOnlyComponent", CAimCameraEnabledVisibleOnlyComponent)
Pointer_CActorComponent.add_option("CAimComponent", CAimComponent)
Pointer_CActorComponent.add_option("CAlternativeActionPlayerComponent", CAlternativeActionPlayerComponent)
Pointer_CActorComponent.add_option("CAmmoRechargeComponent", CAmmoRechargeComponent)
Pointer_CActorComponent.add_option("CAnimationComponent", CAnimationComponent)
Pointer_CActorComponent.add_option("CAnimationNavMeshItemComponent", CAnimationNavMeshItemComponent)
Pointer_CActorComponent.add_option("CArachnusAIComponent", CArachnusAIComponent)
Pointer_CActorComponent.add_option("CAreaFXComponent", CAreaFXComponent)
Pointer_CActorComponent.add_option("CAreaMusicComponent", CAreaMusicComponent)
Pointer_CActorComponent.add_option("CAreaSoundComponent", CAreaSoundComponent)
Pointer_CActorComponent.add_option("CAttackComponent", CAttackComponent)
Pointer_CActorComponent.add_option("CAudioComponent", CAudioComponent)
Pointer_CActorComponent.add_option("CAutclastAIComponent", CAutclastAIComponent)
Pointer_CActorComponent.add_option("CAutectorAIComponent", CAutectorAIComponent)
Pointer_CActorComponent.add_option("CAutectorLifeComponent", CAutectorLifeComponent)
Pointer_CActorComponent.add_option("CAutomperAIComponent", CAutomperAIComponent)
Pointer_CActorComponent.add_option("CAutoolAIComponent", CAutoolAIComponent)
Pointer_CActorComponent.add_option("CAutsharpAIComponent", CAutsharpAIComponent)
Pointer_CActorComponent.add_option("CAutsharpLifeComponent", CAutsharpLifeComponent)
Pointer_CActorComponent.add_option("CAutsharpSpawnPointComponent", CAutsharpSpawnPointComponent)
Pointer_CActorComponent.add_option("CAutsniperAIComponent", CAutsniperAIComponent)
Pointer_CActorComponent.add_option("CAutsniperSpawnPointComponent", CAutsniperSpawnPointComponent)
Pointer_CActorComponent.add_option("CBTObserverComponent", CBTObserverComponent)
Pointer_CActorComponent.add_option("CBaseBigFistAIComponent", CBaseBigFistAIComponent)
Pointer_CActorComponent.add_option("CBaseDamageTriggerComponent", CBaseDamageTriggerComponent)
Pointer_CActorComponent.add_option("CBaseGroundShockerAIComponent", CBaseGroundShockerAIComponent)
Pointer_CActorComponent.add_option("CBaseLightComponent", CBaseLightComponent)
Pointer_CActorComponent.add_option("CBaseTriggerComponent", CBaseTriggerComponent)
Pointer_CActorComponent.add_option("CBasicLifeComponent", CBasicLifeComponent)
Pointer_CActorComponent.add_option("CBatalloonAIComponent", CBatalloonAIComponent)
Pointer_CActorComponent.add_option("CBeamBoxComponent", CBeamBoxComponent)
Pointer_CActorComponent.add_option("CBeamDoorLifeComponent", CBeamDoorLifeComponent)
Pointer_CActorComponent.add_option("CBehaviorTreeAIComponent", CBehaviorTreeAIComponent)
Pointer_CActorComponent.add_option("CBigFistAIComponent", CBigFistAIComponent)
Pointer_CActorComponent.add_option("CBigkranXAIComponent", CBigkranXAIComponent)
Pointer_CActorComponent.add_option("CBillboardCollisionComponent", CBillboardCollisionComponent)
Pointer_CActorComponent.add_option("CBillboardComponent", CBillboardComponent)
Pointer_CActorComponent.add_option("CBillboardLifeComponent", CBillboardLifeComponent)
Pointer_CActorComponent.add_option("CBombMovement", CBombMovement)
Pointer_CActorComponent.add_option("CBoneToConstantComponent", CBoneToConstantComponent)
Pointer_CActorComponent.add_option("CBossAIComponent", CBossAIComponent)
Pointer_CActorComponent.add_option("CBossLifeComponent", CBossLifeComponent)
Pointer_CActorComponent.add_option("CBossSpawnGroupComponent", CBossSpawnGroupComponent)
Pointer_CActorComponent.add_option("CBreakableHintComponent", CBreakableHintComponent)
Pointer_CActorComponent.add_option("CBreakableScenarioComponent", CBreakableScenarioComponent)
Pointer_CActorComponent.add_option("CBreakableTileGroupComponent", CBreakableTileGroupComponent)
Pointer_CActorComponent.add_option("CBreakableTileGroupSonarTargetComponent", CBreakableTileGroupSonarTargetComponent)
Pointer_CActorComponent.add_option("CBreakableVignetteComponent", CBreakableVignetteComponent)
Pointer_CActorComponent.add_option("CCameraComponent", CCameraComponent)
Pointer_CActorComponent.add_option("CCameraRailComponent", CCameraRailComponent)
Pointer_CActorComponent.add_option("CCapsuleUsableComponent", CCapsuleUsableComponent)
Pointer_CActorComponent.add_option("CCaterzillaAIComponent", CCaterzillaAIComponent)
Pointer_CActorComponent.add_option("CCaterzillaSpawnPointComponent", CCaterzillaSpawnPointComponent)
Pointer_CActorComponent.add_option("CCaveCentralUnitComponent", CCaveCentralUnitComponent)
Pointer_CActorComponent.add_option("CCentralUnitAIComponent", CCentralUnitAIComponent)
Pointer_CActorComponent.add_option("CCentralUnitCannonAIComponent", CCentralUnitCannonAIComponent)
Pointer_CActorComponent.add_option("CCentralUnitCannonBeamMovementComponent", CCentralUnitCannonBeamMovementComponent)
Pointer_CActorComponent.add_option("CCentralUnitComponent", CCentralUnitComponent)
Pointer_CActorComponent.add_option("CChainReactionActionSwitcherComponent", CChainReactionActionSwitcherComponent)
Pointer_CActorComponent.add_option("CChangeStageNavMeshItemComponent", CChangeStageNavMeshItemComponent)
Pointer_CActorComponent.add_option("CCharacterLifeComponent", CCharacterLifeComponent)
Pointer_CActorComponent.add_option("CCharacterMovement", CCharacterMovement)
Pointer_CActorComponent.add_option("CChozoCommanderAIComponent", CChozoCommanderAIComponent)
Pointer_CActorComponent.add_option("CChozoCommanderEnergyShardsFragmentMovementComponent", CChozoCommanderEnergyShardsFragmentMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderEnergyShardsSphereMovementComponent", CChozoCommanderEnergyShardsSphereMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderSentenceSphereLifeComponent", CChozoCommanderSentenceSphereLifeComponent)
Pointer_CActorComponent.add_option("CChozoCommanderSentenceSphereMovementComponent", CChozoCommanderSentenceSphereMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderXLifeComponent", CChozoCommanderXLifeComponent)
Pointer_CActorComponent.add_option("CChozoRobotSoldierAIComponent", CChozoRobotSoldierAIComponent)
Pointer_CActorComponent.add_option("CChozoRobotSoldierBeamMovementComponent", CChozoRobotSoldierBeamMovementComponent)
Pointer_CActorComponent.add_option("CChozoWarriorAIComponent", CChozoWarriorAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorEliteAIComponent", CChozoWarriorEliteAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXAIComponent", CChozoWarriorXAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXEliteAIComponent", CChozoWarriorXEliteAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXSpitMovementComponent", CChozoWarriorXSpitMovementComponent)
Pointer_CActorComponent.add_option("CChozoZombieXAIComponent", CChozoZombieXAIComponent)
Pointer_CActorComponent.add_option("CChozoZombieXSpawnPointComponent", CChozoZombieXSpawnPointComponent)
Pointer_CActorComponent.add_option("CChozombieFXComponent", CChozombieFXComponent)
Pointer_CActorComponent.add_option("CColliderTriggerComponent", CColliderTriggerComponent)
Pointer_CActorComponent.add_option("CCollisionComponent", CCollisionComponent)
Pointer_CActorComponent.add_option("CCollisionMaterialCacheComponent", CCollisionMaterialCacheComponent)
Pointer_CActorComponent.add_option("CComponent", CComponent)
Pointer_CActorComponent.add_option("CConstantMovement", CConstantMovement)
Pointer_CActorComponent.add_option("CCooldownXBossAIComponent", CCooldownXBossAIComponent)
Pointer_CActorComponent.add_option("CCooldownXBossFireBallMovementComponent", CCooldownXBossFireBallMovementComponent)
Pointer_CActorComponent.add_option("CCooldownXBossWeakPointLifeComponent", CCooldownXBossWeakPointLifeComponent)
Pointer_CActorComponent.add_option("CCoreXAIComponent", CCoreXAIComponent)
Pointer_CActorComponent.add_option("CCubeMapComponent", CCubeMapComponent)
Pointer_CActorComponent.add_option("CCutsceneComponent", CCutsceneComponent)
Pointer_CActorComponent.add_option("CCutsceneTriggerComponent", CCutsceneTriggerComponent)
Pointer_CActorComponent.add_option("CDaivoAIComponent", CDaivoAIComponent)
Pointer_CActorComponent.add_option("CDaivoSwarmControllerComponent", CDaivoSwarmControllerComponent)
Pointer_CActorComponent.add_option("CDamageComponent", CDamageComponent)
Pointer_CActorComponent.add_option("CDamageTriggerComponent", CDamageTriggerComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockActivatableActorLifeComponent", CDemolitionBlockActivatableActorLifeComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockComponent", CDemolitionBlockComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockLifeComponent", CDemolitionBlockLifeComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockSonarTargetComponent", CDemolitionBlockSonarTargetComponent)
Pointer_CActorComponent.add_option("CDirLightComponent", CDirLightComponent)
Pointer_CActorComponent.add_option("CDizzeanSwarmControllerComponent", CDizzeanSwarmControllerComponent)
Pointer_CActorComponent.add_option("CDoorCentralUnitLifeComponent", CDoorCentralUnitLifeComponent)
Pointer_CActorComponent.add_option("CDoorEmmyFXComponent", CDoorEmmyFXComponent)
Pointer_CActorComponent.add_option("CDoorGrapplePointComponent", CDoorGrapplePointComponent)
Pointer_CActorComponent.add_option("CDoorLifeComponent", CDoorLifeComponent)
Pointer_CActorComponent.add_option("CDoorShieldLifeComponent", CDoorShieldLifeComponent)
Pointer_CActorComponent.add_option("CDredhedAIComponent", CDredhedAIComponent)
Pointer_CActorComponent.add_option("CDredhedAttackComponent", CDredhedAttackComponent)
Pointer_CActorComponent.add_option("CDropComponent", CDropComponent)
Pointer_CActorComponent.add_option("CDroppableComponent", CDroppableComponent)
Pointer_CActorComponent.add_option("CDroppableLifeComponent", CDroppableLifeComponent)
Pointer_CActorComponent.add_option("CDroppableMissileComponent", CDroppableMissileComponent)
Pointer_CActorComponent.add_option("CDroppablePowerBombComponent", CDroppablePowerBombComponent)
Pointer_CActorComponent.add_option("CDroppableSpecialEnergyComponent", CDroppableSpecialEnergyComponent)
Pointer_CActorComponent.add_option("CDropterAIComponent", CDropterAIComponent)
Pointer_CActorComponent.add_option("CDummyAIComponent", CDummyAIComponent)
Pointer_CActorComponent.add_option("CDummyMovement", CDummyMovement)
Pointer_CActorComponent.add_option("CDummyPullableGrapplePointComponent", CDummyPullableGrapplePointComponent)
Pointer_CActorComponent.add_option("CElectricGeneratorComponent", CElectricGeneratorComponent)
Pointer_CActorComponent.add_option("CElectricReactionComponent", CElectricReactionComponent)
Pointer_CActorComponent.add_option("CElectrifyingAreaComponent", CElectrifyingAreaComponent)
Pointer_CActorComponent.add_option("CElevatorCommanderUsableComponent", CElevatorCommanderUsableComponent)
Pointer_CActorComponent.add_option("CElevatorUsableComponent", CElevatorUsableComponent)
Pointer_CActorComponent.add_option("CEmergencyLightElectricReactionComponent", CEmergencyLightElectricReactionComponent)
Pointer_CActorComponent.add_option("CEmmyAIComponent", CEmmyAIComponent)
Pointer_CActorComponent.add_option("CEmmyAttackComponent", CEmmyAttackComponent)
Pointer_CActorComponent.add_option("CEmmyCaveAIComponent", CEmmyCaveAIComponent)
Pointer_CActorComponent.add_option("CEmmyForestAIComponent", CEmmyForestAIComponent)
Pointer_CActorComponent.add_option("CEmmyLabAIComponent", CEmmyLabAIComponent)
Pointer_CActorComponent.add_option("CEmmyMagmaAIComponent", CEmmyMagmaAIComponent)
Pointer_CActorComponent.add_option("CEmmyMovement", CEmmyMovement)
Pointer_CActorComponent.add_option("CEmmyProtoAIComponent", CEmmyProtoAIComponent)
Pointer_CActorComponent.add_option("CEmmySancAIComponent", CEmmySancAIComponent)
Pointer_CActorComponent.add_option("CEmmyShipyardAIComponent", CEmmyShipyardAIComponent)
Pointer_CActorComponent.add_option("CEmmySpawnPointComponent", CEmmySpawnPointComponent)
Pointer_CActorComponent.add_option("CEmmyValveComponent", CEmmyValveComponent)
Pointer_CActorComponent.add_option("CEmmyWakeUpComponent", CEmmyWakeUpComponent)
Pointer_CActorComponent.add_option("CEmmyWaveMovementComponent", CEmmyWaveMovementComponent)
Pointer_CActorComponent.add_option("CEnemyLifeComponent", CEnemyLifeComponent)
Pointer_CActorComponent.add_option("CEnemyMovement", CEnemyMovement)
Pointer_CActorComponent.add_option("CEnhanceWeakSpotComponent", CEnhanceWeakSpotComponent)
Pointer_CActorComponent.add_option("CEscapeSequenceExplosionComponent", CEscapeSequenceExplosionComponent)
Pointer_CActorComponent.add_option("CEvacuationCountDown", CEvacuationCountDown)
Pointer_CActorComponent.add_option("CEventPropComponent", CEventPropComponent)
Pointer_CActorComponent.add_option("CEventScenarioComponent", CEventScenarioComponent)
Pointer_CActorComponent.add_option("CFXComponent", CFXComponent)
Pointer_CActorComponent.add_option("CFactionComponent", CFactionComponent)
Pointer_CActorComponent.add_option("CFakePhysicsMovement", CFakePhysicsMovement)
Pointer_CActorComponent.add_option("CFanComponent", CFanComponent)
Pointer_CActorComponent.add_option("CFanCoolDownComponent", CFanCoolDownComponent)
Pointer_CActorComponent.add_option("CFingSwarmControllerComponent", CFingSwarmControllerComponent)
Pointer_CActorComponent.add_option("CFireComponent", CFireComponent)
Pointer_CActorComponent.add_option("CFloatingPropActingComponent", CFloatingPropActingComponent)
Pointer_CActorComponent.add_option("CFlockingSwarmControllerComponent", CFlockingSwarmControllerComponent)
Pointer_CActorComponent.add_option("CFloorShockWaveComponent", CFloorShockWaveComponent)
Pointer_CActorComponent.add_option("CFootstepPlatformComponent", CFootstepPlatformComponent)
Pointer_CActorComponent.add_option("CForcedMovementAreaComponent", CForcedMovementAreaComponent)
Pointer_CActorComponent.add_option("CFreezeRoomComponent", CFreezeRoomComponent)
Pointer_CActorComponent.add_option("CFrozenAsFrostbiteComponent", CFrozenAsFrostbiteComponent)
Pointer_CActorComponent.add_option("CFrozenAsPlatformComponent", CFrozenAsPlatformComponent)
Pointer_CActorComponent.add_option("CFrozenComponent", CFrozenComponent)
Pointer_CActorComponent.add_option("CFrozenPlatformComponent", CFrozenPlatformComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineAIComponent", CFulmiteBellyMineAIComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineAttackComponent", CFulmiteBellyMineAttackComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineMovementComponent", CFulmiteBellyMineMovementComponent)
Pointer_CActorComponent.add_option("CFusibleBoxComponent", CFusibleBoxComponent)
Pointer_CActorComponent.add_option("CGobblerAIComponent", CGobblerAIComponent)
Pointer_CActorComponent.add_option("CGobblerSpawnPointComponent", CGobblerSpawnPointComponent)
Pointer_CActorComponent.add_option("CGoliathAIComponent", CGoliathAIComponent)
Pointer_CActorComponent.add_option("CGoliathXAIComponent", CGoliathXAIComponent)
Pointer_CActorComponent.add_option("CGoliathXBurstProjectionBombMovement", CGoliathXBurstProjectionBombMovement)
Pointer_CActorComponent.add_option("CGooplotAIComponent", CGooplotAIComponent)
Pointer_CActorComponent.add_option("CGooshockerAIComponent", CGooshockerAIComponent)
Pointer_CActorComponent.add_option("CGrabComponent", CGrabComponent)
Pointer_CActorComponent.add_option("CGrappleBeamComponent", CGrappleBeamComponent)
Pointer_CActorComponent.add_option("CGrapplePointComponent", CGrapplePointComponent)
Pointer_CActorComponent.add_option("CGroundShockerAIComponent", CGroundShockerAIComponent)
Pointer_CActorComponent.add_option("CGunComponent", CGunComponent)
Pointer_CActorComponent.add_option("CHangableGrappleMagnetSlidingBlockComponent", CHangableGrappleMagnetSlidingBlockComponent)
Pointer_CActorComponent.add_option("CHangableGrapplePointComponent", CHangableGrapplePointComponent)
Pointer_CActorComponent.add_option("CHangableGrappleSurfaceComponent", CHangableGrappleSurfaceComponent)
Pointer_CActorComponent.add_option("CHeatRoomComponent", CHeatRoomComponent)
Pointer_CActorComponent.add_option("CHeatableShieldComponent", CHeatableShieldComponent)
Pointer_CActorComponent.add_option("CHeatableShieldEnhanceWeakSpotComponent", CHeatableShieldEnhanceWeakSpotComponent)
Pointer_CActorComponent.add_option("CHecathonAIComponent", CHecathonAIComponent)
Pointer_CActorComponent.add_option("CHecathonLifeComponent", CHecathonLifeComponent)
Pointer_CActorComponent.add_option("CHecathonPlanktonFXComponent", CHecathonPlanktonFXComponent)
Pointer_CActorComponent.add_option("CHomingMovement", CHomingMovement)
Pointer_CActorComponent.add_option("CHydrogigaAIComponent", CHydrogigaAIComponent)
Pointer_CActorComponent.add_option("CHydrogigaZiplineComponent", CHydrogigaZiplineComponent)
Pointer_CActorComponent.add_option("CHydrogigaZiplineRailComponent", CHydrogigaZiplineRailComponent)
Pointer_CActorComponent.add_option("CHyperBeamBlockLifeComponent", CHyperBeamBlockLifeComponent)
Pointer_CActorComponent.add_option("CIceMissileMovement", CIceMissileMovement)
Pointer_CActorComponent.add_option("CInfesterAIComponent", CInfesterAIComponent)
Pointer_CActorComponent.add_option("CInfesterBallAIComponent", CInfesterBallAIComponent)
Pointer_CActorComponent.add_option("CInfesterBallAttackComponent", CInfesterBallAttackComponent)
Pointer_CActorComponent.add_option("CInfesterBallLifeComponent", CInfesterBallLifeComponent)
Pointer_CActorComponent.add_option("CInfesterBallMovementComponent", CInfesterBallMovementComponent)
Pointer_CActorComponent.add_option("CInputComponent", CInputComponent)
Pointer_CActorComponent.add_option("CInterpolationComponent", CInterpolationComponent)
Pointer_CActorComponent.add_option("CInventoryComponent", CInventoryComponent)
Pointer_CActorComponent.add_option("CItemLifeComponent", CItemLifeComponent)
Pointer_CActorComponent.add_option("CKraidAIComponent", CKraidAIComponent)
Pointer_CActorComponent.add_option("CKraidAcidBlobsMovementComponent", CKraidAcidBlobsMovementComponent)
Pointer_CActorComponent.add_option("CKraidBouncingCreaturesMovementComponent", CKraidBouncingCreaturesMovementComponent)
Pointer_CActorComponent.add_option("CKraidNailMovementComponent", CKraidNailMovementComponent)
Pointer_CActorComponent.add_option("CKraidShockerSplashMovementComponent", CKraidShockerSplashMovementComponent)
Pointer_CActorComponent.add_option("CKraidSpikeMovablePlatformComponent", CKraidSpikeMovablePlatformComponent)
Pointer_CActorComponent.add_option("CLandmarkComponent", CLandmarkComponent)
Pointer_CActorComponent.add_option("CLavaPoolComponent", CLavaPoolComponent)
Pointer_CActorComponent.add_option("CLavaPumpComponent", CLavaPumpComponent)
Pointer_CActorComponent.add_option("CLavapumpThermalReactionComponent", CLavapumpThermalReactionComponent)
Pointer_CActorComponent.add_option("CLifeComponent", CLifeComponent)
Pointer_CActorComponent.add_option("CLifeRechargeComponent", CLifeRechargeComponent)
Pointer_CActorComponent.add_option("CLightingComponent", CLightingComponent)
Pointer_CActorComponent.add_option("CLineBombMovement", CLineBombMovement)
Pointer_CActorComponent.add_option("CLiquidPoolBaseComponent", CLiquidPoolBaseComponent)
Pointer_CActorComponent.add_option("CLiquidSimulationComponent", CLiquidSimulationComponent)
Pointer_CActorComponent.add_option("CLockOnMissileMovement", CLockOnMissileMovement)
Pointer_CActorComponent.add_option("CLogicActionTriggerComponent", CLogicActionTriggerComponent)
Pointer_CActorComponent.add_option("CLogicCameraComponent", CLogicCameraComponent)
Pointer_CActorComponent.add_option("CLogicLookAtPlayerComponent", CLogicLookAtPlayerComponent)
Pointer_CActorComponent.add_option("CLogicPathComponent", CLogicPathComponent)
Pointer_CActorComponent.add_option("CLogicPathNavMeshItemComponent", CLogicPathNavMeshItemComponent)
Pointer_CActorComponent.add_option("CLogicShapeComponent", CLogicShapeComponent)
Pointer_CActorComponent.add_option("CMagmaCentralUnitComponent", CMagmaCentralUnitComponent)
Pointer_CActorComponent.add_option("CMagmaKraidPistonPlatformComponent", CMagmaKraidPistonPlatformComponent)
Pointer_CActorComponent.add_option("CMagmaKraidScenarioControllerComponent", CMagmaKraidScenarioControllerComponent)
Pointer_CActorComponent.add_option("CMagmaKraidSpikeComponent", CMagmaKraidSpikeComponent)
Pointer_CActorComponent.add_option("CMagnetMovablePlatformComponent", CMagnetMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockComponent", CMagnetSlidingBlockComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockCounterWeightMovablePlatformComponent", CMagnetSlidingBlockCounterWeightMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockRailComponent", CMagnetSlidingBlockRailComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockWithCollisionsComponent", CMagnetSlidingBlockWithCollisionsComponent)
Pointer_CActorComponent.add_option("CMagnetSurfaceComponent", CMagnetSurfaceComponent)
Pointer_CActorComponent.add_option("CMagnetSurfaceHuskComponent", CMagnetSurfaceHuskComponent)
Pointer_CActorComponent.add_option("CMapAcquisitionComponent", CMapAcquisitionComponent)
Pointer_CActorComponent.add_option("CMassiveCaterzillaSpawnGroupComponent", CMassiveCaterzillaSpawnGroupComponent)
Pointer_CActorComponent.add_option("CMaterialFXComponent", CMaterialFXComponent)
Pointer_CActorComponent.add_option("CMeleeComponent", CMeleeComponent)
Pointer_CActorComponent.add_option("CMenuAnimationChangeComponent", CMenuAnimationChangeComponent)
Pointer_CActorComponent.add_option("CMissileMovement", CMissileMovement)
Pointer_CActorComponent.add_option("CModelInstanceComponent", CModelInstanceComponent)
Pointer_CActorComponent.add_option("CModelUpdaterComponent", CModelUpdaterComponent)
Pointer_CActorComponent.add_option("CMorphBallLauncherComponent", CMorphBallLauncherComponent)
Pointer_CActorComponent.add_option("CMorphBallLauncherExitComponent", CMorphBallLauncherExitComponent)
Pointer_CActorComponent.add_option("CMorphBallMovement", CMorphBallMovement)
Pointer_CActorComponent.add_option("CMovableGrapplePointComponent", CMovableGrapplePointComponent)
Pointer_CActorComponent.add_option("CMovablePlatformComponent", CMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMovementComponent", CMovementComponent)
Pointer_CActorComponent.add_option("CMultiLockOnBlockComponent", CMultiLockOnBlockComponent)
Pointer_CActorComponent.add_option("CMultiLockOnPointComponent", CMultiLockOnPointComponent)
Pointer_CActorComponent.add_option("CMultiModelUpdaterComponent", CMultiModelUpdaterComponent)
Pointer_CActorComponent.add_option("CMushroomPlatformComponent", CMushroomPlatformComponent)
Pointer_CActorComponent.add_option("CNailongAIComponent", CNailongAIComponent)
Pointer_CActorComponent.add_option("CNailongThornMovementComponent", CNailongThornMovementComponent)
Pointer_CActorComponent.add_option("CNailuggerAcidBallMovementComponent", CNailuggerAcidBallMovementComponent)
Pointer_CActorComponent.add_option("CNavMeshItemComponent", CNavMeshItemComponent)
Pointer_CActorComponent.add_option("CNoFreezeRoomComponent", CNoFreezeRoomComponent)
Pointer_CActorComponent.add_option("CObsydomithonAIComponent", CObsydomithonAIComponent)
Pointer_CActorComponent.add_option("COmniLightComponent", COmniLightComponent)
Pointer_CActorComponent.add_option("CPerceptionComponent", CPerceptionComponent)
Pointer_CActorComponent.add_option("CPersistenceComponent", CPersistenceComponent)
Pointer_CActorComponent.add_option("CPickableComponent", CPickableComponent)
Pointer_CActorComponent.add_option("CPickableItemComponent", CPickableItemComponent)
Pointer_CActorComponent.add_option("CPickableSpringBallComponent", CPickableSpringBallComponent)
Pointer_CActorComponent.add_option("CPickableSuitComponent", CPickableSuitComponent)
Pointer_CActorComponent.add_option("CPlatformTrapGrapplePointComponent", CPlatformTrapGrapplePointComponent)
Pointer_CActorComponent.add_option("CPlayerLifeComponent", CPlayerLifeComponent)
Pointer_CActorComponent.add_option("CPlayerMovement", CPlayerMovement)
Pointer_CActorComponent.add_option("CPoisonFlyAIComponent", CPoisonFlyAIComponent)
Pointer_CActorComponent.add_option("CPositionalSoundComponent", CPositionalSoundComponent)
Pointer_CActorComponent.add_option("CPowerBombBlockLifeComponent", CPowerBombBlockLifeComponent)
Pointer_CActorComponent.add_option("CPowerBombMovement", CPowerBombMovement)
Pointer_CActorComponent.add_option("CPowerGeneratorComponent", CPowerGeneratorComponent)
Pointer_CActorComponent.add_option("CPowerUpLifeComponent", CPowerUpLifeComponent)
Pointer_CActorComponent.add_option("CProfessorDoorComponent", CProfessorDoorComponent)
Pointer_CActorComponent.add_option("CProjectileMovement", CProjectileMovement)
Pointer_CActorComponent.add_option("CProtoCentralUnitComponent", CProtoCentralUnitComponent)
Pointer_CActorComponent.add_option("CProtoEmmyChaseMusicTriggerComponent", CProtoEmmyChaseMusicTriggerComponent)
Pointer_CActorComponent.add_option("CPullOffGrapplePointComponent", CPullOffGrapplePointComponent)
Pointer_CActorComponent.add_option("CPullableGrapplePointComponent", CPullableGrapplePointComponent)
Pointer_CActorComponent.add_option("CQuarentineDoorComponent", CQuarentineDoorComponent)
Pointer_CActorComponent.add_option("CQuetzoaAIComponent", CQuetzoaAIComponent)
Pointer_CActorComponent.add_option("CQuetzoaEnergyWaveMovementComponent", CQuetzoaEnergyWaveMovementComponent)
Pointer_CActorComponent.add_option("CQuetzoaMultiTargetProjectileMovementComponent", CQuetzoaMultiTargetProjectileMovementComponent)
Pointer_CActorComponent.add_option("CQuetzoaXAIComponent", CQuetzoaXAIComponent)
Pointer_CActorComponent.add_option("CRedenkiSwarmControllerComponent", CRedenkiSwarmControllerComponent)
Pointer_CActorComponent.add_option("CReturnAreaSmartObjectComponent", CReturnAreaSmartObjectComponent)
Pointer_CActorComponent.add_option("CRinkaAIComponent", CRinkaAIComponent)
Pointer_CActorComponent.add_option("CRinkaUnitComponent", CRinkaUnitComponent)
Pointer_CActorComponent.add_option("CRobotAIComponent", CRobotAIComponent)
Pointer_CActorComponent.add_option("CRockDiverAIComponent", CRockDiverAIComponent)
Pointer_CActorComponent.add_option("CRockDiverSpawnPointComponent", CRockDiverSpawnPointComponent)
Pointer_CActorComponent.add_option("CRodomithonXAIComponent", CRodomithonXAIComponent)
Pointer_CActorComponent.add_option("CRodotukAIComponent", CRodotukAIComponent)
Pointer_CActorComponent.add_option("CRotationalPlatformComponent", CRotationalPlatformComponent)
Pointer_CActorComponent.add_option("CRumbleComponent", CRumbleComponent)
Pointer_CActorComponent.add_option("CSabotoruAIComponent", CSabotoruAIComponent)
Pointer_CActorComponent.add_option("CSabotoruLifeComponent", CSabotoruLifeComponent)
Pointer_CActorComponent.add_option("CSabotoruSpawnPointComponent", CSabotoruSpawnPointComponent)
Pointer_CActorComponent.add_option("CSamusAlternativeActionPlayerComponent", CSamusAlternativeActionPlayerComponent)
Pointer_CActorComponent.add_option("CSamusAnimationComponent", CSamusAnimationComponent)
Pointer_CActorComponent.add_option("CSamusGunComponent", CSamusGunComponent)
Pointer_CActorComponent.add_option("CSamusModelUpdaterComponent", CSamusModelUpdaterComponent)
Pointer_CActorComponent.add_option("CSamusMovement", CSamusMovement)
Pointer_CActorComponent.add_option("CSaveStationUsableComponent", CSaveStationUsableComponent)
Pointer_CActorComponent.add_option("CSceneComponent", CSceneComponent)
Pointer_CActorComponent.add_option("CSceneModelAnimationComponent", CSceneModelAnimationComponent)
Pointer_CActorComponent.add_option("CSclawkAIComponent", CSclawkAIComponent)
Pointer_CActorComponent.add_option("CSclawkLifeComponent", CSclawkLifeComponent)
Pointer_CActorComponent.add_option("CScorpiusAIComponent", CScorpiusAIComponent)
Pointer_CActorComponent.add_option("CScorpiusFXComponent", CScorpiusFXComponent)
Pointer_CActorComponent.add_option("CScorpiusPoisonousSpitMovementComponent", CScorpiusPoisonousSpitMovementComponent)
Pointer_CActorComponent.add_option("CScourgeAIComponent", CScourgeAIComponent)
Pointer_CActorComponent.add_option("CScourgeLifeComponent", CScourgeLifeComponent)
Pointer_CActorComponent.add_option("CScriptComponent", CScriptComponent)
Pointer_CActorComponent.add_option("CSegmentLightComponent", CSegmentLightComponent)
Pointer_CActorComponent.add_option("CSensorDoorComponent", CSensorDoorComponent)
Pointer_CActorComponent.add_option("CShakernautAIComponent", CShakernautAIComponent)
Pointer_CActorComponent.add_option("CShelmitAIComponent", CShelmitAIComponent)
Pointer_CActorComponent.add_option("CShineonAIComponent", CShineonAIComponent)
Pointer_CActorComponent.add_option("CShipRechargeComponent", CShipRechargeComponent)
Pointer_CActorComponent.add_option("CShockWaveComponent", CShockWaveComponent)
Pointer_CActorComponent.add_option("CShockWavePoolComponent", CShockWavePoolComponent)
Pointer_CActorComponent.add_option("CShootActivatorComponent", CShootActivatorComponent)
Pointer_CActorComponent.add_option("CShootActivatorHidrogigaComponent", CShootActivatorHidrogigaComponent)
Pointer_CActorComponent.add_option("CShotComponent", CShotComponent)
Pointer_CActorComponent.add_option("CSideEnemyMovement", CSideEnemyMovement)
Pointer_CActorComponent.add_option("CSlidleSpawnPointComponent", CSlidleSpawnPointComponent)
Pointer_CActorComponent.add_option("CSlowNailongSpawnPointComponent", CSlowNailongSpawnPointComponent)
Pointer_CActorComponent.add_option("CSluggerAIComponent", CSluggerAIComponent)
Pointer_CActorComponent.add_option("CSluggerAcidBallMovementComponent", CSluggerAcidBallMovementComponent)
Pointer_CActorComponent.add_option("CSmartObjectComponent", CSmartObjectComponent)
Pointer_CActorComponent.add_option("CSonarTargetComponent", CSonarTargetComponent)
Pointer_CActorComponent.add_option("CSoundListenerComponent", CSoundListenerComponent)
Pointer_CActorComponent.add_option("CSoundProofTriggerComponent", CSoundProofTriggerComponent)
Pointer_CActorComponent.add_option("CSoundTrigger", CSoundTrigger)
Pointer_CActorComponent.add_option("CSpawnGroupComponent", CSpawnGroupComponent)
Pointer_CActorComponent.add_option("CSpawnPointComponent", CSpawnPointComponent)
Pointer_CActorComponent.add_option("CSpbSprActivator", CSpbSprActivator)
Pointer_CActorComponent.add_option("CSpecialEnergyComponent", CSpecialEnergyComponent)
Pointer_CActorComponent.add_option("CSpitclawkAIComponent", CSpitclawkAIComponent)
Pointer_CActorComponent.add_option("CSpittailMagmaBallMovementComponent", CSpittailMagmaBallMovementComponent)
Pointer_CActorComponent.add_option("CSpotLightComponent", CSpotLightComponent)
Pointer_CActorComponent.add_option("CStandaloneFXComponent", CStandaloneFXComponent)
Pointer_CActorComponent.add_option("CStartPointComponent", CStartPointComponent)
Pointer_CActorComponent.add_option("CSteamJetComponent", CSteamJetComponent)
Pointer_CActorComponent.add_option("CSteeringMovement", CSteeringMovement)
Pointer_CActorComponent.add_option("CSunnapAIComponent", CSunnapAIComponent)
Pointer_CActorComponent.add_option("CSuperMissileMovement", CSuperMissileMovement)
Pointer_CActorComponent.add_option("CSwarmAttackComponent", CSwarmAttackComponent)
Pointer_CActorComponent.add_option("CSwarmControllerComponent", CSwarmControllerComponent)
Pointer_CActorComponent.add_option("CSwifterAIComponent", CSwifterAIComponent)
Pointer_CActorComponent.add_option("CSwifterSpawnGroupComponent", CSwifterSpawnGroupComponent)
Pointer_CActorComponent.add_option("CSwingableGrapplePointComponent", CSwingableGrapplePointComponent)
Pointer_CActorComponent.add_option("CTakumakuAIComponent", CTakumakuAIComponent)
Pointer_CActorComponent.add_option("CTargetComponent", CTargetComponent)
Pointer_CActorComponent.add_option("CTeleporterUsableComponent", CTeleporterUsableComponent)
Pointer_CActorComponent.add_option("CThermalDeviceComponent", CThermalDeviceComponent)
Pointer_CActorComponent.add_option("CThermalReactionComponent", CThermalReactionComponent)
Pointer_CActorComponent.add_option("CThermalRoomConnectionFX", CThermalRoomConnectionFX)
Pointer_CActorComponent.add_option("CThermalRoomFX", CThermalRoomFX)
Pointer_CActorComponent.add_option("CTimelineComponent", CTimelineComponent)
Pointer_CActorComponent.add_option("CTimerComponent", CTimerComponent)
Pointer_CActorComponent.add_option("CTotalRechargeComponent", CTotalRechargeComponent)
Pointer_CActorComponent.add_option("CTrainUsableComponent", CTrainUsableComponent)
Pointer_CActorComponent.add_option("CTrainUsableComponentCutScene", CTrainUsableComponentCutScene)
Pointer_CActorComponent.add_option("CTrainWithPortalUsableComponent", CTrainWithPortalUsableComponent)
Pointer_CActorComponent.add_option("CTriggerComponent", CTriggerComponent)
Pointer_CActorComponent.add_option("CTriggerNavMeshItemComponent", CTriggerNavMeshItemComponent)
Pointer_CActorComponent.add_option("CTunnelTrapMorphballComponent", CTunnelTrapMorphballComponent)
Pointer_CActorComponent.add_option("CUnlockAreaSmartObjectComponent", CUnlockAreaSmartObjectComponent)
Pointer_CActorComponent.add_option("CUsableComponent", CUsableComponent)
Pointer_CActorComponent.add_option("CVideoManagerComponent", CVideoManagerComponent)
Pointer_CActorComponent.add_option("CVulkranAIComponent", CVulkranAIComponent)
Pointer_CActorComponent.add_option("CVulkranMagmaBallMovementComponent", CVulkranMagmaBallMovementComponent)
Pointer_CActorComponent.add_option("CWarLotusAIComponent", CWarLotusAIComponent)
Pointer_CActorComponent.add_option("CWaterNozzleComponent", CWaterNozzleComponent)
Pointer_CActorComponent.add_option("CWaterPlatformUsableComponent", CWaterPlatformUsableComponent)
Pointer_CActorComponent.add_option("CWaterPoolComponent", CWaterPoolComponent)
Pointer_CActorComponent.add_option("CWaterTriggerChangeComponent", CWaterTriggerChangeComponent)
Pointer_CActorComponent.add_option("CWeaponMovement", CWeaponMovement)
Pointer_CActorComponent.add_option("CWeightActivableMovablePlatformComponent", CWeightActivableMovablePlatformComponent)
Pointer_CActorComponent.add_option("CWeightActivablePropComponent", CWeightActivablePropComponent)
Pointer_CActorComponent.add_option("CWeightActivatedPlatformSmartObjectComponent", CWeightActivatedPlatformSmartObjectComponent)
Pointer_CActorComponent.add_option("CWorldGraph", CWorldGraph)
Pointer_CActorComponent.add_option("CXParasiteAIComponent", CXParasiteAIComponent)
Pointer_CActorComponent.add_option("CXParasiteDropComponent", CXParasiteDropComponent)
Pointer_CActorComponent.add_option("CYamplotXAIComponent", CYamplotXAIComponent)

Pointer_CAttackPreset.add_option("CAttackPreset", CAttackPreset)

Pointer_CBarelyFrozenIceInfo.add_option("CBarelyFrozenIceInfo", CBarelyFrozenIceInfo)

Pointer_CBlackboard_CSection.add_option("CBlackboard::CSection", CBlackboard_CSection)

Pointer_CBouncingCreaturesLaunchPattern.add_option("CBouncingCreaturesLaunchPattern", CBouncingCreaturesLaunchPattern)

Pointer_CCentralUnitWeightedEdges.add_option("CCentralUnitWeightedEdges", CCentralUnitWeightedEdges)

Pointer_CChozoRobotSoldierCannonShotPattern.add_option("CChozoRobotSoldierCannonShotPattern", CChozoRobotSoldierCannonShotPattern)

Pointer_CCooldownXBossFireWallDef.add_option("CCooldownXBossFireWallDef", CCooldownXBossFireWallDef)

Pointer_CCooldownXBossLavaCarpetDef.add_option("CCooldownXBossLavaCarpetDef", CCooldownXBossLavaCarpetDef)

Pointer_CCooldownXBossLavaDropsDef.add_option("CCooldownXBossLavaDropsDef", CCooldownXBossLavaDropsDef)

Pointer_CCutSceneDef.add_option("CCutSceneDef", CCutSceneDef)

Pointer_CEmmyAutoForbiddenEdgesDef.add_option("CEmmyAutoForbiddenEdgesDef", CEmmyAutoForbiddenEdgesDef)

Pointer_CEmmyAutoGlobalSmartLinkDef.add_option("CEmmyAutoGlobalSmartLinkDef", CEmmyAutoGlobalSmartLinkDef)

Pointer_CEmmyOverrideDeathPositionDef.add_option("CEmmyOverrideDeathPositionDef", CEmmyOverrideDeathPositionDef)

Pointer_CEnemyPreset.add_option("CEnemyPreset", CEnemyPreset)

Pointer_CEnvironmentData_SAmbient.add_option("CEnvironmentData::SAmbient", CEnvironmentData_SAmbient)

Pointer_CEnvironmentData_SBloom.add_option("CEnvironmentData::SBloom", CEnvironmentData_SBloom)

Pointer_CEnvironmentData_SCubeMap.add_option("CEnvironmentData::SCubeMap", CEnvironmentData_SCubeMap)

Pointer_CEnvironmentData_SDepthTint.add_option("CEnvironmentData::SDepthTint", CEnvironmentData_SDepthTint)

Pointer_CEnvironmentData_SFog.add_option("CEnvironmentData::SFog", CEnvironmentData_SFog)

Pointer_CEnvironmentData_SHemisphericalLight.add_option("CEnvironmentData::SHemisphericalLight", CEnvironmentData_SHemisphericalLight)

Pointer_CEnvironmentData_SIBLAttenuation.add_option("CEnvironmentData::SIBLAttenuation", CEnvironmentData_SIBLAttenuation)

Pointer_CEnvironmentData_SMaterialTint.add_option("CEnvironmentData::SMaterialTint", CEnvironmentData_SMaterialTint)

Pointer_CEnvironmentData_SPlayerLight.add_option("CEnvironmentData::SPlayerLight", CEnvironmentData_SPlayerLight)

Pointer_CEnvironmentData_SSSAO.add_option("CEnvironmentData::SSSAO", CEnvironmentData_SSSAO)

Pointer_CEnvironmentData_SToneMapping.add_option("CEnvironmentData::SToneMapping", CEnvironmentData_SToneMapping)

Pointer_CEnvironmentData_SVerticalFog.add_option("CEnvironmentData::SVerticalFog", CEnvironmentData_SVerticalFog)

Pointer_CEnvironmentManager.add_option("CEnvironmentManager", CEnvironmentManager)

Pointer_CEnvironmentMusicPresets.add_option("CEnvironmentMusicPresets", CEnvironmentMusicPresets)

Pointer_CEnvironmentSoundPresets.add_option("CEnvironmentSoundPresets", CEnvironmentSoundPresets)

Pointer_CEnvironmentVisualPresets.add_option("CEnvironmentVisualPresets", CEnvironmentVisualPresets)

Pointer_CKraidSpinningNailsDef.add_option("CKraidSpinningNailsDef", CKraidSpinningNailsDef)

Pointer_CLightManager.add_option("CLightManager", CLightManager)

Pointer_CLogicCamera.add_option("CLogicCamera", CLogicCamera)

Pointer_CPattern.add_option("CPattern", CPattern)

Pointer_CPlaythrough_SCheckpointData.add_option("CPlaythrough::SCheckpointData", CPlaythrough_SCheckpointData)

Pointer_CPlaythroughDef_SCheckpointDef.add_option("CPlaythroughDef::SCheckpointDef", CPlaythroughDef_SCheckpointDef)

Pointer_CPolypFallPattern.add_option("CPolypFallPattern", CPolypFallPattern)

Pointer_CScenario.add_option("CScenario", CScenario)

Pointer_CShootDCBones.add_option("CShootDCBones", CShootDCBones)

Pointer_CShotLaunchConfig.add_option("CShotLaunchConfig", CShotLaunchConfig)
Pointer_CShotLaunchConfig.add_option("CShotVariableAngleLaunchConfig", CShotVariableAngleLaunchConfig)
Pointer_CShotLaunchConfig.add_option("CShotVariableSpeedLaunchConfig", CShotVariableSpeedLaunchConfig)

Pointer_CShotManager.add_option("CShotManager", CShotManager)

Pointer_CSubAreaManager.add_option("CSubAreaManager", CSubAreaManager)

Pointer_CSubareaCharclassGroup.add_option("CSubareaCharclassGroup", CSubareaCharclassGroup)

Pointer_CSubareaInfo.add_option("CSubareaInfo", CSubareaInfo)

Pointer_CSubareaSetup.add_option("CSubareaSetup", CSubareaSetup)

Pointer_CTentacle.add_option("CTentacle", CTentacle)

Pointer_CTriggerComponent_SActivationCondition.add_option("CTriggerComponent::SActivationCondition", CTriggerComponent_SActivationCondition)

Pointer_CTriggerLogicAction.add_option("CTriggerLogicAction", CTriggerLogicAction)
Pointer_CTriggerLogicAction.add_option("CAllowCoolShinesparkLogicAction", CAllowCoolShinesparkLogicAction)
Pointer_CTriggerLogicAction.add_option("CCameraToRailLogicAction", CCameraToRailLogicAction)
Pointer_CTriggerLogicAction.add_option("CChangeSetupLogicAction", CChangeSetupLogicAction)
Pointer_CTriggerLogicAction.add_option("CChangeStateDoorsLogicAction", CChangeStateDoorsLogicAction)
Pointer_CTriggerLogicAction.add_option("CCheckCoolShinesparkSuccessfullyCompletedLogicAction", CCheckCoolShinesparkSuccessfullyCompletedLogicAction)
Pointer_CTriggerLogicAction.add_option("CCoolShinesparkMarkMinimapLogicAction", CCoolShinesparkMarkMinimapLogicAction)
Pointer_CTriggerLogicAction.add_option("CEmmyStateOverrideLogicAction", CEmmyStateOverrideLogicAction)
Pointer_CTriggerLogicAction.add_option("CForbiddenEdgesLogicAction", CForbiddenEdgesLogicAction)
Pointer_CTriggerLogicAction.add_option("CForceMovementLogicAction", CForceMovementLogicAction)
Pointer_CTriggerLogicAction.add_option("CFreeAimTutoLogicAction", CFreeAimTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CHoldPlayerDirectionOnSubAreaChangeLogicAction", CHoldPlayerDirectionOnSubAreaChangeLogicAction)
Pointer_CTriggerLogicAction.add_option("CIgnoreFloorSlideUpperBodySubmergedLogicAction", CIgnoreFloorSlideUpperBodySubmergedLogicAction)
Pointer_CTriggerLogicAction.add_option("CItemDestructionLogicAction", CItemDestructionLogicAction)
Pointer_CTriggerLogicAction.add_option("CLockRoomLogicAction", CLockRoomLogicAction)
Pointer_CTriggerLogicAction.add_option("CLuaCallsLogicAction", CLuaCallsLogicAction)
Pointer_CTriggerLogicAction.add_option("CMarkMinimapLogicAction", CMarkMinimapLogicAction)
Pointer_CTriggerLogicAction.add_option("CPerceptionModifierLogicAction", CPerceptionModifierLogicAction)
Pointer_CTriggerLogicAction.add_option("CSPBTutoLogicAction", CSPBTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CSPRTutoLogicAction", CSPRTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CSamusOverrideDistanceToBorderLogicAction", CSamusOverrideDistanceToBorderLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameFromEmmyDoorLogicAction", CSaveGameFromEmmyDoorLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameLogicAction", CSaveGameLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameToSnapshotLogicAction", CSaveGameToSnapshotLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveSnapshotToCheckpointLogicAction", CSaveSnapshotToCheckpointLogicAction)
Pointer_CTriggerLogicAction.add_option("CSetActorEnabledLogicAction", CSetActorEnabledLogicAction)
Pointer_CTriggerLogicAction.add_option("CShowPopUpCompositionLogicAction", CShowPopUpCompositionLogicAction)
Pointer_CTriggerLogicAction.add_option("CStartCentralUnitCombatLogicAction", CStartCentralUnitCombatLogicAction)
Pointer_CTriggerLogicAction.add_option("CSubareaTransitionTypeLogicAction", CSubareaTransitionTypeLogicAction)
Pointer_CTriggerLogicAction.add_option("CTutoEnterLogicAction", CTutoEnterLogicAction)
Pointer_CTriggerLogicAction.add_option("CTutoExitLogicAction", CTutoExitLogicAction)

Pointer_CXParasiteBehavior.add_option("CXParasiteBehavior", CXParasiteBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteGoSpawnBehavior", CXParasiteGoSpawnBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteGoTransformBehavior", CXParasiteGoTransformBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteStayOnPlaceBehavior", CXParasiteStayOnPlaceBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteWanderThenFleeBehavior", CXParasiteWanderThenFleeBehavior)

Pointer_GUI_CDisplayObject.add_option("GUI::CDisplayObject", GUI_CDisplayObject)
Pointer_GUI_CDisplayObject.add_option("GUI::CAmiiboButton", GUI_CAmiiboButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CAmiiboComposition", GUI_CAmiiboComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CArchivesInspectorComposition", GUI_CArchivesInspectorComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CBoolTunableButton", GUI_CBoolTunableButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CButton", GUI_CButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CChangeMenuStateButton", GUI_CChangeMenuStateButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CChozoArchivesComposition", GUI_CChozoArchivesComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CChozoGalleryBase", GUI_CChozoGalleryBase)
Pointer_GUI_CDisplayObject.add_option("GUI::CContinueGameButton", GUI_CContinueGameButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CCopySlotButton", GUI_CCopySlotButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CCreditsButton", GUI_CCreditsButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CCustomMarkersDialog", GUI_CCustomMarkersDialog)
Pointer_GUI_CDisplayObject.add_option("GUI::CDebugMenuEntryItemRenderer", GUI_CDebugMenuEntryItemRenderer)
Pointer_GUI_CDisplayObject.add_option("GUI::CDebugTunableButton", GUI_CDebugTunableButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CDeleteSlotButton", GUI_CDeleteSlotButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CDialogComposition", GUI_CDialogComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CDifficultyButton", GUI_CDifficultyButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CDisplayObjectContainer", GUI_CDisplayObjectContainer)
Pointer_GUI_CDisplayObject.add_option("GUI::CEndingRewardsComposition", GUI_CEndingRewardsComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CExitToMainMenuButton", GUI_CExitToMainMenuButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CFloatTunableButton", GUI_CFloatTunableButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CGammaAdjustComposition", GUI_CGammaAdjustComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CGlobalMapArea", GUI_CGlobalMapArea)
Pointer_GUI_CDisplayObject.add_option("GUI::CGlobalMapComposition", GUI_CGlobalMapComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CHUD", GUI_CHUD)
Pointer_GUI_CDisplayObject.add_option("GUI::CIngameMenu", GUI_CIngameMenu)
Pointer_GUI_CDisplayObject.add_option("GUI::CIntTunableButton", GUI_CIntTunableButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CItemRenderer", GUI_CItemRenderer)
Pointer_GUI_CDisplayObject.add_option("GUI::CLabel", GUI_CLabel)
Pointer_GUI_CDisplayObject.add_option("GUI::CLegendMenuEntryItemRenderer", GUI_CLegendMenuEntryItemRenderer)
Pointer_GUI_CDisplayObject.add_option("GUI::CList", GUI_CList)
Pointer_GUI_CDisplayObject.add_option("GUI::CLoadCheckPointButton", GUI_CLoadCheckPointButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CMainMenu", GUI_CMainMenu)
Pointer_GUI_CDisplayObject.add_option("GUI::CMainMenuComposition", GUI_CMainMenuComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CMapMenuController", GUI_CMapMenuController)
Pointer_GUI_CDisplayObject.add_option("GUI::CMissionLog", GUI_CMissionLog)
Pointer_GUI_CDisplayObject.add_option("GUI::CModel3D", GUI_CModel3D)
Pointer_GUI_CDisplayObject.add_option("GUI::CNewGameButton", GUI_CNewGameButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CPopUpComposition", GUI_CPopUpComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CPowerDescriptionButton", GUI_CPowerDescriptionButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CPowerDescriptionComposition", GUI_CPowerDescriptionComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CProfileButton", GUI_CProfileButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CRumbleTunableButton", GUI_CRumbleTunableButton)
Pointer_GUI_CDisplayObject.add_option("GUI::CSamusMenuComposition", GUI_CSamusMenuComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CScene3D", GUI_CScene3D)
Pointer_GUI_CDisplayObject.add_option("GUI::CScrollMenuEntryItemRenderer", GUI_CScrollMenuEntryItemRenderer)
Pointer_GUI_CDisplayObject.add_option("GUI::CSlotInfoComposition", GUI_CSlotInfoComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CSlotOptionsComposition", GUI_CSlotOptionsComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CSlotSelectedComposition", GUI_CSlotSelectedComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CSprite", GUI_CSprite)
Pointer_GUI_CDisplayObject.add_option("GUI::CSpriteGrid", GUI_CSpriteGrid)
Pointer_GUI_CDisplayObject.add_option("GUI::CSubtitleComposition", GUI_CSubtitleComposition)
Pointer_GUI_CDisplayObject.add_option("GUI::CText", GUI_CText)
Pointer_GUI_CDisplayObject.add_option("GUI::CTutorialComposition", GUI_CTutorialComposition)

Pointer_GUI_CDisplayObjectAnimationDef.add_option("GUI::CDisplayObjectAnimationDef", GUI_CDisplayObjectAnimationDef)

Pointer_GUI_CDisplayObjectDef.add_option("GUI::CDisplayObjectDef", GUI_CDisplayObjectDef)

Pointer_GUI_CDisplayObjectStateDef.add_option("GUI::CDisplayObjectStateDef", GUI_CDisplayObjectStateDef)

Pointer_GUI_CSkin.add_option("GUI::CSkin", GUI_CSkin)

Pointer_GUI_CSpriteSheet.add_option("GUI::CSpriteSheet", GUI_CSpriteSheet)

Pointer_GUI_CSpriteSheetItem.add_option("GUI::CSpriteSheetItem", GUI_CSpriteSheetItem)

Pointer_GUI_CTrackSet.add_option("GUI::CTrackSet", GUI_CTrackSet)

Pointer_GUI_IDisplayObjectTrack.add_option("GUI::IDisplayObjectTrack", GUI_IDisplayObjectTrack)
Pointer_GUI_IDisplayObjectTrack.add_option("GUI::CDisplayObjectTrackBool", GUI_CDisplayObjectTrackBool)
Pointer_GUI_IDisplayObjectTrack.add_option("GUI::CDisplayObjectTrackFloat", GUI_CDisplayObjectTrackFloat)
Pointer_GUI_IDisplayObjectTrack.add_option("GUI::CDisplayObjectTrackString", GUI_CDisplayObjectTrackString)

Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CAnimTreeElementDef", animtree_CAnimTreeElementDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CAnimTreeDef", animtree_CAnimTreeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CAnimatedNodeDef", animtree_CAnimatedNodeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CBlendNodeDef", animtree_CBlendNodeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CBoneControlDef", animtree_CBoneControlDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CBoneFilterNodeDef", animtree_CBoneFilterNodeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CCallbackBoneControlDef", animtree_CCallbackBoneControlDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CLayerNodeDef", animtree_CLayerNodeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CLookAtEntityControlDef", animtree_CLookAtEntityControlDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CLookAtPosControlDef", animtree_CLookAtPosControlDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CPoseNodeDef", animtree_CPoseNodeDef)
Pointer_animtree_CAnimTreeElementDef.add_option("animtree::CSamusLegsBoneControlDef", animtree_CSamusLegsBoneControlDef)

Pointer_base_global_CFilePathStrId.add_option("base::global::CFilePathStrId", common_types.StrId)

Pointer_base_global_CRntFile.add_option("base::global::CRntFile", construct.Prefixed(construct.Int32ul, construct.GreedyBytes))

Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_.add_option("base::global::CRntSmallDictionary<base::global::CStrId, CActorComponent*>", base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_)

Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_.add_option("base::global::CRntVector<CEnvironmentData::SAmbientTransition>", base_global_CRntVector_CEnvironmentData_SAmbientTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_.add_option("base::global::CRntVector<CEnvironmentData::SBloomTransition>", base_global_CRntVector_CEnvironmentData_SBloomTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_.add_option("base::global::CRntVector<CEnvironmentData::SCubeMapTransition>", base_global_CRntVector_CEnvironmentData_SCubeMapTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_.add_option("base::global::CRntVector<CEnvironmentData::SDepthTintTransition>", base_global_CRntVector_CEnvironmentData_SDepthTintTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_.add_option("base::global::CRntVector<CEnvironmentData::SFogTransition>", base_global_CRntVector_CEnvironmentData_SFogTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_.add_option("base::global::CRntVector<CEnvironmentData::SHemisphericalLightTransition>", base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_.add_option("base::global::CRntVector<CEnvironmentData::SIBLAttenuationTransition>", base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_.add_option("base::global::CRntVector<CEnvironmentData::SMaterialTintTransition>", base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_.add_option("base::global::CRntVector<CEnvironmentData::SPlayerLightTransition>", base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_.add_option("base::global::CRntVector<CEnvironmentData::SSSAOTransition>", base_global_CRntVector_CEnvironmentData_SSSAOTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_.add_option("base::global::CRntVector<CEnvironmentData::SToneMappingTransition>", base_global_CRntVector_CEnvironmentData_SToneMappingTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_.add_option("base::global::CRntVector<CEnvironmentData::SVerticalFogTransition>", base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_)

Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__.add_option("base::global::CRntVector<std::unique_ptr<CSubareaCharclassGroup>>", base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__)

Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__.add_option("base::global::CRntVector<std::unique_ptr<CSubareaSetup>>", base_global_CRntVector_std_unique_ptr_CSubareaSetup__)

Pointer_base_spatial_CPolygon2D.add_option("base::spatial::CPolygon2D", base_spatial_CPolygon2D)

Pointer_base_tunable_CTunable.add_option("base::tunable::CTunable", base_tunable_CTunable)
Pointer_base_tunable_CTunable.add_option("CAIManager::CTunableAIManager", CAIManager_CTunableAIManager)
Pointer_base_tunable_CTunable.add_option("CAbilityComponent::CTunableAbilityComponent", CAbilityComponent_CTunableAbilityComponent)
Pointer_base_tunable_CTunable.add_option("CAbilityEnergyWave::CTunableAbilityEnergyWave", CAbilityEnergyWave_CTunableAbilityEnergyWave)
Pointer_base_tunable_CTunable.add_option("CAbilityGhostAura::CTunableAbilityGhostAura", CAbilityGhostAura_CTunableAbilityGhostAura)
Pointer_base_tunable_CTunable.add_option("CAbilityMultiLockon::CTunableAbilityMultiLockon", CAbilityMultiLockon_CTunableAbilityMultiLockon)
Pointer_base_tunable_CTunable.add_option("CAbilityOpticCamouflage::CTunableAbilityOpticCamouflage", CAbilityOpticCamouflage_CTunableAbilityOpticCamouflage)
Pointer_base_tunable_CTunable.add_option("CAbilityShinespark::CTunableAbilityShinespark", CAbilityShinespark_CTunableAbilityShinespark)
Pointer_base_tunable_CTunable.add_option("CAbilitySonar::CTunableAbilitySonar", CAbilitySonar_CTunableAbilitySonar)
Pointer_base_tunable_CTunable.add_option("CAbilitySpeedBooster::CTunableAbilitySpeedBooster", CAbilitySpeedBooster_CTunableAbilitySpeedBooster)
Pointer_base_tunable_CTunable.add_option("CAccessPointComponent::CTunableAccessPointComponent", CAccessPointComponent_CTunableAccessPointComponent)
Pointer_base_tunable_CTunable.add_option("CAimComponent::CTunableAim", CAimComponent_CTunableAim)
Pointer_base_tunable_CTunable.add_option("CArenaManager::CTunableArenaManager", CArenaManager_CTunableArenaManager)
Pointer_base_tunable_CTunable.add_option("CAutofocusAimCameraCtrl::CTunableAutofocusAimCameraCtrl", CAutofocusAimCameraCtrl_CTunableAutofocusAimCameraCtrl)
Pointer_base_tunable_CTunable.add_option("CBombGun::CTunableBomb", CBombGun_CTunableBomb)
Pointer_base_tunable_CTunable.add_option("CBombMovement::CTunableBombMovement", CBombMovement_CTunableBombMovement)
Pointer_base_tunable_CTunable.add_option("CBreakableTileManager::CTunableBreakableTileManager", CBreakableTileManager_CTunableBreakableTileManager)
Pointer_base_tunable_CTunable.add_option("CCharClassAttackComponent::CTunableCharClassAttackComponent", CCharClassAttackComponent_CTunableCharClassAttackComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassAutclastAIComponent::CTunableCharClassAutclastAIComponent", CCharClassAutclastAIComponent_CTunableCharClassAutclastAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassAutectorAIComponent::CTunableCharClassAutectorAIComponent", CCharClassAutectorAIComponent_CTunableCharClassAutectorAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassAutoolAIComponent::CTunableCharClassAutoolAIComponent", CCharClassAutoolAIComponent_CTunableCharClassAutoolAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassAutsharpAIComponent::CTunableCharClassAutsharpAIComponent", CCharClassAutsharpAIComponent_CTunableCharClassAutsharpAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassBigFistAIComponent::CTunableCharClassBigFistAIComponent", CCharClassBigFistAIComponent_CTunableCharClassBigFistAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassBigFistAttack::CTunableCharClassBigFistAttack", CCharClassBigFistAttack_CTunableCharClassBigFistAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassBlockableWarningRadius::CTunableCharClassBlockableWarningRadius", CCharClassBlockableWarningRadius_CTunableCharClassBlockableWarningRadius)
Pointer_base_tunable_CTunable.add_option("CCharClassCentralUnitAIComponent::CTunableCharClassCentralUnitAIComponent", CCharClassCentralUnitAIComponent_CTunableCharClassCentralUnitAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassCentralUnitCannonAIComponent::CTunableCharClassCentralUnitCannonAIComponent", CCharClassCentralUnitCannonAIComponent_CTunableCharClassCentralUnitCannonAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoCommanderAIComponent::CTunableCharClassChozoCommanderAIComponent", CCharClassChozoCommanderAIComponent_CTunableCharClassChozoCommanderAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoCommanderAirChargeAttack::CTunableCharClassChozoCommanderAirAttack", CCharClassChozoCommanderAirChargeAttack_CTunableCharClassChozoCommanderAirAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoCommanderBeamBurstAttack::CTunableCharClassChozoCommanderBeamBurstAttack", CCharClassChozoCommanderBeamBurstAttack_CTunableCharClassChozoCommanderBeamBurstAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoRobotSoldierAIComponent::CTunableCharClassChozoRobotSoldierAIComponent", CCharClassChozoRobotSoldierAIComponent_CTunableCharClassChozoRobotSoldierAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoRobotSoldierCannonShotAttack::CTunableCharClassChozoRobotSoldierCannonShotAttack", CCharClassChozoRobotSoldierCannonShotAttack_CTunableCharClassChozoRobotSoldierCannonShotAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoRobotSoldierDashSlashAttack::CTunableCharClassChozoRobotSoldierDashSlashAttack", CCharClassChozoRobotSoldierDashSlashAttack_CTunableCharClassChozoRobotSoldierDashSlashAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoRobotSoldierDisruptionFieldAttack::CTunableCharClassChozoRobotSoldierDisruptionFieldAttack", CCharClassChozoRobotSoldierDisruptionFieldAttack_CTunableCharClassChozoRobotSoldierDisruptionFieldAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoRobotSoldierUppercutAttack::CTunableCharClassChozoRobotSoldierUppercutAttack", CCharClassChozoRobotSoldierUppercutAttack_CTunableCharClassChozoRobotSoldierUppercutAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorAIComponent::CTunableCharClassChozoWarriorAIComponent", CCharClassChozoWarriorAIComponent_CTunableCharClassChozoWarriorAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorDeflectorShieldAttack::CTunableCharClassChozoWarriorShieldAttack", CCharClassChozoWarriorDeflectorShieldAttack_CTunableCharClassChozoWarriorShieldAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorGlaiveSpinAttack::CTunableCharClassChozoWarriorGlaiveSpinAttack", CCharClassChozoWarriorGlaiveSpinAttack_CTunableCharClassChozoWarriorGlaiveSpinAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorGlaiveWalljumpAttack::CTunableCharClassChozoWarriorGlaiveWalljumpAttack", CCharClassChozoWarriorGlaiveWalljumpAttack_CTunableCharClassChozoWarriorGlaiveWalljumpAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXChangeWallAttack::CTunableCharClassChozoWarriorXChangeWallAttack", CCharClassChozoWarriorXChangeWallAttack_CTunableCharClassChozoWarriorXChangeWallAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXGlaiveSpinAttack::CTunableCharClassChozoWarriorXGlaiveSpinAttack", CCharClassChozoWarriorXGlaiveSpinAttack_CTunableCharClassChozoWarriorXGlaiveSpinAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXLandAttack::CTunableCharClassChozoWarriorXLandAttack", CCharClassChozoWarriorXLandAttack_CTunableCharClassChozoWarriorXLandAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXSpitAttack::CTunableCharClassChozoWarriorXSpitAttack", CCharClassChozoWarriorXSpitAttack_CTunableCharClassChozoWarriorXSpitAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXUltimateGrabAttack::CTunableCharClassChozoWarriorXUltimateGrabAttack", CCharClassChozoWarriorXUltimateGrabAttack_CTunableCharClassChozoWarriorXUltimateGrabAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassChozoWarriorXWallClimbAttack::CTunableCharClassChozoWarriorXWallClimbAttack", CCharClassChozoWarriorXWallClimbAttack_CTunableCharClassChozoWarriorXWallClimbAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossAIComponent::CTunableCharClassCooldownXBossAIComponent", CCharClassCooldownXBossAIComponent_CTunableCharClassCooldownXBossAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossLaserBiteAttack::CTunableCharClassCooldownXBossLaserBiteAttack", CCharClassCooldownXBossLaserBiteAttack_CTunableCharClassCooldownXBossLaserBiteAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossLavaCarpetAttack::CTunableCharClassCooldownXBossLavaCarpetAttack", CCharClassCooldownXBossLavaCarpetAttack_CTunableCharClassCooldownXBossLavaCarpetAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossLavaDropsAttack::CTunableCharClassCooldownXBossLavaDropsAttack", CCharClassCooldownXBossLavaDropsAttack_CTunableCharClassCooldownXBossLavaDropsAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossReaperAttack::CTunableCharClassCooldownXBossReaperAttack", CCharClassCooldownXBossReaperAttack_CTunableCharClassCooldownXBossReaperAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossStrongWhipAttack::CTunableCharClassCooldownXBossStrongWhipAttack", CCharClassCooldownXBossStrongWhipAttack_CTunableCharClassCooldownXBossStrongWhipAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCooldownXBossWindTunnelAttack::CTunableCharClassCooldownXBossWindTunnelAttack", CCharClassCooldownXBossWindTunnelAttack_CTunableCharClassCooldownXBossWindTunnelAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassCoreXAIComponent::CTunableCharClassCoreXAIComponent", CCharClassCoreXAIComponent_CTunableCharClassCoreXAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyCaveAIComponent::CTunableEmmyCaveAIComponent", CCharClassEmmyCaveAIComponent_CTunableEmmyCaveAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyForestAIComponent::CTunableEmmyForestAIComponent", CCharClassEmmyForestAIComponent_CTunableEmmyForestAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyLabAIComponent::CTunableEmmyLabAIComponent", CCharClassEmmyLabAIComponent_CTunableEmmyLabAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyMagmaAIComponent::CTunableEmmyMagmaAIComponent", CCharClassEmmyMagmaAIComponent_CTunableEmmyMagmaAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyProtoAIComponent::CTunableEmmyProtoAIComponent", CCharClassEmmyProtoAIComponent_CTunableEmmyProtoAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmySancAIComponent::CTunableEmmySancAIComponent", CCharClassEmmySancAIComponent_CTunableEmmySancAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassEmmyShipyardAIComponent::CTunableEmmyShipyardAIComponent", CCharClassEmmyShipyardAIComponent_CTunableEmmyShipyardAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassGobblerAIComponent::CTunableCharClassGobblerAIComponent", CCharClassGobblerAIComponent_CTunableCharClassGobblerAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassGoliathAIComponent::CTunableCharClassGoliathAIComponent", CCharClassGoliathAIComponent_CTunableCharClassGoliathAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassGoliathAttack::CTunableCharClassGoliathAttack", CCharClassGoliathAttack_CTunableCharClassGoliathAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassGooplotAIComponent::CTunableCharClassGooplotAIComponent", CCharClassGooplotAIComponent_CTunableCharClassGooplotAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassGooplotJumpAttack::CTunableCharClassGooplotJumpAttack", CCharClassGooplotJumpAttack_CTunableCharClassGooplotJumpAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassGooplotUndoJumpAttack::CTunableCharClassGooplotUndoJumpAttack", CCharClassGooplotUndoJumpAttack_CTunableCharClassGooplotUndoJumpAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassGroundShockerAIComponent::CTunableCharClassGroundShockerAIComponent", CCharClassGroundShockerAIComponent_CTunableCharClassGroundShockerAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassGroundShockerAttack::CTunableCharClassGroundShockerAttack", CCharClassGroundShockerAttack_CTunableCharClassGroundShockerAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassHecathonAIComponent::CTunableCharClassHecathoAIComponent", CCharClassHecathonAIComponent_CTunableCharClassHecathoAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassHydrogigaAIComponent::CTunableCharClassHydrogigaAIComponent", CCharClassHydrogigaAIComponent_CTunableCharClassHydrogigaAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidAIComponent::CTunableCharClassKraidAIComponent", CCharClassKraidAIComponent_CTunableCharClassKraidAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidAcidBlobsAttack::CTunableCharClassKraidAcidBlobsAttack", CCharClassKraidAcidBlobsAttack_CTunableCharClassKraidAcidBlobsAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidBackSlapAttack::CTunableCharClassKraidBackSlapAttack", CCharClassKraidBackSlapAttack_CTunableCharClassKraidBackSlapAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidBouncingCreaturesAttack::CTunableCharClassKraidBouncingCreaturesAttack", CCharClassKraidBouncingCreaturesAttack_CTunableCharClassKraidBouncingCreaturesAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidFierceSwipeAttack::CTunableCharClassKraidFierceSwipeAttack", CCharClassKraidFierceSwipeAttack_CTunableCharClassKraidFierceSwipeAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidFlyingSpikesAttack::CTunableCharClassKraidFlyingSpikesAttack", CCharClassKraidFlyingSpikesAttack_CTunableCharClassKraidFlyingSpikesAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidShockerSplashAttack::CTunableCharClassKraidShockerSplashAttack", CCharClassKraidShockerSplashAttack_CTunableCharClassKraidShockerSplashAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidSpinningNailsAttack::CTunableCharClassKraidSpinningNailsAttack", CCharClassKraidSpinningNailsAttack_CTunableCharClassKraidSpinningNailsAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassKraidTripleFlyingSpikesAttack::CTunableCharClassKraidTripleFlyingSpikesAttack", CCharClassKraidTripleFlyingSpikesAttack_CTunableCharClassKraidTripleFlyingSpikesAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassLifeComponent::CTunableCharClassLifeComponent", CCharClassLifeComponent_CTunableCharClassLifeComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassMagnetSurfaceHuskComponent::CTunableCharClassMagnetSurfaceHuskComponent", CCharClassMagnetSurfaceHuskComponent_CTunableCharClassMagnetSurfaceHuskComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassObsydomithonAIComponent::CTunableCharClassObsydomithonAIComponent", CCharClassObsydomithonAIComponent_CTunableCharClassObsydomithonAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassObsydomithonAttack::CTunableCharClassObsydomithonAttack", CCharClassObsydomithonAttack_CTunableCharClassObsydomithonAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassPoisonFlyAIComponent::CTunableCharClassPoisonFlyAIComponent", CCharClassPoisonFlyAIComponent_CTunableCharClassPoisonFlyAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassPoisonFlyDiveAttack::CTunableCharClassPoisonFlyDiveAttack", CCharClassPoisonFlyDiveAttack_CTunableCharClassPoisonFlyDiveAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassQuetzoaAIComponent::CTunableCharClassQuetzoaAIComponent", CCharClassQuetzoaAIComponent_CTunableCharClassQuetzoaAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassQuetzoaChargeAttack::CTunableCharClassQuetzoaChargeAttack", CCharClassQuetzoaChargeAttack_CTunableCharClassQuetzoaChargeAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassQuetzoaEnergyWaveAttack::CTunableCharClassQuetzoaEnergyWaveAttack", CCharClassQuetzoaEnergyWaveAttack_CTunableCharClassQuetzoaEnergyWaveAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassRinkaAIComponent::CTunableCharClassRinkaAIComponent", CCharClassRinkaAIComponent_CTunableCharClassRinkaAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassRinkaUnitComponent::CTunableCharClassRinkaUnitComponent", CCharClassRinkaUnitComponent_CTunableCharClassRinkaUnitComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassRockDiverAIComponent::CTunableCharClassRockDiverAIComponent", CCharClassRockDiverAIComponent_CTunableCharClassRockDiverAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassRodotukAIComponent::CTunableCharClassRodotukAIComponent", CCharClassRodotukAIComponent_CTunableCharClassRodotukAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassRodotukSuckAttack::CTunableCharClassRodotukSuckAttack", CCharClassRodotukSuckAttack_CTunableCharClassRodotukSuckAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassSabotoruAIComponent::CTunableCharClassSabotoruAIComponent", CCharClassSabotoruAIComponent_CTunableCharClassSabotoruAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassSclawkAIComponent::CTunableCharClassSclawkAIComponent", CCharClassSclawkAIComponent_CTunableCharClassSclawkAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusAIComponent::CTunableCharClassScorpiusAIComponent", CCharClassScorpiusAIComponent_CTunableCharClassScorpiusAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusDefensiveSpikeBallPrickAttack::CTunableCharClassScorpiusDefensiveSpikeBallPrickAttack", CCharClassScorpiusDefensiveSpikeBallPrickAttack_CTunableCharClassScorpiusDefensiveSpikeBallPrickAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusDraggedBallPrickAttack::CTunableCharClassScorpiusDraggedBallPrickAttack", CCharClassScorpiusDraggedBallPrickAttack_CTunableCharClassScorpiusDraggedBallPrickAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusMovingPoisonousGasAttack::CTunableCharClassScorpiusMovingPoisonousGasAttack", CCharClassScorpiusMovingPoisonousGasAttack_CTunableCharClassScorpiusMovingPoisonousGasAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusPoisonousGasAttack::CTunableCharClassScorpiusPoisonousGasAttack", CCharClassScorpiusPoisonousGasAttack_CTunableCharClassScorpiusPoisonousGasAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusPoisonousSpitAttack::CTunableCharClassScorpiusPoisonousSpitAttack", CCharClassScorpiusPoisonousSpitAttack_CTunableCharClassScorpiusPoisonousSpitAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusSpikeBallPrickAttack::CTunableCharClassScorpiusSpikeBallPrickAttack", CCharClassScorpiusSpikeBallPrickAttack_CTunableCharClassScorpiusSpikeBallPrickAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusTailSmashAttack::CTunableCharClassScorpiusTailSmashAttack", CCharClassScorpiusTailSmashAttack_CTunableCharClassScorpiusTailSmashAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassScorpiusWhiplashAttack::CTunableCharClassScorpiusWhiplashAttack", CCharClassScorpiusWhiplashAttack_CTunableCharClassScorpiusWhiplashAttack)
Pointer_base_tunable_CTunable.add_option("CCharClassShineonAIComponent::CTunableCharClassShineonAIComponent", CCharClassShineonAIComponent_CTunableCharClassShineonAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassSwifterAIComponent::CTunableCharClassSwifterAIComponent", CCharClassSwifterAIComponent_CTunableCharClassSwifterAIComponent)
Pointer_base_tunable_CTunable.add_option("CCharClassTweakPlayRateTrack::CTunableCharClassTweakPlayRateTrack", CCharClassTweakPlayRateTrack_CTunableCharClassTweakPlayRateTrack)
Pointer_base_tunable_CTunable.add_option("CCharacterMovement::CTunableCharacterMovement", CCharacterMovement_CTunableCharacterMovement)
Pointer_base_tunable_CTunable.add_option("CChozoCommanderUltimateGrabAttack::CTunableCommanderUltimateGrab", CChozoCommanderUltimateGrabAttack_CTunableCommanderUltimateGrab)
Pointer_base_tunable_CTunable.add_option("CChozoWarriorXUltimateGrabAttack::CTunableChozoWarriorXUltimateGrabAttack", CChozoWarriorXUltimateGrabAttack_CTunableChozoWarriorXUltimateGrabAttack)
Pointer_base_tunable_CTunable.add_option("CCreditsMode::CTunableCredits", CCreditsMode_CTunableCredits)
Pointer_base_tunable_CTunable.add_option("CCutscene::CTunableCutscene", CCutscene_CTunableCutscene)
Pointer_base_tunable_CTunable.add_option("CDoorLifeComponent::CTunableDoorLifeComponent", CDoorLifeComponent_CTunableDoorLifeComponent)
Pointer_base_tunable_CTunable.add_option("CDropComponent::CTunableDropComponent", CDropComponent_CTunableDropComponent)
Pointer_base_tunable_CTunable.add_option("CDroppableComponent::CTunableDroppable", CDroppableComponent_CTunableDroppable)
Pointer_base_tunable_CTunable.add_option("CEmmyAIComponent::CTunableEmmyAIComponent", CEmmyAIComponent_CTunableEmmyAIComponent)
Pointer_base_tunable_CTunable.add_option("CEnemyLifeComponent::CTunableEnemyLifeComponent", CEnemyLifeComponent_CTunableEnemyLifeComponent)
Pointer_base_tunable_CTunable.add_option("CEvacuationCountDown::CTunableEvacuationCountDown", CEvacuationCountDown_CTunableEvacuationCountDown)
Pointer_base_tunable_CTunable.add_option("CFrozenAsFrostbiteComponent::CTunableFrozenAsFrostbiteComponent", CFrozenAsFrostbiteComponent_CTunableFrozenAsFrostbiteComponent)
Pointer_base_tunable_CTunable.add_option("CFrozenComponent::CTunableFrozenComponent", CFrozenComponent_CTunableFrozenComponent)
Pointer_base_tunable_CTunable.add_option("CGameManager::CTunableEnemies", CGameManager_CTunableEnemies)
Pointer_base_tunable_CTunable.add_option("CGameManager::CTunableGameManager", CGameManager_CTunableGameManager)
Pointer_base_tunable_CTunable.add_option("CGameManager::CTunableGraphicSettings", CGameManager_CTunableGraphicSettings)
Pointer_base_tunable_CTunable.add_option("CGameManager::CTunableMusicVolume", CGameManager_CTunableMusicVolume)
Pointer_base_tunable_CTunable.add_option("CGrappleBeamComponent::CTunableGrappleBeamComponent", CGrappleBeamComponent_CTunableGrappleBeamComponent)
Pointer_base_tunable_CTunable.add_option("CGrappleBeamGun::CTunableGrappleBeamGun", CGrappleBeamGun_CTunableGrappleBeamGun)
Pointer_base_tunable_CTunable.add_option("CGun::CTunableGun", CGun_CTunableGun)
Pointer_base_tunable_CTunable.add_option("CGunComponent::CTunableGunComponent", CGunComponent_CTunableGunComponent)
Pointer_base_tunable_CTunable.add_option("CHeatableShieldComponent::CTunableHeatableShield", CHeatableShieldComponent_CTunableHeatableShield)
Pointer_base_tunable_CTunable.add_option("CHyperBeamGun::CTunableHyperBeam", CHyperBeamGun_CTunableHyperBeam)
Pointer_base_tunable_CTunable.add_option("CIceMissileGun::CTunableIceMissile", CIceMissileGun_CTunableIceMissile)
Pointer_base_tunable_CTunable.add_option("CInputComponent::CTunableInputComponent", CInputComponent_CTunableInputComponent)
Pointer_base_tunable_CTunable.add_option("CInventoryComponent::CTunableInventoryComponent", CInventoryComponent_CTunableInventoryComponent)
Pointer_base_tunable_CTunable.add_option("CLavaPumpComponent::CTunableLavaPumpComponent", CLavaPumpComponent_CTunableLavaPumpComponent)
Pointer_base_tunable_CTunable.add_option("CLineBombGun::CTunableLineBomb", CLineBombGun_CTunableLineBomb)
Pointer_base_tunable_CTunable.add_option("CLineBombMovement::CTunableLineBombMovement", CLineBombMovement_CTunableLineBombMovement)
Pointer_base_tunable_CTunable.add_option("CLockOnMissileGun::CTunableLockOnMissile", CLockOnMissileGun_CTunableLockOnMissile)
Pointer_base_tunable_CTunable.add_option("CLockOnMissileMovement::CTunableLockOnMissileMovement", CLockOnMissileMovement_CTunableLockOnMissileMovement)
Pointer_base_tunable_CTunable.add_option("CLogicDroppedItemManager::CTunableDroppableBillboard", CLogicDroppedItemManager_CTunableDroppableBillboard)
Pointer_base_tunable_CTunable.add_option("CMetroidCameraCtrl::CTunableMetroidCameraCtrl", CMetroidCameraCtrl_CTunableMetroidCameraCtrl)
Pointer_base_tunable_CTunable.add_option("CMinimapManager::CTunableMinimapManager", CMinimapManager_CTunableMinimapManager)
Pointer_base_tunable_CTunable.add_option("CMissileBaseGun::CTunableSPR", CMissileBaseGun_CTunableSPR)
Pointer_base_tunable_CTunable.add_option("CMissileGun::CTunableMissile", CMissileGun_CTunableMissile)
Pointer_base_tunable_CTunable.add_option("CMorphBallMovement::CTunableMorphBallMovement", CMorphBallMovement_CTunableMorphBallMovement)
Pointer_base_tunable_CTunable.add_option("CMultiLockOnBlockComponent::CTunableMultiLockOnBlockComponent", CMultiLockOnBlockComponent_CTunableMultiLockOnBlockComponent)
Pointer_base_tunable_CTunable.add_option("CPlasmaBeamGun::CTunablePlasmaBeam", CPlasmaBeamGun_CTunablePlasmaBeam)
Pointer_base_tunable_CTunable.add_option("CPlayerLifeComponent::CTunablePlayerLifeComponent", CPlayerLifeComponent_CTunablePlayerLifeComponent)
Pointer_base_tunable_CTunable.add_option("CPlayerMovement::CTunablePlayerMovement", CPlayerMovement_CTunablePlayerMovement)
Pointer_base_tunable_CTunable.add_option("CPowerBeamGun::CTunablePowerBeam", CPowerBeamGun_CTunablePowerBeam)
Pointer_base_tunable_CTunable.add_option("CPowerBombGun::CTunablePowerBomb", CPowerBombGun_CTunablePowerBomb)
Pointer_base_tunable_CTunable.add_option("CPowerBombMovement::CTunablePowerBombMovement", CPowerBombMovement_CTunablePowerBombMovement)
Pointer_base_tunable_CTunable.add_option("CReserveTankInfo::CTunableReserveTanks", CReserveTankInfo_CTunableReserveTanks)
Pointer_base_tunable_CTunable.add_option("CSPBGun::CTunableSPB", CSPBGun_CTunableSPB)
Pointer_base_tunable_CTunable.add_option("CSamusAirMovementState::CTunableSamusAirMovementState", CSamusAirMovementState_CTunableSamusAirMovementState)
Pointer_base_tunable_CTunable.add_option("CSamusAnimationComponent::CTunableSamusAnimationComponent", CSamusAnimationComponent_CTunableSamusAnimationComponent)
Pointer_base_tunable_CTunable.add_option("CSamusGrappleMovementState::CTunableSamusGrappleMovementState", CSamusGrappleMovementState_CTunableSamusGrappleMovementState)
Pointer_base_tunable_CTunable.add_option("CSamusGunComponent::CTunableSamusGunComponent", CSamusGunComponent_CTunableSamusGunComponent)
Pointer_base_tunable_CTunable.add_option("CSamusHangMovementState::CTunableSamusHangMovementState", CSamusHangMovementState_CTunableSamusHangMovementState)
Pointer_base_tunable_CTunable.add_option("CSamusMagnetGloveMovementState::CTunableSamusMagnetGloveMovementState", CSamusMagnetGloveMovementState_CTunableSamusMagnetGloveMovementState)
Pointer_base_tunable_CTunable.add_option("CSamusMovement::CTunableSamusMovement", CSamusMovement_CTunableSamusMovement)
Pointer_base_tunable_CTunable.add_option("CSaveStationUsableComponent::CTunableSaveStationUsableComponent", CSaveStationUsableComponent_CTunableSaveStationUsableComponent)
Pointer_base_tunable_CTunable.add_option("CScenario::CTunableScenario", CScenario_CTunableScenario)
Pointer_base_tunable_CTunable.add_option("CShootActivatorComponent::CTunableShootActivatorComponent", CShootActivatorComponent_CTunableShootActivatorComponent)
Pointer_base_tunable_CTunable.add_option("CShotManager::CTunableShotManager", CShotManager_CTunableShotManager)
Pointer_base_tunable_CTunable.add_option("CSpecialEnergyComponent::CTunableSpecialEnergyComponent", CSpecialEnergyComponent_CTunableSpecialEnergyComponent)
Pointer_base_tunable_CTunable.add_option("CSubAreaManager::CTunableSubAreaManager", CSubAreaManager_CTunableSubAreaManager)
Pointer_base_tunable_CTunable.add_option("CSuperMissileGun::CTunableSuperMissile", CSuperMissileGun_CTunableSuperMissile)
Pointer_base_tunable_CTunable.add_option("CSwarmControllerComponent::CTunableSwarmDamage", CSwarmControllerComponent_CTunableSwarmDamage)
Pointer_base_tunable_CTunable.add_option("CTeamManager::CTunableTeamManager", CTeamManager_CTunableTeamManager)
Pointer_base_tunable_CTunable.add_option("CTriggerComponent::CTunableTriggerComponent", CTriggerComponent_CTunableTriggerComponent)
Pointer_base_tunable_CTunable.add_option("CUnlockAreaSmartObjectComponent::CTunableUnlockAreaSmartObjectComponent", CUnlockAreaSmartObjectComponent_CTunableUnlockAreaSmartObjectComponent)
Pointer_base_tunable_CTunable.add_option("CUsableComponent::CTunableUsableComponent", CUsableComponent_CTunableUsableComponent)
Pointer_base_tunable_CTunable.add_option("CVulkranAttackManager::CTunableVulkranAttackManager", CVulkranAttackManager_CTunableVulkranAttackManager)
Pointer_base_tunable_CTunable.add_option("CWaterNozzleComponent::CTunableWaterNozzle", CWaterNozzleComponent_CTunableWaterNozzle)
Pointer_base_tunable_CTunable.add_option("CWaveBeamGun::CTunableWaveBeam", CWaveBeamGun_CTunableWaveBeam)
Pointer_base_tunable_CTunable.add_option("CWideBeamGun::CTunableWideBeam", CWideBeamGun_CTunableWideBeam)
Pointer_base_tunable_CTunable.add_option("base::input::CRumbleManager::CTunableRumbleManager", base_input_CRumbleManager_CTunableRumbleManager)
Pointer_base_tunable_CTunable.add_option("base::snd::CSoundSystem::CTunableSoundSystem", base_snd_CSoundSystem_CTunableSoundSystem)
Pointer_base_tunable_CTunable.add_option("base::snd::CSoundSystemATK::CTunableSoundSystemATK", base_snd_CSoundSystemATK_CTunableSoundSystemATK)
Pointer_base_tunable_CTunable.add_option("sound::CMusicManager::CTunableMusicManager", sound_CMusicManager_CTunableMusicManager)
Pointer_base_tunable_CTunable.add_option("sound::CMusicVolumeOverride::CTunableMusicVolumeOverride", sound_CMusicVolumeOverride_CTunableMusicVolumeOverride)

Pointer_engine_scene_CScene.add_option("engine::scene::CScene", engine_scene_CScene)

Pointer_engine_scene_CSceneSlot.add_option("engine::scene::CSceneSlot", engine_scene_CSceneSlot)

Pointer_game_logic_collision_CCollider.add_option("game::logic::collision::CCollider", game_logic_collision_CCollider)

Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CShape", game_logic_collision_CShape)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CAABoxShape2D", game_logic_collision_CAABoxShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CCapsuleShape2D", game_logic_collision_CCapsuleShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CCircleShape2D", game_logic_collision_CCircleShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::COBoxShape2D", game_logic_collision_COBoxShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CPolygonCollectionShape", game_logic_collision_CPolygonCollectionShape)

Pointer_querysystem_CEvaluator.add_option("querysystem::CEvaluator", querysystem_CEvaluator)
Pointer_querysystem_CEvaluator.add_option("querysystem::CChozoRobotSoldierHeightEvaluator", querysystem_CChozoRobotSoldierHeightEvaluator)
Pointer_querysystem_CEvaluator.add_option("querysystem::CCurrentEvaluator", querysystem_CCurrentEvaluator)
Pointer_querysystem_CEvaluator.add_option("querysystem::CDistanceEvaluator", querysystem_CDistanceEvaluator)
Pointer_querysystem_CEvaluator.add_option("querysystem::CDistanceToTargetEvaluator", querysystem_CDistanceToTargetEvaluator)
Pointer_querysystem_CEvaluator.add_option("querysystem::CFilterToEvaluator", querysystem_CFilterToEvaluator)

Pointer_querysystem_CFilter.add_option("querysystem::CFilter", querysystem_CFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CChozoRobotSoldierIsInFrustumFilter", querysystem_CChozoRobotSoldierIsInFrustumFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CChozoRobotSoldierIsInMeleePathFilter", querysystem_CChozoRobotSoldierIsInMeleePathFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CChozoRobotSoldierIsInShootingPositionPathFilter", querysystem_CChozoRobotSoldierIsInShootingPositionPathFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CChozoRobotSoldierLineOfFireFilter", querysystem_CChozoRobotSoldierLineOfFireFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CChozoRobotSoldierMinTargetDistanceFilter", querysystem_CChozoRobotSoldierMinTargetDistanceFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CIsInFrustumFilter", querysystem_CIsInFrustumFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CIsInNavigablePathFilter", querysystem_CIsInNavigablePathFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CLookAtTargetFilter", querysystem_CLookAtTargetFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CMaxDistanceFilter", querysystem_CMaxDistanceFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CMaxTargetDistanceFilter", querysystem_CMaxTargetDistanceFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CMinDistanceFilter", querysystem_CMinDistanceFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CMinTargetDistanceFilter", querysystem_CMinTargetDistanceFilter)
Pointer_querysystem_CFilter.add_option("querysystem::CSameEntitySideFilter", querysystem_CSameEntitySideFilter)

Pointer_sound_CAudioPresets.add_option("sound::CAudioPresets", sound_CAudioPresets)

Pointer_sound_CMusicManager.add_option("sound::CMusicManager", sound_CMusicManager)

Pointer_sound_CSoundEventsDef_SSoundEventsRule.add_option("sound::CSoundEventsDef::SSoundEventsRule", sound_CSoundEventsDef_SSoundEventsRule)

Pointer_sound_CSoundEventsDef_SSoundEventsSelector.add_option("sound::CSoundEventsDef::SSoundEventsSelector", sound_CSoundEventsDef_SSoundEventsSelector)
Pointer_sound_CSoundEventsDef_SSoundEventsSelector.add_option("sound::SGUISoundEventsSelector", sound_SGUISoundEventsSelector)

Pointer_sound_CSoundManager.add_option("sound::CSoundManager", sound_CSoundManager)

