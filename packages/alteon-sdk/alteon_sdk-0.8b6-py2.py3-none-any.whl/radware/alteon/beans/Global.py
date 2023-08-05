
from radware.sdk.beans_common import *


class EnumVADCCurCfgVadcadvState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVADCUsersSwitch(BaseBeanEnum):
    disabled = 0
    enabled = 1


class EnumVADCUsersAdminBackdoor(BaseBeanEnum):
    disabled = 0
    enabled = 1


class EnumBwmNewCfgGenState(BaseBeanEnum):
    on = 2
    off = 3


class EnumBwmNewCfgGenEnforcePolicy(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumBwmOperSendSMTP(BaseBeanEnum):
    other = 1
    send = 2


class EnumBwmOperClearUsrEntry(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSlbNewCfgGlobalControl(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumSlbNewCfgDirectMode(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgGrace(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgVirtMatrixArch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgTpcp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgLdapVersion(BaseBeanEnum):
    version2 = 1
    version3 = 2


class EnumSlbNewCfgAllowHttpHc(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSubmac(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgRtsVlan(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgVirtualServiceStats(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgPortBind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgVmaSrcPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgIpTcpCksum(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgAuxRipHash(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgClearBackup(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgvStat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgVmaDip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgClsRst(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgRtsIpLkp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSubdmac(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgpVlanTag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSessRevive(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSipSpat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgServDown(BaseBeanEnum):
    route = 1
    drop = 2


class EnumSlbNewCfgSlbTcpRstSecSeqNumChk(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbSrvCkData(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbSessVpt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbMilliSecResolution(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbVmacBkp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbFmrPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbEnhance(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgNonHTTP(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbSlntcls(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgIpTos(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSlbDynAddr(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgHwHash(BaseBeanEnum):
    l4 = 1
    l3 = 2


class EnumSlbNewCfgPreserve(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgMacToMe(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSessRtSrcMacUpdate(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumSlbNewCfgWaphcCouple(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgWapTpcp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncFilt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncVrrp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncSfo(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncBwm(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncPeerPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncCerts(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncRoute(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncRouteTbl(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncDynamicData(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncL3(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncUcastSfo(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncMaponly(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncPasswordMode(BaseBeanEnum):
    admin = 1
    passphrase = 2


class EnumSlbNewCfgSyncGw(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgSyncAutosync(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSynAttackNewCfgOnOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumGslbNewCfgGenState(BaseBeanEnum):
    on = 1
    off = 2


class EnumGslbNewCfgGenHttpRedirect(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenUsern(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenNoremote(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenEncrypt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenDnsDirect(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenHostname(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenDsync(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgGenServcDownDnsRsp(BaseBeanEnum):
    norsp = 1
    srvfail = 2


class EnumGslbNewCfgGenExcludeRedir(BaseBeanEnum):
    disabled = 0
    enabled = 1


class EnumGslbNewCfgDnsSecGlobalEnabled(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNewCfgDnsSecGlobalType(BaseBeanEnum):
    nsec = 1
    nsec3 = 2


class EnumGslbNewCfgDnsSecGlobalNsec3Algorithm(BaseBeanEnum):
    sha1 = 1
    sha256 = 2


class EnumGslbNewCfgDnsSecGlobalKeyMaster(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbDnsSecImportExportComponentType(BaseBeanEnum):
    none = 0
    key = 1
    dnskey = 2
    dsrecord = 3


class EnumGslbDnsSecImportExportPortType(BaseBeanEnum):
    data = 0
    mgmt = 1


class EnumGslbDnsSecImportExportImpKeyType(BaseBeanEnum):
    keyTypeKSK = 1
    keyTypeZSK = 2


class EnumGslbDnsSecImportExportImpKeyStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumGslbDnsSecImportExportImpKeySize(BaseBeanEnum):
    keySize1024 = 1
    keySize2048 = 2
    keySize4096 = 3


class EnumGslbDnsSecImportExportImpKeyAlgo(BaseBeanEnum):
    keyAlgoRsaSha1 = 1
    keyAlgoRsaSha256 = 2
    keyAlgoRsaSha512 = 3


class EnumGslbDnsSecImportExportAction(BaseBeanEnum):
    none = 0
    import_ = 1
    export = 2


class EnumGslbNewCfgLLBProxonOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumGslbNewDnsResLPWizardFirstIpVersion(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbNewDnsResLPWizardSecondIpVersion(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbNewDnsResLPWizardThirdIpVersion(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumPipNewCfgBaseType(BaseBeanEnum):
    port = 1
    vlan = 2


class EnumSlbStatLinkpfClearAll(BaseBeanEnum):
    ok = 1
    clearAll = 2


class EnumSlbStatLinkpfSmartNATAll(BaseBeanEnum):
    ok = 1
    clearAll = 2
    nonat = 3
    static = 4
    dynamic = 5


class EnumGslbStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSlbStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSlbStatsPeerClearConfirm(BaseBeanEnum):
    yes = 1
    no = 2


class EnumSlbSfoSessMirrorStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSessionInfoState(BaseBeanEnum):
    start = 1
    idle = 2
    inprogress = 3
    complete = 4


class EnumSlbSessionInfoType(BaseBeanEnum):
    all = 1
    cip = 2
    cport = 3
    dip = 4
    dport = 5
    pip = 6
    pport = 7
    filter = 8
    flag = 9
    port = 10
    real = 11


class EnumSlbSessionInfoFlag(BaseBeanEnum):
    eFlag = 1
    lFlag = 2
    nFlag = 3
    pFlag = 4
    sFlag = 5
    tFlag = 6
    uFlag = 7
    wFlag = 8
    ruFlag = 9
    riFlag = 10
    viFlag = 11
    vrFlag = 12
    vsFlag = 13
    vmFlag = 14
    vdFlag = 15
    none = 20


class EnumSlbSessionInfoStringFormatFlag(BaseBeanEnum):
    formatted = 1
    none = 2


class EnumSlbNewAcclCfgFastViewOnOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumSlbCurAcclCfgFastViewSupported(BaseBeanEnum):
    true = 1
    false = 2


class EnumSynAtkState(BaseBeanEnum):
    on = 1
    off = 2


class EnumSynAtkOnOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumSlbOperClearSessionTable(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSlbOperConfigSync(BaseBeanEnum):
    ok = 1
    sync = 2


class EnumGslbOperRemove(BaseBeanEnum):
    ok = 1
    remove = 2


class EnumGslbOperClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumGslbOperSendQuery(BaseBeanEnum):
    ok = 1
    query = 2


class EnumGslbOperQuerySrcIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbOperQueryType(BaseBeanEnum):
    a = 1
    aaaa = 2


class EnumGslbOperAddEntry(BaseBeanEnum):
    ok = 1
    add = 2


class EnumGslbOperAvPersisState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbOperAvpersistence(BaseBeanEnum):
    ok = 1
    config = 2


class EnumSlbOperSessionDelTransType(BaseBeanEnum):
    tcp = 1
    udp = 2


class EnumSlbOperSessionDelete(BaseBeanEnum):
    ok = 1
    delete = 2


class EnumSlbOperSessionMoveOper(BaseBeanEnum):
    ok = 1
    move = 2


class EnumSlbOperPersSessionDelSessKeyType(BaseBeanEnum):
    cookie = 1
    clientip = 2
    sslid = 3


class EnumSlbOperPersSessionDelOper(BaseBeanEnum):
    ok = 1
    delete = 2


class EnumSlbNewCfgLinklbState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewSslCfgSSLAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewSslCfgSSLInspectDeployment(BaseBeanEnum):
    single = 1
    internal = 2
    external = 3


class EnumSlbNewSslCfgHwOffld(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewSslBereuseEna(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewSslBereuseSrcmtch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewAcclCfgCacheOnOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumSlbNewAcclCfgCompOnOff(BaseBeanEnum):
    on = 1
    off = 2


class EnumSlbNewCfgClusterRole(BaseBeanEnum):
    off = 1
    frontend = 2
    member = 3


class EnumSlbNewCfgClusterFeprimaIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbNewCfgClusterFeseconIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbNewCfgClusterFeprima2IpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbNewCfgClusterFesecon2IpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbNewAppwallGenCfgWaf(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbNewAppwallGenCfgAuthSso(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbNewAppwallReporterPciRep(BaseBeanEnum):
    tcp = 0
    udp = 1


class EnumSlbNewAppwallReporterSecLog(BaseBeanEnum):
    tcp = 0
    udp = 1


class EnumSlbNewAppwallReporterAudit(BaseBeanEnum):
    tcp = 0
    udp = 1


class EnumSlbNewAppwallReporterOthLog(BaseBeanEnum):
    tcp = 0
    udp = 1


class EnumSlbNewAppwallReporterTenant(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbNewAppwallReporterOnOff(BaseBeanEnum):
    off = 0
    on = 1


class EnumSlbNewAppwallReporterHighPrio(BaseBeanEnum):
    tcp = 0
    udp = 1


class EnumSlbNewLpOn(BaseBeanEnum):
    off = 0
    on = 1


class EnumSlbNewCfgSmartNatState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGslbProximityClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSlbNewCfgUrlRedirNonGetOrigSrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgUrlRedirCookieOrigSrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgUrlRedirNoCacheOrigSrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgUrlRedirHeader(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgUrlHashing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbNewCfgUrlRedirHeaderNameType(BaseBeanEnum):
    host = 1
    useragent = 2
    others = 3


class EnumSlbNewCfgUrlLbCaseSensitiveStrMatch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpNewCfgGwMetric(BaseBeanEnum):
    strict = 1
    roundrobin = 2


class EnumRip2NewCfgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumRip2NewCfgVip(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumRip2NewCfgStaticSupply(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpFwdNewCfgState(BaseBeanEnum):
    on = 2
    off = 3


class EnumIpFwdNewCfgDirectedBcast(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpFwdNewCfgNoICMPRedirect(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpFwdNewCfgRtCache(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpNewCfgBootpState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumIpNewCfgBootpPrsvPort(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVrrpNewCfgGenState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpNewCfgGenHotstandby(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpNewCfgGenUnicast(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpNewCfgGenFovdelay(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpNewCfgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumBgpNewCfgStopVipAdv(BaseBeanEnum):
    enabled = 1
    disabled = 2

class EnumBgpNewCfgMode(BaseBeanEnum):
    legacy = 1
    frr = 2
    unsupported = 2147483647

class EnumBgpNewCfgEcmp(BaseBeanEnum):
    off = 1
    ibgp = 2
    ebgp = 3
    eibgp = 4
    unsupported = 2147483647

class EnumBgpNewCfgAdvFip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfNewCfgDefaultRouteMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfNewCfgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumOspfNewCfgStaticMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfNewCfgEbgpMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfNewCfgIbgpMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfNewCfgFixedMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfNewCfgRipMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgDefaultRouteMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumOspfv3NewCfgStaticMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgEbgpMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgIbgpMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgFixedMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumOspfv3NewCfgRipMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumIpClearStats(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumUrlfClearStats(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumRouteTableClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumArpCacheClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumNbrcacheClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumRipInfoState(BaseBeanEnum):
    on = 1
    off = 2


class EnumRipInfoVip(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumRipInfoStaticSupply(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumOspfv3AdminState(BaseBeanEnum):
    on = 1
    off = 2


class EnumOspfv3ASBRstatus(BaseBeanEnum):
    on = 1
    off = 2


class EnumOspfv3ABRStatus(BaseBeanEnum):
    on = 1
    off = 2


class EnumHaNewCfgMode(BaseBeanEnum):
    disabled = 1
    vrrp = 2
    switch = 3
    service = 4
    extendedHA = 5


class EnumHaSwitchNewCfgPref(BaseBeanEnum):
    active = 1
    standby = 2


class EnumHaSwitchNewCfgFailBackMode(BaseBeanEnum):
    onfailure = 1
    always = 2


class EnumHaSwitchNewCfgTriggerl4Reals(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumHaSwitchNewCfgTrigGwTrackState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumHaSwitchNewCfgTriggerNewl4Reals(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumHaSwitchNewCfgTriggerAllReml4Reals(BaseBeanEnum):
    aadd = 1
    arem = 2


class EnumHaNewLPWizardCfgMode(BaseBeanEnum):
    disabled = 1
    vrrp = 2
    switch = 3
    service = 4
    extendedHA = 5


class EnumHaNewCfgBkpVipRt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumHaNewCfgNwClGarp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBfdNewCfgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumVrrpOperVirtRtrGroupBackup(BaseBeanEnum):
    ok = 1
    backup = 2


class EnumBgpOperStartSess(BaseBeanEnum):
    ok = 1
    start = 2


class EnumBgpOperStopSess(BaseBeanEnum):
    ok = 1
    stop = 2


class EnumGarpOperSend(BaseBeanEnum):
    ok = 1
    send = 2
    error = 3


class EnumHaOperSwitchBackup(BaseBeanEnum):
    ok = 1
    backup = 2


class EnumHwTemperatureStatus(BaseBeanEnum):
    notRelevant = 0
    ok = 1
    exceed = 2


class EnumHwFanStatus(BaseBeanEnum):
    notRelevant = 0
    ok = 1
    fail = 2
    unplug = 3


class EnumAgLicenseInfoConvStatus(BaseBeanEnum):
    licConvDone = 0
    licCookieConvPending = 1


class EnumLicenseDelete(BaseBeanEnum):
    deleteGlobal = 1
    deleteBwm = 2
    deleteSecurity = 4
    deleteLlb = 5
    deleteItm = 6
    deleteCookie = 7
    deleteSymantec = 8
    deleteSlb = 9
    other = 10
    deleteServices = 11
    deletevADC = 12
    deleteNg = 13
    deleteNgPlus = 14
    deleteLp = 15


class EnumAutomaticConvType(BaseBeanEnum):
    other = 1
    automatic = 2


class EnumAgSecIpAclOperRemAll(BaseBeanEnum):
    ok = 1
    remove = 2


class EnumAgSecIpAclOperDestRemAll(BaseBeanEnum):
    ok = 1
    remove = 2


class EnumAgSecIpAclOperAddIp(BaseBeanEnum):
    ok = 1
    add = 2


class EnumAgSecIpAclOperRemove(BaseBeanEnum):
    ok = 1
    remove = 2


class EnumAgSecIpAclOperDestAddIp(BaseBeanEnum):
    ok = 1
    add = 2


class EnumAgSecIpAclOperDestRemove(BaseBeanEnum):
    ok = 1
    remove = 2


class EnumAgSyslogOperDispLog(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumAgClearAppLog(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumNtpOperSendReq(BaseBeanEnum):
    no = 1
    yes = 2


class EnumAgPeerSyncConfigOper(BaseBeanEnum):
    other = 1
    sync = 2


class EnumAgAppLogAppShape(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogCaching(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogCompression(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogContentClass(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogHTTP(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogHTTPModification(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogSSL(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogTCP(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogDataTable(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogMemory(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogFastview(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogFastviewSmf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppLogExternalFetcher(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledGslbKey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledBwmKey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledSecurityKey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledLinklbKey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledOtbKey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgEnabledGeoKey(BaseBeanEnum):
    enabled = 1
    disabled = 2
    expired = 3


class EnumAgApplyConfiguration(BaseBeanEnum):
    other = 1
    apply = 2
    applyVadc = 3


class EnumAgSavePending(BaseBeanEnum):
    saveNeeded = 1
    noSaveNeeded = 2


class EnumAgSaveConfiguration(BaseBeanEnum):
    ok = 1
    saveActive = 2
    notSaveActive = 3
    saveVadc = 4


class EnumAgRevert(BaseBeanEnum):
    other = 1
    revert = 2


class EnumAgRevertApply(BaseBeanEnum):
    other = 1
    revertApply = 2


class EnumAgReset(BaseBeanEnum):
    other = 1
    reset = 2


class EnumAgConfigForNxtReset(BaseBeanEnum):
    active = 2
    backup = 3
    default = 4


class EnumAgNewCfgConsole(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgBootp(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgClearFlashDump(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumAgNewDaylightSavings(BaseBeanEnum):
    none = 0
    africa_Algeria = 1
    africa_Angola = 2
    africa_Benin = 3
    africa_Botswana = 4
    africa_Burkina_Faso = 5
    africa_Burundi = 6
    africa_Cameroon = 7
    africa_Central_African_Rep = 8
    africa_Chad = 9
    africa_Congo_WestDemRepCongo = 10
    africa_Congo_EastDemRepCongo = 11
    africa_Congo_Rep = 12
    africa_Cote_dIvoire = 13
    africa_Djibouti = 14
    africa_Egypt = 15
    africa_Equatorial_Guinea = 16
    africa_Eritrea = 17
    africa_Ethiopia = 18
    africa_Gabon = 19
    africa_Gambia = 20
    africa_Ghana = 21
    africa_Guinea = 22
    africa_Guinea_Bissau = 23
    africa_Kenya = 24
    africa_Lesotho = 25
    africa_Liberia = 26
    africa_Libya = 27
    africa_Malawi = 28
    africa_Mali_SouthWestMali = 29
    africa_Mali_NorthEastMali = 30
    africa_Mauritania = 31
    africa_Morocco = 32
    africa_Mozambique = 33
    africa_Namibia = 34
    africa_Niger = 35
    africa_Nigeria = 36
    africa_Rwanda = 37
    africa_SaoTome_And_Principe = 38
    africa_Senegal = 39
    africa_SierraLeone = 40
    africa_Somalia = 41
    africa_SouthAfrica = 42
    europe_Spain_Mainland = 43
    africa_Spain_CeutaMelilla = 44
    atlanticOcean_Spain_CanaryIslands = 45
    africa_Sudan = 46
    africa_Swaziland = 47
    africa_Tanzania = 48
    africa_Togo = 49
    africa_Tunisia = 50
    africa_Uganda = 51
    africa_Western_Sahara = 52
    africa_Zambia = 53
    africa_Zimbabwe = 54
    americas_Anguilla = 55
    americas_Antigua_Barbuda = 56
    americas_Argentina_EArgentina = 57
    americas_Argentina_MostLocations = 58
    americas_Argentina_Jujuy = 59
    americas_Argentina_Catamarca = 60
    americas_Argentina_Mendoza = 61
    americas_Aruba = 62
    americas_Bahamas = 63
    americas_Barbados = 64
    americas_Belize = 65
    americas_Bolivia = 66
    americas_Brazil_AtlanticIslands = 67
    americas_Brazil_AmapaEPara = 68
    americas_Brazil_NEBrazil = 69
    americas_Brazil_Pernambuco = 70
    americas_Brazil_Tocantins = 71
    americas_Brazil_AlagoasSergipe = 72
    americas_Brazil_SSEBrazil = 73
    americas_Brazil_MatoGrossoDoSul = 74
    americas_Brazil_WParaRondonia = 75
    americas_Brazil_Roraima = 76
    americas_Brazil_EAmazonas = 77
    americas_Brazil_WAmazonas = 78
    americas_Brazil_Acre = 79
    americas_Canada_NewfoundlandIsland = 80
    americas_Canada_AtlanTime_NovaScotia = 81
    americas_Canada_AtlanTime_ELabrador = 82
    americas_Canada_EastTime_OntarioMostlocation = 83
    americas_Canada_EastTime_ThunderBay = 84
    americas_Canada_EastStdTime_PangnirtungNunavut = 85
    americas_Canada_EastStdTime_EastNunavut = 86
    americas_Canada_EastStdTime_CenNunavut = 87
    americas_Canada_CenTime_ManitobaWestOntario = 88
    americas_Canada_CenTime_RainyRiver = 89
    americas_Canada_CenTime_WestNunavut = 90
    americas_Canada_CenStdTime_SaskatchewanMostlocation = 91
    americas_Canada_CenStdTime_SaskatchewanMidwest = 92
    americas_Canada_MountTime_AlbertaEastBritishColumbia = 93
    americas_Canada_MountTime_CentralNorthwestTerritories = 94
    americas_Canada_MountTime_WestNorthwestTerritories = 95
    americas_Canada_MountStdTime_DawsonCrkStJohnBritColumbia = 96
    americas_Canada_PacificTime_WestBritishColumbia = 97
    americas_Canada_PacificTime_SouthYukon = 98
    americas_Canada_PacificTime_NorthYukon = 99
    americas_CaymanIslands = 100
    americas_Chile_MostLocation = 101
    americas_Chile_EasterIsland = 102
    americas_Colombia = 103
    americas_CostaRica = 104
    americas_Cuba = 105
    americas_Dominica = 106
    americas_DominicanRepublic = 107
    americas_Ecuador = 108
    americas_ElSalvado = 109
    americas_FrenchGuiana = 110
    americas_Greenland_MostLocation = 111
    americas_Greenland_EastCoastNorthScoresbysund = 112
    americas_Greenland_ScoresbysundIttoqqortoormiit = 113
    americas_Greenland_ThulePituffik = 114
    americas_Grenada = 115
    americas_Guadeloupe = 116
    americas_Guatemala = 117
    americas_Guyana = 118
    americas_Haiti = 119
    americas_Honduras = 120
    americas_Jamaica = 121
    americas_Martinique = 122
    americas_Mexico_CentTime_Mostlocations = 123
    americas_Mexico_CentTime_QuintanaRoo = 124
    americas_Mexico_CentTime_CampecheYucatan = 125
    americas_Mexico_CTime_CoahuilaDurangoNuevoLeonTamaulipas = 126
    americas_Mexico_MountTime_SBajaNayaritSinaloa = 127
    americas_Mexico_MountTime_Chihuahua = 128
    americas_Mexico_MountStdTime_Sonora = 129
    americas_Mexico_PacificTime = 130
    americas_Montserrat = 131
    americas_NetherlandsAntilles = 132
    americas_Nicaragua = 133
    americas_Panama = 134
    americas_Paraguay = 135
    americas_Peru = 136
    americas_PuertoRico = 137
    americas_StKittsAndNevis = 138
    americas_StLucia = 139
    americas_StPierreAndMiquelon = 140
    americas_StVincent = 141
    americas_Suriname = 142
    americas_TrinidadAndTobago = 143
    americas_TurksAndCaicosIs = 144
    americas_USA_EastTime = 145
    americas_USA_EastTime_MichiganMostLocation = 146
    americas_USA_EastTime_KentuckyLouisvilleArea = 147
    americas_USA_EastTime_KentuckyWayneCounty = 148
    americas_USA_EastStdTime_IndianaMostLocations = 149
    americas_USA_EastStdTime_IndianaCrawfordCounty = 150
    americas_USA_EastStdTime_IndianaStarkeCounty = 151
    americas_USA_EastStdTime_IndianaSwitzerlandCounty = 152
    americas_USA_CentTime = 153
    americas_USA_CentTime_MichiganWisconsinborder = 154
    americas_USA_CentTime_NorthDakotaOliverCounty = 155
    americas_USA_MountTime = 156
    americas_USA_MountTime_SouthIdahoAndEastOregon = 157
    americas_USA_MountTime_Navajo = 158
    americas_USA_MountStdTime_Arizona = 159
    americas_USA_PacificTime = 160
    americas_USA_AlaskaTime = 161
    americas_USA_AlaskaTime_AlaskaPanhandle = 162
    americas_USA_AlaskaTime_AlaskaPanhandleNeck = 163
    americas_USA_AlaskaTime_WestAlaska = 164
    americas_USA_AleutianIslands = 165
    americas_USA_Hawaii = 166
    americas_Uruguay = 167
    americas_Venezuela = 168
    americas_VirginIslands_UK = 169
    americas_VirginIslands_US = 170
    antarctica_McMurdoStationRossIsland = 171
    antarctica_Amundsen_ScottStationSouthPole = 172
    antarctica_PalmerStationAnversIsland = 173
    antarctica_MawsonStationHolmeBay = 174
    antarctica_DavisStationVestfoldHills = 175
    antarctica_CaseyStationBaileyPeninsula = 176
    antarctica_VostokStationSMagneticPole = 177
    antarctica_Dumont_dUrvilleBaseTerreAdelie = 178
    antarctica_SyowaStationEOngulI = 179
    arcticOcean_Svalbard = 180
    arcticOcean_JanMayen = 181
    asia_Afghanistan = 182
    asia_Armenia = 183
    asia_Azerbaijan = 184
    asia_Bahrain = 185
    asia_Bangladesh = 186
    asia_Bhutan = 187
    asia_Brunei = 188
    asia_Cambodia = 189
    asia_China_EastChinaBeijingGuangdongShanghai = 190
    asia_China_Heilongjiang = 191
    asia_China_CentralChinaGansuGuizhouSichuanYunnan = 192
    asia_China_TibetmostofXinjiangUyghur = 193
    asia_China_SouthwestXinjiangUyghur = 194
    asia_Cyprus = 195
    asia_EastTimor = 196
    asia_Georgia = 197
    asia_HongKong = 198
    asia_India = 199
    asia_Indonesia_JavaAndSumatra = 200
    asia_Indonesia_WestCentralBorneo = 201
    asia_Indonesia_EstSthBorneoCelebsBaliNusaTengaraWstTimor = 202
    asia_Indonesia_IrianJayaAndMoluccas = 203
    asia_Iran = 204
    asia_Iraq = 205
    asia_Israel = 206
    asia_Japan = 207
    asia_Jordan = 208
    asia_Kazakhstan_MostLocations = 209
    asia_Kazakhstan_QyzylordaKyzylorda = 210
    asia_Kazakhstan_Aqtobe = 211
    asia_Kazakhstan_AtyrauMangghystau = 212
    asia_Kazakhstan_WestKazakhstan = 213
    asia_Korea_North = 214
    asia_Korea_South = 215
    asia_Kuwait = 216
    asia_Kyrgyzstan = 217
    asia_Laos = 218
    asia_Lebanon = 219
    asia_Macau = 220
    asia_Malaysia_PeninsularMalaysia = 221
    asia_Malaysia_SabahSarawak = 222
    asia_Mongolia_MostLocations = 223
    asia_Mongolia_BayanOlgiyGoviAltaiHovdUvsZavkhan = 224
    asia_Mongolia_DornodSukhbaatar = 225
    asia_Myanmar = 226
    asia_Nepal = 227
    asia_Oman = 228
    asia_Pakistan = 229
    asia_Palestine = 230
    asia_Philippines = 231
    asia_Qatar = 232
    asia_Russia_Moscow_01Kaliningrad = 233
    asia_Russia_Moscow00WestRussia = 234
    asia_Russia_Moscow01CaspianSea = 235
    asia_Russia_Moscow02Urals = 236
    asia_Russia_Moscow03WestSiberia = 237
    asia_Russia_Moscow03Novosibirsk = 238
    asia_Russia_Moscow04YeniseiRiver = 239
    asia_Russia_Moscow05LakeBaikal = 240
    asia_Russia_Moscow06LenaRiver = 241
    asia_Russia_Moscow07AmurRiver = 242
    asia_Russia_Moscow07SakhalinIsland = 243
    asia_Russia_Moscow08Magadan = 244
    asia_Russia_Moscow09Kamchatka = 245
    asia_Russia_Moscow10BeringSea = 246
    asia_SaudiArabia = 247
    asia_Singapore = 248
    asia_SriLanka = 249
    asia_Syria = 250
    asia_Taiwan = 251
    asia_Tajikistan = 252
    asia_Thailand = 253
    asia_Turkmenistan = 254
    asia_UnitedArabEmirates = 255
    asia_Uzbekistan_WestUzbekistan = 256
    asia_Uzbekistan_EastUzbekistan = 257
    asia_Vietnam = 258
    asia_Yemen = 259
    atlanticOcean_Bermuda = 260
    atlanticOcean_CapeVerde = 261
    atlanticOcean_FaeroeIslands = 262
    atlanticOcean_FalklandIslands = 263
    atlanticOcean_Iceland = 264
    atlanticOcean_Portugal_Mainland = 265
    atlanticOcean_Portugal_MadeiraIslands = 266
    atlanticOcean_Portugal_Azores = 267
    atlanticOcean_SouthGeorgia_SouthSandwichIslands = 268
    atlanticOcean_StHelena = 269
    atlanticOcean_Svalbard_JanMayen = 270
    australia_LordHoweIsland = 271
    australia_Tasmania = 272
    australia_Victoria = 273
    australia_NewSouthWales_MostLocations = 274
    australia_NewSouthWales_Yancowinna = 275
    australia_Queensland_MostLocations = 276
    australia_Queensland_HolidayIslands = 277
    australia_SouthAustralia = 278
    australia_NorthernTerritory = 279
    australia_WesternAustralia = 280
    europe_Albania = 281
    europe_Andorra = 282
    europe_Austria = 283
    europe_Belarus = 284
    europe_Belgium = 285
    europe_BosniaHerzegovina = 286
    europe_Britain_UKGreatBritain = 287
    europe_Britain_UKNorthernIreland = 288
    europe_Bulgaria = 289
    europe_Croatia = 290
    europe_CzechRepublic = 291
    europe_Denmark = 292
    europe_Estonia = 293
    europe_Finland = 294
    europe_France = 295
    europe_Germany = 296
    europe_Gibraltar = 297
    europe_Greece = 298
    europe_Hungary = 299
    europe_Ireland = 300
    europe_Italy = 301
    europe_Latvia = 302
    europe_Liechtenstein = 303
    europe_Lithuania = 304
    europe_Luxembourg = 305
    europe_Macedonia = 306
    europe_Malta = 307
    europe_Moldova = 308
    europe_Monaco = 309
    europe_Netherlands = 310
    europe_Norway = 311
    europe_Poland = 312
    europe_Portugal_Mainland = 313
    europe_Portugal_MadeiraIslands = 314
    europe_Portugal_Azores = 315
    europe_Romania = 316
    europe_Russia_Moscow_01Kaliningrad = 317
    europe_Russia_Moscow00WestRussia = 318
    europe_Russia_Moscow01CaspianSea = 319
    europe_Russia_Moscow02Urals = 320
    europe_Russia_Moscow03WestSiberia = 321
    europe_Russia_Moscow03Novosibirsk = 322
    europe_Russia_Moscow04YeniseiRiver = 323
    europe_Russia_Moscow05LakeBaikal = 324
    europe_Russia_Moscow06LenaRiver = 325
    europe_Russia_Moscow07AmurRiver = 326
    europe_Russia_Moscow07SakhalinIsland = 327
    europe_Russia_Moscow08Magadan = 328
    europe_Russia_Moscow09Kamchatka = 329
    europe_Russia_Moscow10BeringSea = 330
    europe_SanMarino = 331
    europe_Slovakia = 332
    europe_Slovenia = 333
    europe_Sweden = 334
    europe_Switzerland = 335
    europe_Turkey = 336
    europe_Ukraine_MostLocations = 337
    europe_Ukraine_Ruthenia = 338
    europe_Ukraine_Zaporozhye_ELugansk = 339
    europe_Ukraine_CentralCrimea = 340
    europe_VaticanCity = 341
    europe_Yugoslavia = 342
    indianOcean_BritishIndianOceanTerritory = 343
    indianOcean_ChristmasIsland = 344
    indianOcean_CocosOrKeelingIslands = 345
    indianOcean_Comoros = 346
    indianOcean_FrenchSouthernAndAntarcticLands = 347
    indianOcean_Madagascar = 348
    indianOcean_Maldives = 349
    indianOcean_Mauritius = 350
    indianOcean_Mayotte = 351
    indianOcean_Reunion = 352
    indianOcean_Seychelles = 353
    pacificOcean_Chile_MostLocations = 354
    pacificOcean_Chile_EasterIslandSalayGomez = 355
    pacificOcean_CookIslands = 356
    pacificOcean_Ecuador = 357
    pacificOcean_Fiji = 358
    pacificOcean_FrenchPolynesia_SocietyIslands = 359
    pacificOcean_FrenchPolynesia_MarquesasIslands = 360
    pacificOcean_FrenchPolynesia_GambierIslands = 361
    pacificOcean_Guam = 362
    pacificOcean_Kiribati_GilbertIslands = 363
    pacificOcean_Kiribati_PhoenixIslands = 364
    pacificOcean_Kiribati_LineIslands = 365
    pacificOcean_MarshallIslands_MostLocations = 366
    pacificOcean_MarshallIslands_Kwajalein = 367
    pacificOcean_Micronesia_Yap = 368
    pacificOcean_Micronesia_TrukOrChuuk = 369
    pacificOcean_Micronesia_PonapeOrPohnpei = 370
    pacificOcean_Micronesia_Kosrae = 371
    pacificOcean_Nauru = 372
    pacificOcean_NewCaledonia = 373
    pacificOcean_NewZealand_MostLocations = 374
    pacificOcean_NewZealand_ChathamIslands = 375
    pacificOcean_Niue = 376
    pacificOcean_NorfolkIsland = 377
    pacificOcean_NorthernMarianaIslands = 378
    pacificOcean_Palau = 379
    pacificOcean_PapuaNewGuinea = 380
    pacificOcean_Pitcairn = 381
    pacificOcean_SamoaAmerican = 382
    pacificOcean_SamoaWestern = 383
    pacificOcean_SolomonIslands = 384
    pacificOcean_Tokelau = 385
    pacificOcean_Tonga = 386
    pacificOcean_Tuvalu = 387
    pacificOceanUSA_EastTime = 388
    pacificOceanUSA_EastTime_MichiganMostLocations = 389
    pacificOceanUSA_EastTime_KentuckyLouisvilleArea = 390
    pacificOceanUSA_EastTime_KentuckyWayneCounty = 391
    pacificOceanUSA_EastStdTime_IndianaMostLocations = 392
    pacificOceanUSA_EastStdTime_IndianaCrawfordCounty = 393
    pacificOceanUSA_EastStdTime_IndianaStarkeCounty = 394
    pacificOceanUSA_EastStdTime_IndianaSwitzerlandCounty = 395
    pacificOceanUSA_CentTime = 396
    pacificOceanUSA_CentTime_MichiganWisconsinborder = 397
    pacificOceanUSA_CentTime_NorthDakotaOliverCounty = 398
    pacificOceanUSA_MountTime = 399
    pacificOceanUSA_MountTime_SouthIdahoAndEastOregon = 400
    pacificOceanUSA_MountTime_Navajo = 401
    pacificOceanUSA_MountStdTime_Arizona = 402
    pacificOceanUSA_PacificTime = 403
    pacificOceanUSA_AlaskaTime = 404
    pacificOceanUSA_AlaskaTime_AlaskaPanhandle = 405
    pacificOceanUSA_AlaskaTime_AlaskaPanhandleNeck = 406
    pacificOceanUSA_AlaskaTime_WestAlaska = 407
    pacificOceanUSA_AleutianIslands = 408
    pacificOceanUSA_Hawaii = 409
    pacificOcean_USMinorOutlyingIslands_JohnstonAtoll = 410
    pacificOcean_USMinorOutlyingIslands_MidwayIslands = 411
    pacificOcean_USMinorOutlyingIslands_WakeIsland = 412
    pacificOcean_Vanuatu = 413
    pacificOcean_WallisAndFutuna = 414


class EnumAgMgmtGlobalState(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumAgNewCfgPrompt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgVisionDriverRestoreFromBackup(BaseBeanEnum):
    activate = 1


class EnumAgNewCfgHCTCPServState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgImageTrasform(BaseBeanEnum):
    no = 0
    yes = 1


class EnumAgImageTransformBootOption(BaseBeanEnum):
    factoryDefault = 1
    lastKnownCfg = 2
    factoryWithMgmtPortCfg = 3


class EnumAgNewCfgIdleCUAlloc(BaseBeanEnum):
    limit = 0
    share = 1


class EnumAgMgmtConfigForNxtReset(BaseBeanEnum):
    erase = 1
    keep = 2


class EnumAgNewCfgSmtpHostIPVersion(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class EnumAgNewCfgVassign(BaseBeanEnum):
    vadc = 0
    cu = 1


class EnumAgMgmtCurGlobalState(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumAgSshKeysForNxtReset(BaseBeanEnum):
    erase = 1
    keep = 2


class EnumAgNewStatReportStatus(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumAgStatReportRstCounters(BaseBeanEnum):
    other = 1
    reset = 2


class EnumAgStatReportNaming(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumAgShutdown(BaseBeanEnum):
    other = 1
    shutdown = 2


class EnumAgNewCfgLimitCUAlloc(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumAgNewIdByNum(BaseBeanEnum):
    disabled = 1
    enabled = 2


class EnumAgSysIdByNum(BaseBeanEnum):
    byNumber = 1
    byName = 2


class EnumAgSyncStatus(BaseBeanEnum):
    idle = 0
    inprogress = 1
    success = 2
    failure = 3


class EnumConnmngStatsFIPSCard(BaseBeanEnum):
    notexist = 1
    zeroized = 2
    initialized = 3
    trusted = 4
    error = 5


class EnumAgImageUploadStatus(BaseBeanEnum):
    ok = 0
    inProgressFail = 1
    inProgress = 2
    inProgressSuccessful = 3
    wrriteToFlashFail = 4
    wrriteToFlashSuccessful = 5
    verificationFail = 6
    verificationSuccessful = 7
    instalattionFail = 8
    installationSuccessful = 9
    inProgressOfRmimgFail = 10


class EnumAgSyncNeeded(BaseBeanEnum):
    syncNeeded = 1
    syncNotNeeded = 2


class EnumAgNewCfgGlobalLanguage(BaseBeanEnum):
    english = 0
    chinese = 1
    korean = 2
    japanese = 3


class EnumAgLpMode(BaseBeanEnum):
    none = 0
    module = 1
    standalone = 2


class EnumAgNewCfgSmtpHost2IPVersion(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class EnumAgFipsSecurityLevel(BaseBeanEnum):
    none = 0
    level2 = 2


class EnumAgNewSecurityReportingServer(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgCurCfgSingleip(BaseBeanEnum):
    unsupported = 0
    enabled = 1
    disabled = 2


class EnumAgCurSingleIPonSingleNIC(BaseBeanEnum):
    unsupported = 0
    enabled = 1
    disabled = 2


class EnumAgAccCardSupport(BaseBeanEnum):
    notexist = 1
    cavium = 2
    caviumfips = 3
    qat = 4


class EnumAgDeviceLicMode(BaseBeanEnum):
    none = 0
    ng = 1
    ngplus = 2
    deliver = 3
    perform = 4
    secure = 5


class EnumAgMgmtNewCfgArpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgMgmtNewCfgWsRadius(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgWsLdap(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgDefensePro(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgLinkBonding(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgSysNewSyncPasswordMode(BaseBeanEnum):
    admin = 1
    passphrase = 2


class EnumAgSysNewSyncAutosync(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgAPMServerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgCurCfgAPMSharepathConfigStatus(BaseBeanEnum):
    inProgress = 1
    idleSucceeded = 2
    idleFailed = 3


class EnumAgNewCfgSyslogFac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSyslog2Fac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSyslogSev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgSyslog2Sev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgClrSyslogMsgs(BaseBeanEnum):
    other = 1
    reset = 2


class EnumAgNewCfgSyslog3Fac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSyslog4Fac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSyslog5Fac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSyslog3Sev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgSyslog4Sev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgSyslog5Sev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgAuditTrail(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogSessLog(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogSessLogFieldReal(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogSessLogFieldNat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogEmail(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogEmailSev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgSecSyslogFac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgNewCfgSecSyslogSev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumAgNewCfgSyslogFeature(BaseBeanEnum):
    all = 1
    grpmng = 2
    grpsys = 3
    grpnw = 4
    grpslb = 5
    grpsec = 6
    fastview = 7
    ha = 8
    appsvc = 9
    bgp = 10
    filter = 11
    gslb = 12
    ip = 13
    ipv6 = 14
    ospf = 15
    ospfv3 = 16
    ratelim = 17
    rmon = 18
    security = 19
    slb = 20
    slbatk = 21
    synatk = 22
    vlan = 23
    vrrp = 24
    cli = 25
    console = 26
    mgmt = 27
    ntp = 28
    ssh = 29
    stp = 30
    system = 31
    web = 32
    audit = 33


class EnumAgNewCfgSyslog2Feature(BaseBeanEnum):
    all = 1
    grpmng = 2
    grpsys = 3
    grpnw = 4
    grpslb = 5
    grpsec = 6
    fastview = 7
    ha = 8
    appsvc = 9
    bgp = 10
    filter = 11
    gslb = 12
    ip = 13
    ipv6 = 14
    ospf = 15
    ospfv3 = 16
    ratelim = 17
    rmon = 18
    security = 19
    slb = 20
    slbatk = 21
    synatk = 22
    vlan = 23
    vrrp = 24
    cli = 25
    console = 26
    mgmt = 27
    ntp = 28
    ssh = 29
    stp = 30
    system = 31
    web = 32
    audit = 33


class EnumAgNewCfgSyslog3Feature(BaseBeanEnum):
    all = 1
    grpmng = 2
    grpsys = 3
    grpnw = 4
    grpslb = 5
    grpsec = 6
    fastview = 7
    ha = 8
    appsvc = 9
    bgp = 10
    filter = 11
    gslb = 12
    ip = 13
    ipv6 = 14
    ospf = 15
    ospfv3 = 16
    ratelim = 17
    rmon = 18
    security = 19
    slb = 20
    slbatk = 21
    synatk = 22
    vlan = 23
    vrrp = 24
    cli = 25
    console = 26
    mgmt = 27
    ntp = 28
    ssh = 29
    stp = 30
    system = 31
    web = 32
    audit = 33


class EnumAgNewCfgSyslog4Feature(BaseBeanEnum):
    all = 1
    grpmng = 2
    grpsys = 3
    grpnw = 4
    grpslb = 5
    grpsec = 6
    fastview = 7
    ha = 8
    appsvc = 9
    bgp = 10
    filter = 11
    gslb = 12
    ip = 13
    ipv6 = 14
    ospf = 15
    ospfv3 = 16
    ratelim = 17
    rmon = 18
    security = 19
    slb = 20
    slbatk = 21
    synatk = 22
    vlan = 23
    vrrp = 24
    cli = 25
    console = 26
    mgmt = 27
    ntp = 28
    ssh = 29
    stp = 30
    system = 31
    web = 32
    audit = 33


class EnumAgNewCfgSyslog5Feature(BaseBeanEnum):
    all = 1
    grpmng = 2
    grpsys = 3
    grpnw = 4
    grpslb = 5
    grpsec = 6
    fastview = 7
    ha = 8
    appsvc = 9
    bgp = 10
    filter = 11
    gslb = 12
    ip = 13
    ipv6 = 14
    ospf = 15
    ospfv3 = 16
    ratelim = 17
    rmon = 18
    security = 19
    slb = 20
    slbatk = 21
    synatk = 22
    vlan = 23
    vrrp = 24
    cli = 25
    console = 26
    mgmt = 27
    ntp = 28
    ssh = 29
    stp = 30
    system = 31
    web = 32
    audit = 33


class EnumAgNewCfgSyslogExtdlog(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogSessLogMode(BaseBeanEnum):
    syslog = 1
    disk = 2
    both = 3


class EnumAgNewCfgSyslogTrapConsole(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSystem(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapMgmt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapCli(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapStp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapVlan(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSlb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapGslb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapFilter(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSsh(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapVrrp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapBgp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapNtp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapIp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapWeb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSynAtk(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapTcpLim(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapOspf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSecurity(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapRmon(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapSlbAtk(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapIpv6(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapAppSvc(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapFastView(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapHA(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapOspfv3(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapAudit(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogUrlf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSyslogTrapIprep(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgTftpImage(BaseBeanEnum):
    image1 = 2
    image2 = 3


class EnumAgTftpAction(BaseBeanEnum):
    other = 1
    img_get = 2
    cfg_get = 3
    cfg_put = 4
    dump_put = 5
    bkpdump_put = 6
    tsdump_put = 8
    bogon_get = 9
    xml_get = 14
    applog_export = 15
    cert_export = 16
    cert_import = 17
    put_techdata = 18
    sesslog_export = 19
    sshkey_export = 20
    sshkey_import = 21


class EnumAgTftpPort(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgTftpMode(BaseBeanEnum):
    tftp = 1
    ftp = 2
    scp = 3


class EnumAgTftpConfigOption(BaseBeanEnum):
    all = 1
    global_ = 2
    vADC = 3
    pvadc = 4


class EnumAgTftpConfigTypevADC(BaseBeanEnum):
    all = 1
    vadmin = 2


class EnumAgTftpSSLCertType(BaseBeanEnum):
    key = 1
    srvrcert = 2
    cert_key = 3
    request = 4
    intermca = 5
    trustca = 6
    crl = 7


class EnumAgTftpPrivateKeys(BaseBeanEnum):
    yes = 1
    no = 2


class EnumAgTftpAllowedNetworks(BaseBeanEnum):
    yes = 1
    no = 2


class EnumAgCfgTftpHostIPVersion(BaseBeanEnum):
    ipv4 = 4
    ipv6 = 6


class EnumAgTftpImageType(BaseBeanEnum):
    other = 0
    vx = 1
    adc = 2
    vxAdc = 3


class EnumAgTftpImageDownloadStatus(BaseBeanEnum):
    unKnown = 0
    failed = 1
    inProgress = 2
    successful = 3


class EnumAgTftpManSync(BaseBeanEnum):
    none = 1
    mansync = 2


class EnumAgTftpPrevArchSessLogFile(BaseBeanEnum):
    yes = 1
    no = 2


class EnumRadNewCfgState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumRadNewCfgTelnet(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRadNewCfgSecBd(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRadNewCfgOtp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumRadNewCfgLocalAuth(BaseBeanEnum):
    localFirst = 1
    disabled = 2


class EnumAgNewCfgNTPDlight(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgNTPService(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgApplyPending(BaseBeanEnum):
    applyNeeded = 2
    noApplyNeeded = 3


class EnumAgApplyConfig(BaseBeanEnum):
    apply = 1
    idle = 2
    inprogress = 3
    complete = 4
    failed = 5


class EnumAgMgmtNewCfgState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgMgmtNewCfgNtp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgRadius(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgSmtp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgSnmp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgSyslog(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgTftp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgDns(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgTacacs(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgWlm(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgReport(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgState2(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgMgmtNewCfgCdp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtNewCfgOcsp(BaseBeanEnum):
    data = 1
    mgmt = 2


class EnumAgMgmtPortNewCfgSpeed(BaseBeanEnum):
    mbs10 = 1
    mbs100 = 2
    mbs1000 = 3
    any = 4


class EnumAgMgmtPortNewCfgMode(BaseBeanEnum):
    full = 1
    half = 2
    any = 3


class EnumAgMgmtPortNewCfgAuto(BaseBeanEnum):
    on = 1
    off = 2


class EnumAgMgmtPortNewCfgSpeed2(BaseBeanEnum):
    mbs10 = 1
    mbs100 = 2
    mbs1000 = 3
    any = 4


class EnumAgMgmtPortNewCfgMode2(BaseBeanEnum):
    full = 1
    half = 2
    any = 3


class EnumAgMgmtPortNewCfgAuto2(BaseBeanEnum):
    on = 1
    off = 2


class EnumAgSslprocNewCfgRts(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgSslprocNewCfgFilt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumTacNewCfgTelnet(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgCmdAuthor(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgCmdLogging(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgClogname(BaseBeanEnum):
    admin = 1
    accounting = 2


class EnumTacNewCfgSecBd(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgCmap(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgOtp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumTacNewCfgLocalAuth(BaseBeanEnum):
    localFirst = 1
    disabled = 2


class EnumIpRepEnableNewCfg(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumIpRepNewCfgActionsErtTorLow(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepNewCfgActionsErtTorMedium(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepNewCfgActionsErtTorHigh(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepNewCfgActionsErtMaliciousLow(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepNewCfgActionsErtMaliciousMedium(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepNewCfgActionsErtMaliciousHigh(BaseBeanEnum):
    allow = 1
    block = 2
    alarm = 3


class EnumIpRepIndirectNewCfg(BaseBeanEnum):
    direct = 0
    indirect = 1


class EnumSecNewCfgIpAclSyslogSendMode(BaseBeanEnum):
    none = 1
    threshold = 2
    time = 3


class EnumSecSignalingEnableNewCfg(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumSecSignalingNewSyslogHostSev(BaseBeanEnum):
    emerg0 = 1
    alert1 = 2
    crit2 = 3
    err3 = 4
    warning4 = 5
    notice5 = 6
    info6 = 7
    debug7 = 8


class EnumSecSignalingNewSyslogHostFac(BaseBeanEnum):
    local0 = 1
    local1 = 2
    local2 = 3
    local3 = 4
    local4 = 5
    local5 = 6
    local6 = 7
    local7 = 8


class EnumAgSaveConfig(BaseBeanEnum):
    save = 1
    idle = 2
    inprogress = 3
    complete = 4
    failed = 5
    saveNoBackup = 6


class EnumAgFileTransferState(BaseBeanEnum):
    idle = 1
    transfer = 2
    inprogress = 3
    missingrows = 4
    complete = 5
    error = 6
    endoftransfer = 7


class EnumAgFileType(BaseBeanEnum):
    bogon = 1
    symantecSignature = 2


class EnumAgAccessTelnet(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessHttp(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessNewCfgHttpsState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessNewTls10State(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessNewTls11State(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessNewTls12State(BaseBeanEnum):
    enabled = 2
    disabled = 3

class EnumAgAccessNewTls13State(BaseBeanEnum):
    enabled = 2
    disabled = 3

class EnumAgAccessNewCfgSnmpAccess(BaseBeanEnum):
    read_only = 1
    read_write = 2
    disabled = 3


class EnumAgAccessNewCfgSshV1(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAccessNewCfgSshScp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAccessNewCfgSshState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgXMLCfgState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgCfgXMLClientCertDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgAccessNewCfgUserAutolock(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessNewCfgSnmpV1V2Access(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLicCookie(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumPortMirrorStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumClearCapacityUsageStats(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumNtpLastUpdateServer(BaseBeanEnum):
    none = 0
    primary = 1
    secondary = 2


class EnumNtpClearStats(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumSnmpClearStats(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumAgDiffState(BaseBeanEnum):
    diff = 1
    flashdiff = 2
    idle = 3
    inprogress = 4
    complete = 5


class EnumAgCfgDumpState(BaseBeanEnum):
    dump = 1
    idle = 2
    inprogress = 3
    complete = 4


class EnumSystemMemStatsMemoryLimitEna(BaseBeanEnum):
    enabled = 1
    disabled = 0


class EnumSystemMemStatsMemoryTrapsEna(BaseBeanEnum):
    enabled = 1
    disabled = 0


class EnumMgmtPortInfoSpeed(BaseBeanEnum):
    mbs10 = 1
    mbs100 = 2
    any = 3


class EnumMgmtPortInfoMode(BaseBeanEnum):
    full_duplex = 1
    half_duplex = 2
    any = 3


class EnumMgmtPortInfoLink(BaseBeanEnum):
    up = 1
    down = 2
    disabled = 3


class EnumHwTemperatureThresholdStatusCPU1Get(BaseBeanEnum):
    notRelevant = 0
    normal = 1
    warning = 2
    critical = 3


class EnumHwTemperatureThresholdStatusCPU2Get(BaseBeanEnum):
    notRelevant = 0
    normal = 1
    warning = 2
    critical = 3


class EnumHwPowerSupplyStatus(BaseBeanEnum):
    notRelevant = 0
    singlePowerSupplyOk = 1
    firstPowerSupplyFailed = 2
    secondPowerSupplyFailed = 3
    doublePowerSupplyOk = 4
    unknownPowerSupplyFailed = 5
    singlePowerSupplyFailed = 6
    singlePowerSupplyConnected = 7


class EnumAgGeoDbIsLicValid(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgentSwExtInfo(BaseBeanEnum):
    available = 1
    not_available = 2


class EnumAgAppwallWafStatus(BaseBeanEnum):
    disabled = 0
    enabled = 1


class EnumAgIpRepStatus(BaseBeanEnum):
    notOperational = 0
    operational = 1


class EnumAgNewCfgGeoDbAutoUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgAppwallWebUIMode(BaseBeanEnum):
    java = 0
    nodejs = 1


class EnumIpRepCountStatsClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumAgSysDiskNewCfgCriEnable(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgSysDiskNewCfgExtEnable(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgSysDiskNewCfgHighEnable(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLacpNewSystemTimeoutTime(BaseBeanEnum):
    short = 3
    long = 90


class EnumLacpNewBlockPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumPmNewCfgPortMirrState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumMstNewCfgState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumMstNewCfgStpMode(BaseBeanEnum):
    mstp = 1
    rstp = 2


class EnumMstCistDefaultCfg(BaseBeanEnum):
    default = 1


class EnumHwBypassNewState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumLldpNewTxState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLldpNewVendtlv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFdbClear(BaseBeanEnum):
    ok = 1
    clear = 2


class EnumDot1dBaseType(BaseBeanEnum):
    unknown = 1
    transparent_only = 2
    sourceroute_only = 3
    srt = 4


class EnumDot1dStpProtocolSpecification(BaseBeanEnum):
    unknown = 1
    decLb100 = 2
    ieee8021d = 3


class EnumSnmpEnableAuthenTraps(BaseBeanEnum):
    enabled = 1
    disabled = 2

class EnumGelState(BaseBeanEnum):
    enabled = 1
    disabled = 2

class Root(DeviceBean):
    def __init__(self, **kwargs):
        self.vADCMaxVADCId = kwargs.get('vADCMaxVADCId', None)
        self.vADCMaxCU = kwargs.get('vADCMaxCU', None)
        self.vADCUResolution = kwargs.get('vADCUResolution', None)
        self.vADCCurCfgVadcadvState = EnumVADCCurCfgVadcadvState.enum(kwargs.get('vADCCurCfgVadcadvState', None))
        self.vADCUsersSwitch = EnumVADCUsersSwitch.enum(kwargs.get('vADCUsersSwitch', None))
        self.vADCUsersAdminBackdoor = EnumVADCUsersAdminBackdoor.enum(kwargs.get('vADCUsersAdminBackdoor', None))
        self.vADCInfoAvailableCU = kwargs.get('vADCInfoAvailableCU', None)
        self.vADCInfoAvailableThruput = kwargs.get('vADCInfoAvailableThruput', None)
        self.vADCInfoConfigChangeTime = kwargs.get('vADCInfoConfigChangeTime', None)
        self.vADCInfoAvailableSSL = kwargs.get('vADCInfoAvailableSSL', None)
        self.vADCInfoAvailableCompression = kwargs.get('vADCInfoAvailableCompression', None)
        self.vADCInfoMaxCU = kwargs.get('vADCInfoMaxCU', None)
        self.vADCInfoMaxThruput = kwargs.get('vADCInfoMaxThruput', None)
        self.vADCInfoMaxSSL = kwargs.get('vADCInfoMaxSSL', None)
        self.vADCInfoMaxCompression = kwargs.get('vADCInfoMaxCompression', None)
        self.vADCInfoMaxVADCId = kwargs.get('vADCInfoMaxVADCId', None)
        self.vADCInfoMaxApm = kwargs.get('vADCInfoMaxApm', None)                #obsolete
        self.vADCInfoAvailableApm = kwargs.get('vADCInfoAvailableApm', None)    #obsolete
        self.vADCInfoMinCuFV = kwargs.get('vADCInfoMinCuFV', None)
        self.vADCInfoMinCuAw = kwargs.get('vADCInfoMinCuAw', None)
        self.vADCInfonMaxSslPerCu = kwargs.get('vADCInfonMaxSslPerCu', None)
        self.vADCInfonCompPerCu = kwargs.get('vADCInfonCompPerCu', None)
        self.vADCInfonCoreAvailable = kwargs.get('vADCInfonCoreAvailable', None)
        self.vADCInfoMinStepCuADC = kwargs.get('vADCInfoMinStepCuADC', None)
        self.vADCInfoMinStepCuFv = kwargs.get('vADCInfoMinStepCuFv', None)
        self.vADCInfoMinStepCuAw = kwargs.get('vADCInfoMinStepCuAw', None)
        self.bwmNewCfgGenState = EnumBwmNewCfgGenState.enum(kwargs.get('bwmNewCfgGenState', None))
        self.bwmNewCfgGenEnforcePolicy = EnumBwmNewCfgGenEnforcePolicy.enum(kwargs.get('bwmNewCfgGenEnforcePolicy', None))
        self.bwmNewCfgGenIPUserLimit = kwargs.get('bwmNewCfgGenIPUserLimit', None)
        self.bwmNewCfgGenReportStr = kwargs.get('bwmNewCfgGenReportStr', None)
        self.bwmNewCfgGenAlarmsPerSec = kwargs.get('bwmNewCfgGenAlarmsPerSec', None)
        self.bwmNewCfgGenAlarmsUpdateRate = kwargs.get('bwmNewCfgGenAlarmsUpdateRate', None)
        self.bwmNewCfgGenIPPrefixLimit = kwargs.get('bwmNewCfgGenIPPrefixLimit', None)
        self.bwmPolicyTableMaxEnt = kwargs.get('bwmPolicyTableMaxEnt', None)
        self.bwmContractTableMaxEnt = kwargs.get('bwmContractTableMaxEnt', None)
        self.bwmContTimePolicyTableMaxEnt = kwargs.get('bwmContTimePolicyTableMaxEnt', None)
        self.bwmContractGroupTableMaxEnt = kwargs.get('bwmContractGroupTableMaxEnt', None)
        self.bwmContractGroupTableMaxCont = kwargs.get('bwmContractGroupTableMaxCont', None)
        self.bwmStatsClear = EnumBwmStatsClear.enum(kwargs.get('bwmStatsClear', None))
        self.bwmOperSendSMTP = EnumBwmOperSendSMTP.enum(kwargs.get('bwmOperSendSMTP', None))
        self.bwmOperClearUsrEntry = EnumBwmOperClearUsrEntry.enum(kwargs.get('bwmOperClearUsrEntry', None))
        self.slbRealServerMaxSize = kwargs.get('slbRealServerMaxSize', None)
        self.slbRealServPortTableMaxSize = kwargs.get('slbRealServPortTableMaxSize', None)
        self.slbBuddyTableMaxSize = kwargs.get('slbBuddyTableMaxSize', None)
        self.slbGroupTableMaxSize = kwargs.get('slbGroupTableMaxSize', None)
        self.slbGroupMaxIdsSize = kwargs.get('slbGroupMaxIdsSize', None)
        self.slbVirtServerTableMaxSize = kwargs.get('slbVirtServerTableMaxSize', None)
        self.slbVirtServicesTableMaxSize = kwargs.get('slbVirtServicesTableMaxSize', None)
        self.slbUrlBwmTableMaxSize = kwargs.get('slbUrlBwmTableMaxSize', None)
        self.slbStatCPSSwitch = kwargs.get('slbStatCPSSwitch', None)
        self.slbStatThroughputSwitch = kwargs.get('slbStatThroughputSwitch', None)
        self.slbStatSSLCPSSwitch = kwargs.get('slbStatSSLCPSSwitch', None)
        self.slbPortTableMaxSize = kwargs.get('slbPortTableMaxSize', None)
        self.slbNewCfgGlobalControl = EnumSlbNewCfgGlobalControl.enum(kwargs.get('slbNewCfgGlobalControl', None))
        self.slbNewCfgImask = kwargs.get('slbNewCfgImask', None)
        self.slbNewCfgMnet = kwargs.get('slbNewCfgMnet', None)
        self.slbNewCfgMmask = kwargs.get('slbNewCfgMmask', None)
        self.slbNewCfgRadiusAuthenString = kwargs.get('slbNewCfgRadiusAuthenString', None)
        self.slbNewCfgDirectMode = EnumSlbNewCfgDirectMode.enum(kwargs.get('slbNewCfgDirectMode', None))
        self.slbNewCfgPmask = kwargs.get('slbNewCfgPmask', None)
        self.slbNewCfgGrace = EnumSlbNewCfgGrace.enum(kwargs.get('slbNewCfgGrace', None))
        self.slbNewCfgVirtMatrixArch = EnumSlbNewCfgVirtMatrixArch.enum(kwargs.get('slbNewCfgVirtMatrixArch', None))
        self.slbNewCfgFastage = kwargs.get('slbNewCfgFastage', None)
        self.slbNewCfgTpcp = EnumSlbNewCfgTpcp.enum(kwargs.get('slbNewCfgTpcp', None))
        self.slbNewCfgMetricInterval = kwargs.get('slbNewCfgMetricInterval', None)
        self.slbNewCfgLdapVersion = EnumSlbNewCfgLdapVersion.enum(kwargs.get('slbNewCfgLdapVersion', None))
        self.slbNewCfgAllowHttpHc = EnumSlbNewCfgAllowHttpHc.enum(kwargs.get('slbNewCfgAllowHttpHc', None))
        self.slbNewCfgSubmac = EnumSlbNewCfgSubmac.enum(kwargs.get('slbNewCfgSubmac', None))
        self.slbNewCfgRtsVlan = EnumSlbNewCfgRtsVlan.enum(kwargs.get('slbNewCfgRtsVlan', None))
        self.slbNewCfgVirtualServiceStats = EnumSlbNewCfgVirtualServiceStats.enum(kwargs.get('slbNewCfgVirtualServiceStats', None))
        self.slbNewCfgSlbSessAtkIntrval = kwargs.get('slbNewCfgSlbSessAtkIntrval', None)
        self.slbNewCfgSlbSessAtkAllowlim = kwargs.get('slbNewCfgSlbSessAtkAllowlim', None)
        self.slbNewCfgNewSlowage = kwargs.get('slbNewCfgNewSlowage', None)
        self.slbNewCfgPortBind = EnumSlbNewCfgPortBind.enum(kwargs.get('slbNewCfgPortBind', None))
        self.slbNewCfgVmaSrcPort = EnumSlbNewCfgVmaSrcPort.enum(kwargs.get('slbNewCfgVmaSrcPort', None))
        self.slbNewCfgIpTcpCksum = EnumSlbNewCfgIpTcpCksum.enum(kwargs.get('slbNewCfgIpTcpCksum', None))
        self.slbNewCfgAuxRipHash = EnumSlbNewCfgAuxRipHash.enum(kwargs.get('slbNewCfgAuxRipHash', None))
        self.slbNewCfgClearBackup = EnumSlbNewCfgClearBackup.enum(kwargs.get('slbNewCfgClearBackup', None))
        self.slbNewCfgmStat = kwargs.get('slbNewCfgmStat', None)
        self.slbNewCfgvStat = EnumSlbNewCfgvStat.enum(kwargs.get('slbNewCfgvStat', None))
        self.slbNewCfgVmaDip = EnumSlbNewCfgVmaDip.enum(kwargs.get('slbNewCfgVmaDip', None))
        self.slbNewCfgClsRst = EnumSlbNewCfgClsRst.enum(kwargs.get('slbNewCfgClsRst', None))
        self.slbNewCfgRtsIpLkp = EnumSlbNewCfgRtsIpLkp.enum(kwargs.get('slbNewCfgRtsIpLkp', None))
        self.slbNewCfgPprefix = kwargs.get('slbNewCfgPprefix', None)
        self.slbNewCfgSubdmac = EnumSlbNewCfgSubdmac.enum(kwargs.get('slbNewCfgSubdmac', None))
        self.slbNewCfgpVlanTag = EnumSlbNewCfgpVlanTag.enum(kwargs.get('slbNewCfgpVlanTag', None))
        self.slbNewCfgNmask = kwargs.get('slbNewCfgNmask', None)
        self.slbNewCfgSessRevive = EnumSlbNewCfgSessRevive.enum(kwargs.get('slbNewCfgSessRevive', None))
        self.slbNewCfgSipSpat = EnumSlbNewCfgSipSpat.enum(kwargs.get('slbNewCfgSipSpat', None))
        self.slbNewCfgSlbFilterParseLen = kwargs.get('slbNewCfgSlbFilterParseLen', None)
        self.slbNewCfgServDown = EnumSlbNewCfgServDown.enum(kwargs.get('slbNewCfgServDown', None))
        self.slbNewCfgSlbFtpDataSessAge = kwargs.get('slbNewCfgSlbFtpDataSessAge', None)
        self.slbNewCfgSlbTcpRstSecSeqNumChk = EnumSlbNewCfgSlbTcpRstSecSeqNumChk.enum(kwargs.get('slbNewCfgSlbTcpRstSecSeqNumChk', None))
        self.slbNewCfgSlbSrvCkData = EnumSlbNewCfgSlbSrvCkData.enum(kwargs.get('slbNewCfgSlbSrvCkData', None))
        self.slbNewCfgSlbSessVpt = EnumSlbNewCfgSlbSessVpt.enum(kwargs.get('slbNewCfgSlbSessVpt', None))
        self.slbNewCfgSlbMilliSecResolution = EnumSlbNewCfgSlbMilliSecResolution.enum(kwargs.get('slbNewCfgSlbMilliSecResolution', None))
        self.slbNewCfgSlbVmacBkp = EnumSlbNewCfgSlbVmacBkp.enum(kwargs.get('slbNewCfgSlbVmacBkp', None))
        self.slbNewCfgSlbFmrPort = EnumSlbNewCfgSlbFmrPort.enum(kwargs.get('slbNewCfgSlbFmrPort', None))
        self.slbNewCfgSlbEnhance = EnumSlbNewCfgSlbEnhance.enum(kwargs.get('slbNewCfgSlbEnhance', None))
        self.slbNewCfgNonHTTP = EnumSlbNewCfgNonHTTP.enum(kwargs.get('slbNewCfgNonHTTP', None))
        self.slbNewCfgSlbSlntcls = EnumSlbNewCfgSlbSlntcls.enum(kwargs.get('slbNewCfgSlbSlntcls', None))
        self.slbNewCfgSlbSessTblCap = kwargs.get('slbNewCfgSlbSessTblCap', None)
        self.slbNewCfgSlbDataTblCap = kwargs.get('slbNewCfgSlbDataTblCap', None)
        self.slbNewCfgIpTos = EnumSlbNewCfgIpTos.enum(kwargs.get('slbNewCfgIpTos', None))
        self.slbNewCfgSlbDynAddr = EnumSlbNewCfgSlbDynAddr.enum(kwargs.get('slbNewCfgSlbDynAddr', None))
        self.slbNewCfgClientCert = kwargs.get('slbNewCfgClientCert', None)
        self.slbNewCfgHwHash = EnumSlbNewCfgHwHash.enum(kwargs.get('slbNewCfgHwHash', None))
        self.slbNewCfgPreserve = EnumSlbNewCfgPreserve.enum(kwargs.get('slbNewCfgPreserve', None))
        self.slbNewCfgProxyage = kwargs.get('slbNewCfgProxyage', None)
        self.slbNewCfgMacToMe = EnumSlbNewCfgMacToMe.enum(kwargs.get('slbNewCfgMacToMe', None))
        self.slbNewCfgSessRtSrcMacUpdate = EnumSlbNewCfgSessRtSrcMacUpdate.enum(kwargs.get('slbNewCfgSessRtSrcMacUpdate', None))
        self.slbNewCfgWaphcWSPPort = kwargs.get('slbNewCfgWaphcWSPPort', None)
        self.slbNewCfgWaphcOffset = kwargs.get('slbNewCfgWaphcOffset', None)
        self.slbNewCfgWaphcSndContent = kwargs.get('slbNewCfgWaphcSndContent', None)
        self.slbNewCfgWaphcRcvContent = kwargs.get('slbNewCfgWaphcRcvContent', None)
        self.slbNewCfgWaphcWTLSPort = kwargs.get('slbNewCfgWaphcWTLSPort', None)
        self.slbNewCfgWaphcWTPSndContent = kwargs.get('slbNewCfgWaphcWTPSndContent', None)
        self.slbNewCfgWaphcWTPRcvContent = kwargs.get('slbNewCfgWaphcWTPRcvContent', None)
        self.slbNewCfgWaphcWTPConnContent = kwargs.get('slbNewCfgWaphcWTPConnContent', None)
        self.slbNewCfgWaphcWTPPort = kwargs.get('slbNewCfgWaphcWTPPort', None)
        self.slbNewCfgWaphcWTLSWSPPort = kwargs.get('slbNewCfgWaphcWTLSWSPPort', None)
        self.slbNewCfgWaphcWTPOffset = kwargs.get('slbNewCfgWaphcWTPOffset', None)
        self.slbNewCfgWaphcCouple = EnumSlbNewCfgWaphcCouple.enum(kwargs.get('slbNewCfgWaphcCouple', None))
        self.slbNewCfgWaphcConnPDU = kwargs.get('slbNewCfgWaphcConnPDU', None)
        self.slbNewCfgWaphcSndPDU = kwargs.get('slbNewCfgWaphcSndPDU', None)
        self.slbNewCfgWaphcRcvPDU = kwargs.get('slbNewCfgWaphcRcvPDU', None)
        self.slbNewCfgWapTpcp = EnumSlbNewCfgWapTpcp.enum(kwargs.get('slbNewCfgWapTpcp', None))
        self.slbNewCfgWapDebug = kwargs.get('slbNewCfgWapDebug', None)
        self.slbPeerTableMaxSize = kwargs.get('slbPeerTableMaxSize', None)
        self.slbNewCfgSyncFilt = EnumSlbNewCfgSyncFilt.enum(kwargs.get('slbNewCfgSyncFilt', None))
        self.slbNewCfgSyncPort = EnumSlbNewCfgSyncPort.enum(kwargs.get('slbNewCfgSyncPort', None))
        self.slbNewCfgSyncVrrp = EnumSlbNewCfgSyncVrrp.enum(kwargs.get('slbNewCfgSyncVrrp', None))
        self.slbNewCfgSyncPip = EnumSlbNewCfgSyncPip.enum(kwargs.get('slbNewCfgSyncPip', None))
        self.slbNewCfgSyncSfo = EnumSlbNewCfgSyncSfo.enum(kwargs.get('slbNewCfgSyncSfo', None))
        self.slbNewCfgSyncSfoUpdatePeriod = kwargs.get('slbNewCfgSyncSfoUpdatePeriod', None)
        self.slbNewCfgSyncBwm = EnumSlbNewCfgSyncBwm.enum(kwargs.get('slbNewCfgSyncBwm', None))
        self.slbNewCfgSyncPeerPip = EnumSlbNewCfgSyncPeerPip.enum(kwargs.get('slbNewCfgSyncPeerPip', None))
        self.slbNewCfgSyncCerts = EnumSlbNewCfgSyncCerts.enum(kwargs.get('slbNewCfgSyncCerts', None))
        self.slbNewCfgSyncCertsPassPhrase = kwargs.get('slbNewCfgSyncCertsPassPhrase', None)
        self.slbNewCfgSyncCertsConfPassPhrase = kwargs.get('slbNewCfgSyncCertsConfPassPhrase', None)
        self.slbNewCfgSyncRoute = EnumSlbNewCfgSyncRoute.enum(kwargs.get('slbNewCfgSyncRoute', None))
        self.slbNewCfgSyncRouteTbl = EnumSlbNewCfgSyncRouteTbl.enum(kwargs.get('slbNewCfgSyncRouteTbl', None))
        self.slbNewCfgSyncDynamicData = EnumSlbNewCfgSyncDynamicData.enum(kwargs.get('slbNewCfgSyncDynamicData', None))
        self.slbNewCfgSyncRUpdate = kwargs.get('slbNewCfgSyncRUpdate', None)
        self.slbNewCfgSyncRHold = kwargs.get('slbNewCfgSyncRHold', None)
        self.slbNewCfgSyncL3 = EnumSlbNewCfgSyncL3.enum(kwargs.get('slbNewCfgSyncL3', None))
        self.slbNewCfgSyncUcastSfo = EnumSlbNewCfgSyncUcastSfo.enum(kwargs.get('slbNewCfgSyncUcastSfo', None))
        self.slbNewCfgSyncUcastSfoPrimif = kwargs.get('slbNewCfgSyncUcastSfoPrimif', None)
        self.slbNewCfgSyncUcastSfoSecif = kwargs.get('slbNewCfgSyncUcastSfoSecif', None)
        self.slbNewCfgSyncMaponly = EnumSlbNewCfgSyncMaponly.enum(kwargs.get('slbNewCfgSyncMaponly', None))
        self.slbNewCfgSyncPasswordMode = EnumSlbNewCfgSyncPasswordMode.enum(kwargs.get('slbNewCfgSyncPasswordMode', None))
        self.slbCfgSyncPassphrase = kwargs.get('slbCfgSyncPassphrase', None)
        self.slbNewCfgSyncGw = EnumSlbNewCfgSyncGw.enum(kwargs.get('slbNewCfgSyncGw', None))
        self.slbNewCfgSyncAutosync = EnumSlbNewCfgSyncAutosync.enum(kwargs.get('slbNewCfgSyncAutosync', None))
        self.synAttackNewCfgInterval = kwargs.get('synAttackNewCfgInterval', None)
        self.synAttackNewCfgThreshhold = kwargs.get('synAttackNewCfgThreshhold', None)
        self.synAttackNewCfgResponseInterval = kwargs.get('synAttackNewCfgResponseInterval', None)
        self.synAttackNewCfgOnOff = EnumSynAttackNewCfgOnOff.enum(kwargs.get('synAttackNewCfgOnOff', None))
        self.fltCfgTableMaxSize = kwargs.get('fltCfgTableMaxSize', None)
        self.fltUrlBwmTableMaxSize = kwargs.get('fltUrlBwmTableMaxSize', None)
        self.fltCfgHttpRedirMappingTableMaxSize = kwargs.get('fltCfgHttpRedirMappingTableMaxSize', None)
        self.gslbNewCfgGenState = EnumGslbNewCfgGenState.enum(kwargs.get('gslbNewCfgGenState', None))
        self.gslbNewCfgGenHttpRedirect = EnumGslbNewCfgGenHttpRedirect.enum(kwargs.get('gslbNewCfgGenHttpRedirect', None))
        self.gslbNewCfgGenMinco = kwargs.get('gslbNewCfgGenMinco', None)
        self.gslbNewCfgGenUsern = EnumGslbNewCfgGenUsern.enum(kwargs.get('gslbNewCfgGenUsern', None))
        self.gslbNewCfgGenNoremote = EnumGslbNewCfgGenNoremote.enum(kwargs.get('gslbNewCfgGenNoremote', None))
        self.gslbNewCfgGenEncrypt = EnumGslbNewCfgGenEncrypt.enum(kwargs.get('gslbNewCfgGenEncrypt', None))
        self.gslbNewCfgGenRemSiteUpdatePort = kwargs.get('gslbNewCfgGenRemSiteUpdatePort', None)
        self.gslbNewCfgGenSessUtilCap = kwargs.get('gslbNewCfgGenSessUtilCap', None)
        self.gslbNewCfgGenCpuUtilCap = kwargs.get('gslbNewCfgGenCpuUtilCap', None)
        self.gslbNewCfgGenSourceIpNetmask = kwargs.get('gslbNewCfgGenSourceIpNetmask', None)
        self.gslbNewCfgGenTimeout = kwargs.get('gslbNewCfgGenTimeout', None)
        self.gslbNewCfgGenDnsDirect = EnumGslbNewCfgGenDnsDirect.enum(kwargs.get('gslbNewCfgGenDnsDirect', None))
        self.gslbNewCfgGenRemSiteUpdateVersion = kwargs.get('gslbNewCfgGenRemSiteUpdateVersion', None)
        self.gslbNewCfgGenHostname = EnumGslbNewCfgGenHostname.enum(kwargs.get('gslbNewCfgGenHostname', None))
        self.gslbNewCfgGenRemSiteUpdateIntervalSeconds = kwargs.get('gslbNewCfgGenRemSiteUpdateIntervalSeconds', None)
        self.gslbNewCfgGenNoResp = kwargs.get('gslbNewCfgGenNoResp', None)
        self.gslbNewCfgProximityTime = kwargs.get('gslbNewCfgProximityTime', None)
        self.gslbNewCfgProximityMask = kwargs.get('gslbNewCfgProximityMask', None)
        self.gslbNewCfgProximityAge = kwargs.get('gslbNewCfgProximityAge', None)
        self.gslbNewCfgGenSourceIpv6Prefix = kwargs.get('gslbNewCfgGenSourceIpv6Prefix', None)
        self.gslbNewCfgGenDsync = EnumGslbNewCfgGenDsync.enum(kwargs.get('gslbNewCfgGenDsync', None))
        self.gslbNewCfgProximityTimeAfterCalc = kwargs.get('gslbNewCfgProximityTimeAfterCalc', None)
        self.gslbNewCfgGenServcDownDnsRsp = EnumGslbNewCfgGenServcDownDnsRsp.enum(kwargs.get('gslbNewCfgGenServcDownDnsRsp', None))
        self.gslbNewCfgGenExcludeRedir = EnumGslbNewCfgGenExcludeRedir.enum(kwargs.get('gslbNewCfgGenExcludeRedir', None))
        self.gslbRemSiteTableMaxSize = kwargs.get('gslbRemSiteTableMaxSize', None)
        self.gslbEnhNetworkTableMaxSize = kwargs.get('gslbEnhNetworkTableMaxSize', None)
        self.gslbRuleTableMaxSize = kwargs.get('gslbRuleTableMaxSize', None)
        self.gslbMetricTableMaxSize = kwargs.get('gslbMetricTableMaxSize', None)
        self.gslbNewCfgDnsSecGlobalEnabled = EnumGslbNewCfgDnsSecGlobalEnabled.enum(kwargs.get('gslbNewCfgDnsSecGlobalEnabled', None))
        self.gslbNewCfgDnsSecGlobalRollTm = kwargs.get('gslbNewCfgDnsSecGlobalRollTm', None)
        self.gslbNewCfgDnsSecGlobalType = EnumGslbNewCfgDnsSecGlobalType.enum(kwargs.get('gslbNewCfgDnsSecGlobalType', None))
        self.gslbNewCfgDnsSecGlobalKskRollTm = kwargs.get('gslbNewCfgDnsSecGlobalKskRollTm', None)
        self.gslbNewCfgDnsSecGlobalNsec3SaltLen = kwargs.get('gslbNewCfgDnsSecGlobalNsec3SaltLen', None)
        self.gslbNewCfgDnsSecGlobalNsec3SaltLifetime = kwargs.get('gslbNewCfgDnsSecGlobalNsec3SaltLifetime', None)
        self.gslbNewCfgDnsSecGlobalNsec3HashIterations = kwargs.get('gslbNewCfgDnsSecGlobalNsec3HashIterations', None)
        self.gslbNewCfgDnsSecGlobalSMPTServerUserName = kwargs.get('gslbNewCfgDnsSecGlobalSMPTServerUserName', None)
        self.gslbNewCfgDnsSecGlobalNsec3Algorithm = EnumGslbNewCfgDnsSecGlobalNsec3Algorithm.enum(kwargs.get('gslbNewCfgDnsSecGlobalNsec3Algorithm', None))
        self.gslbNewCfgDnsSecGlobalKeyMaster = EnumGslbNewCfgDnsSecGlobalKeyMaster.enum(kwargs.get('gslbNewCfgDnsSecGlobalKeyMaster', None))
        self.gslbDnsSecImportExportSCPHostName = kwargs.get('gslbDnsSecImportExportSCPHostName', None)
        self.gslbDnsSecImportExportSCPFileName = kwargs.get('gslbDnsSecImportExportSCPFileName', None)
        self.gslbDnsSecImportExportSCPUserName = kwargs.get('gslbDnsSecImportExportSCPUserName', None)
        self.gslbDnsSecImportExportSCPPassword = kwargs.get('gslbDnsSecImportExportSCPPassword', None)
        self.gslbDnsSecImportExportKeyID = kwargs.get('gslbDnsSecImportExportKeyID', None)
        self.gslbDnsSecImportExportZoneID = kwargs.get('gslbDnsSecImportExportZoneID', None)
        self.gslbDnsSecImportExportPassphrase = kwargs.get('gslbDnsSecImportExportPassphrase', None)
        self.gslbDnsSecImportExportComponentType = EnumGslbDnsSecImportExportComponentType.enum(kwargs.get('gslbDnsSecImportExportComponentType', None))
        self.gslbDnsSecImportExportPortType = EnumGslbDnsSecImportExportPortType.enum(kwargs.get('gslbDnsSecImportExportPortType', None))
        self.gslbDnsSecImportExportImpKeyType = EnumGslbDnsSecImportExportImpKeyType.enum(kwargs.get('gslbDnsSecImportExportImpKeyType', None))
        self.gslbDnsSecImportExportImpKeyStatus = EnumGslbDnsSecImportExportImpKeyStatus.enum(kwargs.get('gslbDnsSecImportExportImpKeyStatus', None))
        self.gslbDnsSecImportExportImpKeySize = EnumGslbDnsSecImportExportImpKeySize.enum(kwargs.get('gslbDnsSecImportExportImpKeySize', None))
        self.gslbDnsSecImportExportImpKeyAlgo = EnumGslbDnsSecImportExportImpKeyAlgo.enum(kwargs.get('gslbDnsSecImportExportImpKeyAlgo', None))
        self.gslbDnsSecImportExportImpKeyTTL = kwargs.get('gslbDnsSecImportExportImpKeyTTL', None)
        self.gslbDnsSecImportExportImpKeyExpPeriod = kwargs.get('gslbDnsSecImportExportImpKeyExpPeriod', None)
        self.gslbDnsSecImportExportImpKeyRollOverPeriod = kwargs.get('gslbDnsSecImportExportImpKeyRollOverPeriod', None)
        self.gslbDnsSecImportExportImpKeyValidityPeriod = kwargs.get('gslbDnsSecImportExportImpKeyValidityPeriod', None)
        self.gslbDnsSecImportExportImpKeyPublicationPeriod = kwargs.get('gslbDnsSecImportExportImpKeyPublicationPeriod', None)
        self.gslbDnsSecImportExportAction = EnumGslbDnsSecImportExportAction.enum(kwargs.get('gslbDnsSecImportExportAction', None))
        self.gslbNewCfgLLBProxAging = kwargs.get('gslbNewCfgLLBProxAging', None)
        self.gslbNewCfgLLBProxInterval = kwargs.get('gslbNewCfgLLBProxInterval', None)
        self.gslbNewCfgLLBProxRetry = kwargs.get('gslbNewCfgLLBProxRetry', None)
        self.gslbNewCfgLLBProxMask = kwargs.get('gslbNewCfgLLBProxMask', None)
        self.gslbNewCfgLLBProxPrfx = kwargs.get('gslbNewCfgLLBProxPrfx', None)
        self.gslbNewCfgLLBProxonOff = EnumGslbNewCfgLLBProxonOff.enum(kwargs.get('gslbNewCfgLLBProxonOff', None))
        self.gslbNewDnsResLPWizardFirstIpVersion = EnumGslbNewDnsResLPWizardFirstIpVersion.enum(kwargs.get('gslbNewDnsResLPWizardFirstIpVersion', None))
        self.gslbNewDnsResLPWizardSecondIpVersion = EnumGslbNewDnsResLPWizardSecondIpVersion.enum(kwargs.get('gslbNewDnsResLPWizardSecondIpVersion', None))
        self.gslbNewDnsResLPWizardThirdIpVersion = EnumGslbNewDnsResLPWizardThirdIpVersion.enum(kwargs.get('gslbNewDnsResLPWizardThirdIpVersion', None))
        self.gslbNewDnsResLPWizardFirstIpv4Addr = kwargs.get('gslbNewDnsResLPWizardFirstIpv4Addr', None)
        self.gslbNewDnsResLPWizardFirstIpv6Addr = kwargs.get('gslbNewDnsResLPWizardFirstIpv6Addr', None)
        self.gslbNewDnsResLPWizardSecondIpv4Addr = kwargs.get('gslbNewDnsResLPWizardSecondIpv4Addr', None)
        self.gslbNewDnsResLPWizardSecondIpv6Addr = kwargs.get('gslbNewDnsResLPWizardSecondIpv6Addr', None)
        self.gslbNewDnsResLPWizardThirdIpv4Addr = kwargs.get('gslbNewDnsResLPWizardThirdIpv4Addr', None)
        self.gslbNewDnsResLPWizardThirdIpv6Addr = kwargs.get('gslbNewDnsResLPWizardThirdIpv6Addr', None)
        self.gslbNewDnsProxyDefaultgroup = kwargs.get('gslbNewDnsProxyDefaultgroup', None)
        self.gslbCurDnsSoaDefaultRefresh = kwargs.get('gslbCurDnsSoaDefaultRefresh', None)
        self.gslbCurDnsSoaDefaultRetry = kwargs.get('gslbCurDnsSoaDefaultRetry', None)
        self.gslbCurDnsSoaDefaultExpire = kwargs.get('gslbCurDnsSoaDefaultExpire', None)
        self.gslbCurDnsSoaDefaultMinTtl = kwargs.get('gslbCurDnsSoaDefaultMinTtl', None)
        self.gslbCurDnsSoaZoneTableMaxEntries = kwargs.get('gslbCurDnsSoaZoneTableMaxEntries', None)
        self.hcsTableMaxSize = kwargs.get('hcsTableMaxSize', None)
        self.snmphcTableMaxSize = kwargs.get('snmphcTableMaxSize', None)
        self.curCfgFilterTableSize = kwargs.get('curCfgFilterTableSize', None)
        self.newCfgFilterTableSize = kwargs.get('newCfgFilterTableSize', None)
        self.curCfgRealServerTableSize = kwargs.get('curCfgRealServerTableSize', None)
        self.newCfgRealServerTableSize = kwargs.get('newCfgRealServerTableSize', None)
        self.curCfgRealServerGroupTableSize = kwargs.get('curCfgRealServerGroupTableSize', None)
        self.newCfgRealServerGroupTableSize = kwargs.get('newCfgRealServerGroupTableSize', None)
        self.curCfgVirtServerTableSize = kwargs.get('curCfgVirtServerTableSize', None)
        self.newCfgVirtServerTableSize = kwargs.get('newCfgVirtServerTableSize', None)
        self.pipTableMaxSize = kwargs.get('pipTableMaxSize', None)
        self.pipNewCfgBaseType = EnumPipNewCfgBaseType.enum(kwargs.get('pipNewCfgBaseType', None))
        self.slbStatMaintMaximumSessions = kwargs.get('slbStatMaintMaximumSessions', None)
        self.slbStatMaintCurBindings = kwargs.get('slbStatMaintCurBindings', None)
        self.slbStatMaintCurBindings4Seconds = kwargs.get('slbStatMaintCurBindings4Seconds', None)
        self.slbStatMaintCurBindings64Seconds = kwargs.get('slbStatMaintCurBindings64Seconds', None)
        self.slbStatMaintTerminatedSessions = kwargs.get('slbStatMaintTerminatedSessions', None)
        self.slbStatMaintAllocFailures = kwargs.get('slbStatMaintAllocFailures', None)
        self.slbStatMaintNonTcpFrames = kwargs.get('slbStatMaintNonTcpFrames', None)
        self.slbStatMaintTcpFragments = kwargs.get('slbStatMaintTcpFragments', None)
        self.slbStatMaintUdpDatagrams = kwargs.get('slbStatMaintUdpDatagrams', None)
        self.slbIncorrectVirtServs = kwargs.get('slbIncorrectVirtServs', None)
        self.slbIncorrectVports = kwargs.get('slbIncorrectVports', None)
        self.slbNoRealServs = kwargs.get('slbNoRealServs', None)
        self.slbStatMaintBackupServActs = kwargs.get('slbStatMaintBackupServActs', None)
        self.slbStatMaintOverflowServActs = kwargs.get('slbStatMaintOverflowServActs', None)
        self.slbStatMaintFilteredDeniedFrames = kwargs.get('slbStatMaintFilteredDeniedFrames', None)
        self.slbStatMaintLandAttacks = kwargs.get('slbStatMaintLandAttacks', None)
        self.slbStatMaintIpFragTotalSessions = kwargs.get('slbStatMaintIpFragTotalSessions', None)
        self.slbStatMaintIpFragCurSessions = kwargs.get('slbStatMaintIpFragCurSessions', None)
        self.slbStatMaintIpFragDiscards = kwargs.get('slbStatMaintIpFragDiscards', None)
        self.slbStatMaintIpFragTableFull = kwargs.get('slbStatMaintIpFragTableFull', None)
        self.slbStatMaintIp6CurrSessions = kwargs.get('slbStatMaintIp6CurrSessions', None)
        self.slbIncorrectIp6Vip = kwargs.get('slbIncorrectIp6Vip', None)
        self.slbIncorrectIp6Vports = kwargs.get('slbIncorrectIp6Vports', None)
        self.slbStatMaintIp6PktDropped = kwargs.get('slbStatMaintIp6PktDropped', None)
        self.slbStatMaintOOSFinPktDrops = kwargs.get('slbStatMaintOOSFinPktDrops', None)
        self.slbStatMaintSymSessions = kwargs.get('slbStatMaintSymSessions', None)
        self.slbStatMaintSymValidSegments = kwargs.get('slbStatMaintSymValidSegments', None)
        self.slbStatMaintSymFragSessions = kwargs.get('slbStatMaintSymFragSessions', None)
        self.slbStatMaintSymSegAllocFails = kwargs.get('slbStatMaintSymSegAllocFails', None)
        self.slbStatLinkpfClearWanLinkServer = kwargs.get('slbStatLinkpfClearWanLinkServer', None)
        self.slbStatLinkpfClearWanLinkIP = kwargs.get('slbStatLinkpfClearWanLinkIP', None)
        self.slbStatLinkpfClearAll = EnumSlbStatLinkpfClearAll.enum(kwargs.get('slbStatLinkpfClearAll', None))
        self.slbStatLinkpfSmartNATID = kwargs.get('slbStatLinkpfSmartNATID', None)
        self.slbStatLinkpfSmartNATAll = EnumSlbStatLinkpfSmartNATAll.enum(kwargs.get('slbStatLinkpfSmartNATAll', None))
        self.slbStatMaintSymBufferAllocFails = kwargs.get('slbStatMaintSymBufferAllocFails', None)
        self.slbStatMaintSymConnAllocFails = kwargs.get('slbStatMaintSymConnAllocFails', None)
        self.slbStatMaintSymInvalidBuffers = kwargs.get('slbStatMaintSymInvalidBuffers', None)
        self.slbStatMaintSymSegReallocFails = kwargs.get('slbStatMaintSymSegReallocFails', None)
        self.slbStatMaintSymPacketsIn = kwargs.get('slbStatMaintSymPacketsIn', None)
        self.slbStatMaintSymPacketsWithNoData = kwargs.get('slbStatMaintSymPacketsWithNoData', None)
        self.slbStatMaintSymTcpPackets = kwargs.get('slbStatMaintSymTcpPackets', None)
        self.slbStatMaintSymUdpPackets = kwargs.get('slbStatMaintSymUdpPackets', None)
        self.slbStatMaintSymIcmpPackets = kwargs.get('slbStatMaintSymIcmpPackets', None)
        self.slbStatMaintSymOtherPackets = kwargs.get('slbStatMaintSymOtherPackets', None)
        self.slbStatMaintSymMatchCount = kwargs.get('slbStatMaintSymMatchCount', None)
        self.slbStatMaintSymFetchErrors = kwargs.get('slbStatMaintSymFetchErrors', None)
        self.slbStatMaintSymTruncPayloadToMp = kwargs.get('slbStatMaintSymTruncPayloadToMp', None)
        self.slbStatMaintSymPacketsInFastPath = kwargs.get('slbStatMaintSymPacketsInFastPath', None)
        self.slbStatMaintPeakBindings = kwargs.get('slbStatMaintPeakBindings', None)
        self.slbStatMaintCurAxBindings = kwargs.get('slbStatMaintCurAxBindings', None)
        self.slbStatMaintCurAxBindings4Seconds = kwargs.get('slbStatMaintCurAxBindings4Seconds', None)
        self.slbStatMaintCurAxBindings64Seconds = kwargs.get('slbStatMaintCurAxBindings64Seconds', None)
        self.slbStatMaintPeakAxBindings = kwargs.get('slbStatMaintPeakAxBindings', None)
        self.fltStatPsessCur = kwargs.get('fltStatPsessCur', None)
        self.fltStatPsessHigh = kwargs.get('fltStatPsessHigh', None)
        self.fltStatPsessTotal = kwargs.get('fltStatPsessTotal', None)
        self.gslbStatsClear = EnumGslbStatsClear.enum(kwargs.get('gslbStatsClear', None))
        self.gslbStatMaintInGoodSiteUpdates = kwargs.get('gslbStatMaintInGoodSiteUpdates', None)
        self.gslbStatMaintInBadSiteUpdates = kwargs.get('gslbStatMaintInBadSiteUpdates', None)
        self.gslbStatMaintOutSiteUpdates = kwargs.get('gslbStatMaintOutSiteUpdates', None)
        self.gslbStatMaintInGoodSiteUpdates2 = kwargs.get('gslbStatMaintInGoodSiteUpdates2', None)
        self.gslbStatMaintOutSiteUpdates2 = kwargs.get('gslbStatMaintOutSiteUpdates2', None)
        self.gslbStatMaintLocalSitePers = kwargs.get('gslbStatMaintLocalSitePers', None)
        self.gslbStatMaintInDns = kwargs.get('gslbStatMaintInDns', None)
        self.gslbStatMaintInBadDns = kwargs.get('gslbStatMaintInBadDns', None)
        self.gslbStatMaintOutDns = kwargs.get('gslbStatMaintOutDns', None)
        self.gslbStatMaintInHttp = kwargs.get('gslbStatMaintInHttp', None)
        self.gslbStatMaintInBadHttp = kwargs.get('gslbStatMaintInBadHttp', None)
        self.gslbStatMaintOutHttp = kwargs.get('gslbStatMaintOutHttp', None)
        self.gslbStatMaintNoServer = kwargs.get('gslbStatMaintNoServer', None)
        self.gslbStatMaintNoDomain = kwargs.get('gslbStatMaintNoDomain', None)
        self.gslbStatMaintHostHits = kwargs.get('gslbStatMaintHostHits', None)
        self.gslbStatMaintRuleHits = kwargs.get('gslbStatMaintRuleHits', None)
        self.gslbStatMaintVirtHits = kwargs.get('gslbStatMaintVirtHits', None)
        self.gslbStatMaintNoServerHost = kwargs.get('gslbStatMaintNoServerHost', None)
        self.gslbStatMaintNoServerRule = kwargs.get('gslbStatMaintNoServerRule', None)
        self.gslbStatMaintNoServerVirt = kwargs.get('gslbStatMaintNoServerVirt', None)
        self.gslbStatMaintLastNoResultDomain = kwargs.get('gslbStatMaintLastNoResultDomain', None)
        self.gslbStatMaintLastSrcIp = kwargs.get('gslbStatMaintLastSrcIp', None)
        self.gslbStatMaintThresholdHits = kwargs.get('gslbStatMaintThresholdHits', None)
        self.gslbStatMaintLastSrcIpV6 = kwargs.get('gslbStatMaintLastSrcIpV6', None)
        self.gslbStatGeoNA = kwargs.get('gslbStatGeoNA', None)
        self.gslbStatGeoSA = kwargs.get('gslbStatGeoSA', None)
        self.gslbStatGeoEU = kwargs.get('gslbStatGeoEU', None)
        self.gslbStatGeoCA = kwargs.get('gslbStatGeoCA', None)
        self.gslbStatGeoPR = kwargs.get('gslbStatGeoPR', None)
        self.gslbStatGeoSS = kwargs.get('gslbStatGeoSS', None)
        self.gslbStatGeoJP = kwargs.get('gslbStatGeoJP', None)
        self.gslbStatGeoTotal = kwargs.get('gslbStatGeoTotal', None)
        self.gslbStatGeoAF = kwargs.get('gslbStatGeoAF', None)
        self.gslbStatPersCurrent = kwargs.get('gslbStatPersCurrent', None)
        self.gslbStatPersHiwat = kwargs.get('gslbStatPersHiwat', None)
        self.gslbStatPersMax = kwargs.get('gslbStatPersMax', None)
        self.gslbStatDnsDomainPerseErrorsAll = kwargs.get('gslbStatDnsDomainPerseErrorsAll', None)
        self.gslbStatDnsSecCurrentRequestAll = kwargs.get('gslbStatDnsSecCurrentRequestAll', None)
        self.gslbStatDnsCurrentRequestAll = kwargs.get('gslbStatDnsCurrentRequestAll', None)
        self.gslbStatDnsTotalRequestAll = kwargs.get('gslbStatDnsTotalRequestAll', None)
        self.gslbStatDnsSecTotalRequestAll = kwargs.get('gslbStatDnsSecTotalRequestAll', None)
        self.gslbStatDnsSecRequestPercentAll = kwargs.get('gslbStatDnsSecRequestPercentAll', None)
        self.gslbStatDnsRequestPerSecAll = kwargs.get('gslbStatDnsRequestPerSecAll', None)
        self.gslbStatDnsSecRequestPerSecAll = kwargs.get('gslbStatDnsSecRequestPerSecAll', None)
        self.gslbStatDnsTcpRequestAll = kwargs.get('gslbStatDnsTcpRequestAll', None)
        self.gslbStatDnsUdpRequestAll = kwargs.get('gslbStatDnsUdpRequestAll', None)
        self.gslbStatDnsInvalidRequestAll = kwargs.get('gslbStatDnsInvalidRequestAll', None)
        self.gslbStatDnsNsecRecordAnsAll = kwargs.get('gslbStatDnsNsecRecordAnsAll', None)
        self.ftpSlbStatTotal = kwargs.get('ftpSlbStatTotal', None)
        self.ftpNatStatTotal = kwargs.get('ftpNatStatTotal', None)
        self.ftpStatActiveNatIndex = kwargs.get('ftpStatActiveNatIndex', None)
        self.ftpStatNatAckSeqDiff = kwargs.get('ftpStatNatAckSeqDiff', None)
        self.ftpStatSlbParseIndex = kwargs.get('ftpStatSlbParseIndex', None)
        self.ftpStatSlbParseAckSeqDiff = kwargs.get('ftpStatSlbParseAckSeqDiff', None)
        self.ftpStatModeSwitchError = kwargs.get('ftpStatModeSwitchError', None)
        self.radiusAcctReqs = kwargs.get('radiusAcctReqs', None)
        self.radiusAcctWrapReqs = kwargs.get('radiusAcctWrapReqs', None)
        self.radiusAcctStartReqs = kwargs.get('radiusAcctStartReqs', None)
        self.radiusAcctUpdateReqs = kwargs.get('radiusAcctUpdateReqs', None)
        self.radiusAcctStopReqs = kwargs.get('radiusAcctStopReqs', None)
        self.radiusAcctBadReqs = kwargs.get('radiusAcctBadReqs', None)
        self.radiusAcctAddSessionReqs = kwargs.get('radiusAcctAddSessionReqs', None)
        self.radiusAcctDeleteSessionReqs = kwargs.get('radiusAcctDeleteSessionReqs', None)
        self.radiusAcctReqFailsSPDead = kwargs.get('radiusAcctReqFailsSPDead', None)
        self.radiusAcctReqFailsDMAFails = kwargs.get('radiusAcctReqFailsDMAFails', None)
        self.radiusAcctReqWithFramedIp = kwargs.get('radiusAcctReqWithFramedIp', None)
        self.radiusAcctReqWithoutFramedIp = kwargs.get('radiusAcctReqWithoutFramedIp', None)
        self.tpcpAddSessReqs = kwargs.get('tpcpAddSessReqs', None)
        self.tpcpAddSessReqsFailsSPDead = kwargs.get('tpcpAddSessReqsFailsSPDead', None)
        self.tpcpDeleteSessReqs = kwargs.get('tpcpDeleteSessReqs', None)
        self.tpcpDeleteSessReqsFailsSPDead = kwargs.get('tpcpDeleteSessReqsFailsSPDead', None)
        self.wapRequestToWrongSP = kwargs.get('wapRequestToWrongSP', None)
        self.rtspStatControlConns = kwargs.get('rtspStatControlConns', None)
        self.rtspStatUDPStreams = kwargs.get('rtspStatUDPStreams', None)
        self.rtspStatRedirects = kwargs.get('rtspStatRedirects', None)
        self.rtspStatConnDenied = kwargs.get('rtspStatConnDenied', None)
        self.rtspStatAllocFails = kwargs.get('rtspStatAllocFails', None)
        self.rtspStatBufferAllocs = kwargs.get('rtspStatBufferAllocs', None)
        self.tcpLimitStatHoldDowns = kwargs.get('tcpLimitStatHoldDowns', None)
        self.tcpLimitStatClientEntries = kwargs.get('tcpLimitStatClientEntries', None)
        self.udpLimitStatHoldDowns = kwargs.get('udpLimitStatHoldDowns', None)
        self.icmpLimitStatHoldDowns = kwargs.get('icmpLimitStatHoldDowns', None)
        self.udpLimitStatClientEntries = kwargs.get('udpLimitStatClientEntries', None)
        self.icmpLimitStatClientEntries = kwargs.get('icmpLimitStatClientEntries', None)
        self.dnsSlbStatTCPQueries = kwargs.get('dnsSlbStatTCPQueries', None)
        self.dnsSlbStatUDPQueries = kwargs.get('dnsSlbStatUDPQueries', None)
        self.dnsSlbStatInvalidQueries = kwargs.get('dnsSlbStatInvalidQueries', None)
        self.dnsSlbStatMultipleQueries = kwargs.get('dnsSlbStatMultipleQueries', None)
        self.dnsSlbStatDnameParseErrors = kwargs.get('dnsSlbStatDnameParseErrors', None)
        self.dnsSlbStatFailedMatches = kwargs.get('dnsSlbStatFailedMatches', None)
        self.dnsSlbStatInternalErrors = kwargs.get('dnsSlbStatInternalErrors', None)
        self.slbStatsClear = EnumSlbStatsClear.enum(kwargs.get('slbStatsClear', None))
        self.slbStatsPeerClearConfirm = EnumSlbStatsPeerClearConfirm.enum(kwargs.get('slbStatsPeerClearConfirm', None))
        self.slbSfoSessMirrorStatus = EnumSlbSfoSessMirrorStatus.enum(kwargs.get('slbSfoSessMirrorStatus', None))
        self.slbSecondsFromLastStatsClear = kwargs.get('slbSecondsFromLastStatsClear', None)
        self.sslSlbStatSessIdAllocFails = kwargs.get('sslSlbStatSessIdAllocFails', None)
        self.sslSlbStatCurSessions = kwargs.get('sslSlbStatCurSessions', None)
        self.sslSlbStatTotalSessions = kwargs.get('sslSlbStatTotalSessions', None)
        self.sslSlbStatHighestSessions = kwargs.get('sslSlbStatHighestSessions', None)
        self.sslSlbStatUniqCurSessions = kwargs.get('sslSlbStatUniqCurSessions', None)
        self.sslSlbStatUniqTotalSessions = kwargs.get('sslSlbStatUniqTotalSessions', None)
        self.sslSlbStatUniqHighestSessions = kwargs.get('sslSlbStatUniqHighestSessions', None)
        self.sslSlbStatPersistPortCurSessions = kwargs.get('sslSlbStatPersistPortCurSessions', None)
        self.sslSlbStatPersistPortTotalSessions = kwargs.get('sslSlbStatPersistPortTotalSessions', None)
        self.sslSlbStatPersistPortHighestSessions = kwargs.get('sslSlbStatPersistPortHighestSessions', None)
        self.sipTotalClientParseErrors = kwargs.get('sipTotalClientParseErrors', None)
        self.sipTotalServerParseErrors = kwargs.get('sipTotalServerParseErrors', None)
        self.sipTotalUnknownMethodReq = kwargs.get('sipTotalUnknownMethodReq', None)
        self.sipTotalIncompleteMsgs = kwargs.get('sipTotalIncompleteMsgs', None)
        self.sipTotalSdpNatPackets = kwargs.get('sipTotalSdpNatPackets', None)
        self.sessMirrorTotalCreateSessionMsgRx = kwargs.get('sessMirrorTotalCreateSessionMsgRx', None)
        self.sessMirrorTotalCreateSessionMsgTx = kwargs.get('sessMirrorTotalCreateSessionMsgTx', None)
        self.sessMirrorTotalCreateDataSessionMsgRx = kwargs.get('sessMirrorTotalCreateDataSessionMsgRx', None)
        self.sessMirrorTotalCreateDataSessionMsgTx = kwargs.get('sessMirrorTotalCreateDataSessionMsgTx', None)
        self.sessMirrorTotalUpdateSessionMsgRx = kwargs.get('sessMirrorTotalUpdateSessionMsgRx', None)
        self.sessMirrorTotalUpdateSessionMsgTx = kwargs.get('sessMirrorTotalUpdateSessionMsgTx', None)
        self.sessMirrorTotalUpdateDataSessionMsgRx = kwargs.get('sessMirrorTotalUpdateDataSessionMsgRx', None)
        self.sessMirrorTotalUpdateDataSessionMsgTx = kwargs.get('sessMirrorTotalUpdateDataSessionMsgTx', None)
        self.sessMirrorTotalDeleteSessionMsgRx = kwargs.get('sessMirrorTotalDeleteSessionMsgRx', None)
        self.sessMirrorTotalDeleteSessionMsgTx = kwargs.get('sessMirrorTotalDeleteSessionMsgTx', None)
        self.sessMirrorTotalDeleteDataSessionMsgRx = kwargs.get('sessMirrorTotalDeleteDataSessionMsgRx', None)
        self.sessMirrorTotalDeleteDataSessionMsgTx = kwargs.get('sessMirrorTotalDeleteDataSessionMsgTx', None)
        self.sessMirrorTotalSessionsCreated = kwargs.get('sessMirrorTotalSessionsCreated', None)
        self.sessMirrorTotalDataSessionsCreated = kwargs.get('sessMirrorTotalDataSessionsCreated', None)
        self.sessMirrorTotalSessionsUpdated = kwargs.get('sessMirrorTotalSessionsUpdated', None)
        self.sessMirrorTotalDataSessionsUpdated = kwargs.get('sessMirrorTotalDataSessionsUpdated', None)
        self.sessMirrorTotalSessionsDeleted = kwargs.get('sessMirrorTotalSessionsDeleted', None)
        self.sessMirrorTotalDataSessionsDeleted = kwargs.get('sessMirrorTotalDataSessionsDeleted', None)
        self.sessMirrorSessionTableFullErr = kwargs.get('sessMirrorSessionTableFullErr', None)
        self.sessMirrorNoPortErr = kwargs.get('sessMirrorNoPortErr', None)
        self.sessMirrorSessionPresentErr = kwargs.get('sessMirrorSessionPresentErr', None)
        self.sessMirrorSessionNotFoundErr = kwargs.get('sessMirrorSessionNotFoundErr', None)
        self.sessMirrorCtrlSessionNotFoundErr = kwargs.get('sessMirrorCtrlSessionNotFoundErr', None)
        self.slbSessionInfoState = EnumSlbSessionInfoState.enum(kwargs.get('slbSessionInfoState', None))
        self.slbSessionInfoType = EnumSlbSessionInfoType.enum(kwargs.get('slbSessionInfoType', None))
        self.slbSessionInfoIpAddr = kwargs.get('slbSessionInfoIpAddr', None)
        self.slbSessionInfoFilterId = kwargs.get('slbSessionInfoFilterId', None)
        self.slbSessionInfoPortId = kwargs.get('slbSessionInfoPortId', None)
        self.slbSessionInfoFlag = EnumSlbSessionInfoFlag.enum(kwargs.get('slbSessionInfoFlag', None))
        self.slbSessionInfoStringFormatFlag = EnumSlbSessionInfoStringFormatFlag.enum(kwargs.get('slbSessionInfoStringFormatFlag', None))
        self.slbSessionInfoMaxSessDump = kwargs.get('slbSessionInfoMaxSessDump', None)
        self.slbNewAcclCfgFastViewOnOff = EnumSlbNewAcclCfgFastViewOnOff.enum(kwargs.get('slbNewAcclCfgFastViewOnOff', None))
        self.slbCurAcclCfgFastViewSupported = EnumSlbCurAcclCfgFastViewSupported.enum(kwargs.get('slbCurAcclCfgFastViewSupported', None))
        self.synAtkState = EnumSynAtkState.enum(kwargs.get('synAtkState', None))
        self.synAtkInterval = kwargs.get('synAtkInterval', None)
        self.synAtkThreshhold = kwargs.get('synAtkThreshhold', None)
        self.synAtkWarningFired = kwargs.get('synAtkWarningFired', None)
        self.synAtkResponseInterval = kwargs.get('synAtkResponseInterval', None)
        self.synAtkOnOff = EnumSynAtkOnOff.enum(kwargs.get('synAtkOnOff', None))
        self.slbFreeVirtualServerIndexInfo = kwargs.get('slbFreeVirtualServerIndexInfo', None)
        self.slbFreeRealGroupIndexInfo = kwargs.get('slbFreeRealGroupIndexInfo', None)
        self.slbFreeRealServerIndexInfo = kwargs.get('slbFreeRealServerIndexInfo', None)
        self.slbOperClearSessionTable = EnumSlbOperClearSessionTable.enum(kwargs.get('slbOperClearSessionTable', None))
        self.slbOperConfigSync = EnumSlbOperConfigSync.enum(kwargs.get('slbOperConfigSync', None))
        self.gslbOperRemove = EnumGslbOperRemove.enum(kwargs.get('gslbOperRemove', None))
        self.gslbOperClear = EnumGslbOperClear.enum(kwargs.get('gslbOperClear', None))
        self.gslbOperQueryDomain = kwargs.get('gslbOperQueryDomain', None)
        self.gslbOperQuerySrcIp = kwargs.get('gslbOperQuerySrcIp', None)
        self.gslbOperSendQuery = EnumGslbOperSendQuery.enum(kwargs.get('gslbOperSendQuery', None))
        self.gslbOperQuerySrcIpV6 = kwargs.get('gslbOperQuerySrcIpV6', None)
        self.gslbOperQuerySrcIpVer = EnumGslbOperQuerySrcIpVer.enum(kwargs.get('gslbOperQuerySrcIpVer', None))
        self.gslbOperQueryType = EnumGslbOperQueryType.enum(kwargs.get('gslbOperQueryType', None))
        self.gslbOperAddDomain = kwargs.get('gslbOperAddDomain', None)
        self.gslbOperAddSrcIp = kwargs.get('gslbOperAddSrcIp', None)
        self.gslbOperAddServerIp = kwargs.get('gslbOperAddServerIp', None)
        self.gslbOperAddEntry = EnumGslbOperAddEntry.enum(kwargs.get('gslbOperAddEntry', None))
        self.gslbOperAddSrcIp6 = kwargs.get('gslbOperAddSrcIp6', None)
        self.gslbOperAddServerIp6 = kwargs.get('gslbOperAddServerIp6', None)
        self.gslbOperAddNetIpMask = kwargs.get('gslbOperAddNetIpMask', None)
        self.gslbOperAddIpv6Prefix = kwargs.get('gslbOperAddIpv6Prefix', None)
        self.gslbOperAvPersisVirtNum = kwargs.get('gslbOperAvPersisVirtNum', None)
        self.gslbOperAvPersisState = EnumGslbOperAvPersisState.enum(kwargs.get('gslbOperAvPersisState', None))
        self.gslbOperAvpersistence = EnumGslbOperAvpersistence.enum(kwargs.get('gslbOperAvpersistence', None))
        self.slbOperSessionDelSrcIp = kwargs.get('slbOperSessionDelSrcIp', None)
        self.slbOperSessionDelSrcPort = kwargs.get('slbOperSessionDelSrcPort', None)
        self.slbOperSessionDelDestIp = kwargs.get('slbOperSessionDelDestIp', None)
        self.slbOperSessionDelDestPort = kwargs.get('slbOperSessionDelDestPort', None)
        self.slbOperSessionDelTransType = EnumSlbOperSessionDelTransType.enum(kwargs.get('slbOperSessionDelTransType', None))
        self.slbOperSessionDelete = EnumSlbOperSessionDelete.enum(kwargs.get('slbOperSessionDelete', None))
        self.slbOperOcspCachePurge = kwargs.get('slbOperOcspCachePurge', None)
        self.slbOperCdpCachePurge = kwargs.get('slbOperCdpCachePurge', None)
        self.slbOperSessionMoveSrcIp = kwargs.get('slbOperSessionMoveSrcIp', None)
        self.slbOperSessionMoveVirtId = kwargs.get('slbOperSessionMoveVirtId', None)
        self.slbOperSessionMoveGroupId = kwargs.get('slbOperSessionMoveGroupId', None)
        self.slbOperSessionMoveRealId = kwargs.get('slbOperSessionMoveRealId', None)
        self.slbOperSessionMoveRPort = kwargs.get('slbOperSessionMoveRPort', None)
        self.slbOperSessionMoveOper = EnumSlbOperSessionMoveOper.enum(kwargs.get('slbOperSessionMoveOper', None))
        self.slbOperPersSessionDelSessKeyType = EnumSlbOperPersSessionDelSessKeyType.enum(kwargs.get('slbOperPersSessionDelSessKeyType', None))
        self.slbOperPersSessionDelSessKey = kwargs.get('slbOperPersSessionDelSessKey', None)
        self.slbOperPersSessionDelVirtId = kwargs.get('slbOperPersSessionDelVirtId', None)
        self.slbOperPersSessionDelServPort = kwargs.get('slbOperPersSessionDelServPort', None)
        self.slbOperPersSessionDelRealId = kwargs.get('slbOperPersSessionDelRealId', None)
        self.slbOperPersSessionDelOper = EnumSlbOperPersSessionDelOper.enum(kwargs.get('slbOperPersSessionDelOper', None))
        self.slbNewCfgLinklbState = EnumSlbNewCfgLinklbState.enum(kwargs.get('slbNewCfgLinklbState', None))
        self.slbNewCfgLinklbRealGroup = kwargs.get('slbNewCfgLinklbRealGroup', None)
        self.slbNewCfgLinklbTTL = kwargs.get('slbNewCfgLinklbTTL', None)
        self.slbNewCfgLinklbEnhRealGroup = kwargs.get('slbNewCfgLinklbEnhRealGroup', None)
        self.slbDrecordTableMaxSize = kwargs.get('slbDrecordTableMaxSize', None)
        self.slbDrecordVirtRealMappingTableMaxSize = kwargs.get('slbDrecordVirtRealMappingTableMaxSize', None)
        self.slbNewSslCfgSSLAdminStatus = EnumSlbNewSslCfgSSLAdminStatus.enum(kwargs.get('slbNewSslCfgSSLAdminStatus', None))
        self.slbNewSslCfgCertsDefaultsCountryName = kwargs.get('slbNewSslCfgCertsDefaultsCountryName', None)
        self.slbNewSslCfgCertsDefaultsProvinceName = kwargs.get('slbNewSslCfgCertsDefaultsProvinceName', None)
        self.slbNewSslCfgCertsDefaultsLocallyName = kwargs.get('slbNewSslCfgCertsDefaultsLocallyName', None)
        self.slbNewSslCfgCertsDefaultsOrganizationName = kwargs.get('slbNewSslCfgCertsDefaultsOrganizationName', None)
        self.slbNewSslCfgCertsDefaultsOrganizationUnitName = kwargs.get('slbNewSslCfgCertsDefaultsOrganizationUnitName', None)
        self.slbNewSslCfgCertsDefaultsEMail = kwargs.get('slbNewSslCfgCertsDefaultsEMail', None)
        self.slbNewSslCfgSSLInspectKey = kwargs.get('slbNewSslCfgSSLInspectKey', None)
        self.slbNewSslCfgSSLInspectCacert = kwargs.get('slbNewSslCfgSSLInspectCacert', None)
        self.slbNewSslCfgSSLInspectMemsize = kwargs.get('slbNewSslCfgSSLInspectMemsize', None)
        self.slbNewSslCfgSSLInspectDeployment = EnumSlbNewSslCfgSSLInspectDeployment.enum(kwargs.get('slbNewSslCfgSSLInspectDeployment', None))
        self.slbNewSslCfgHwOffld = EnumSlbNewSslCfgHwOffld.enum(kwargs.get('slbNewSslCfgHwOffld', None))
        self.slbNewSslBereuseEna = EnumSlbNewSslBereuseEna.enum(kwargs.get('slbNewSslBereuseEna', None))
        self.slbNewSslBereuseSrcmtch = EnumSlbNewSslBereuseSrcmtch.enum(kwargs.get('slbNewSslBereuseSrcmtch', None))
        self.slbNewSslBereuseAging = kwargs.get('slbNewSslBereuseAging', None)
        self.slbSmtportTableMaxSize = kwargs.get('slbSmtportTableMaxSize', None)
        self.slbSmtportTableAvaibleIndex = kwargs.get('slbSmtportTableAvaibleIndex', None)
        self.slbWlmTableMaxSize = kwargs.get('slbWlmTableMaxSize', None)
        self.slbNewAcclCfgCachememcache = kwargs.get('slbNewAcclCfgCachememcache', None)
        self.slbNewAcclCfgCacheOnOff = EnumSlbNewAcclCfgCacheOnOff.enum(kwargs.get('slbNewAcclCfgCacheOnOff', None))
        self.slbNewAcclCfgCompOnOff = EnumSlbNewAcclCfgCompOnOff.enum(kwargs.get('slbNewAcclCfgCompOnOff', None))
        self.slbNewCfgClusterRole = EnumSlbNewCfgClusterRole.enum(kwargs.get('slbNewCfgClusterRole', None))
        self.slbNewCfgClusterFeprimaV4 = kwargs.get('slbNewCfgClusterFeprimaV4', None)
        self.slbNewCfgClusterFeprimaV6 = kwargs.get('slbNewCfgClusterFeprimaV6', None)
        self.slbNewCfgClusterFeseconV4 = kwargs.get('slbNewCfgClusterFeseconV4', None)
        self.slbNewCfgClusterFeseconV6 = kwargs.get('slbNewCfgClusterFeseconV6', None)
        self.slbNewCfgClusterFeprimaIpVer = EnumSlbNewCfgClusterFeprimaIpVer.enum(kwargs.get('slbNewCfgClusterFeprimaIpVer', None))
        self.slbNewCfgClusterFeseconIpVer = EnumSlbNewCfgClusterFeseconIpVer.enum(kwargs.get('slbNewCfgClusterFeseconIpVer', None))
        self.slbNewCfgClusterFeprima2V4 = kwargs.get('slbNewCfgClusterFeprima2V4', None)
        self.slbNewCfgClusterFeprima2V6 = kwargs.get('slbNewCfgClusterFeprima2V6', None)
        self.slbNewCfgClusterFesecon2V4 = kwargs.get('slbNewCfgClusterFesecon2V4', None)
        self.slbNewCfgClusterFesecon2V6 = kwargs.get('slbNewCfgClusterFesecon2V6', None)
        self.slbNewCfgClusterFeprima2IpVer = EnumSlbNewCfgClusterFeprima2IpVer.enum(kwargs.get('slbNewCfgClusterFeprima2IpVer', None))
        self.slbNewCfgClusterFesecon2IpVer = EnumSlbNewCfgClusterFesecon2IpVer.enum(kwargs.get('slbNewCfgClusterFesecon2IpVer', None))
        self.slbDataclassCfgDataClassesManualEntryCreationId = kwargs.get('slbDataclassCfgDataClassesManualEntryCreationId', None)
        self.fastviewStatSummTransactions = kwargs.get('fastviewStatSummTransactions', None)
        self.fastviewStatSummPages = kwargs.get('fastviewStatSummPages', None)
        self.fastviewStatSummOptimizedPages = kwargs.get('fastviewStatSummOptimizedPages', None)
        self.fastviewStatSummLearningPages = kwargs.get('fastviewStatSummLearningPages', None)
        self.fastviewStatSummTokensParsed = kwargs.get('fastviewStatSummTokensParsed', None)
        self.fastviewStatSummTokensRewritten = kwargs.get('fastviewStatSummTokensRewritten', None)
        self.fastviewStatSummBytesSavedImgReduction = kwargs.get('fastviewStatSummBytesSavedImgReduction', None)
        self.fastviewStatSummBytesBeforeImgReduction = kwargs.get('fastviewStatSummBytesBeforeImgReduction', None)
        self.fastviewStatSummBytesSavedPercent = kwargs.get('fastviewStatSummBytesSavedPercent', None)
        self.fastviewStatSummRespWithExpiryModified = kwargs.get('fastviewStatSummRespWithExpiryModified', None)
        self.fastviewStatSummExpiryModifiedPercent = kwargs.get('fastviewStatSummExpiryModifiedPercent', None)
        self.fastviewStatSummPeakTransactions = kwargs.get('fastviewStatSummPeakTransactions', None)
        self.fastviewStatSummPeakPages = kwargs.get('fastviewStatSummPeakPages', None)
        self.fastviewStatSummPeakOptimizedPages = kwargs.get('fastviewStatSummPeakOptimizedPages', None)
        self.fastviewStatSummPeakLearningPages = kwargs.get('fastviewStatSummPeakLearningPages', None)
        self.fastviewStatSummPeakTokensParsed = kwargs.get('fastviewStatSummPeakTokensParsed', None)
        self.fastviewStatSummPeakTokensRewritten = kwargs.get('fastviewStatSummPeakTokensRewritten', None)
        self.fastviewStatSummTotTransactions = kwargs.get('fastviewStatSummTotTransactions', None)
        self.fastviewStatSummTotPages = kwargs.get('fastviewStatSummTotPages', None)
        self.fastviewStatSummTotOptimizedPages = kwargs.get('fastviewStatSummTotOptimizedPages', None)
        self.fastviewStatSummTotLearningPages = kwargs.get('fastviewStatSummTotLearningPages', None)
        self.fastviewStatSummTotTokensParsed = kwargs.get('fastviewStatSummTotTokensParsed', None)
        self.fastviewStatSummTotTokensRewritten = kwargs.get('fastviewStatSummTotTokensRewritten', None)
        self.fastviewStatSummTotBytesSavedImgReduction = kwargs.get('fastviewStatSummTotBytesSavedImgReduction', None)
        self.fastviewStatSummTotBytesBeforeImgReduction = kwargs.get('fastviewStatSummTotBytesBeforeImgReduction', None)
        self.fastviewStatSummTotBytesSavedPercent = kwargs.get('fastviewStatSummTotBytesSavedPercent', None)
        self.fastviewStatSummTotRespWithExpiryModified = kwargs.get('fastviewStatSummTotRespWithExpiryModified', None)
        self.fastviewStatSummTotExpiryModifiedPercent = kwargs.get('fastviewStatSummTotExpiryModifiedPercent', None)
        self.fastviewStatSummCompiledPages = kwargs.get('fastviewStatSummCompiledPages', None)
        self.fastviewStatSummPeakCompiledPages = kwargs.get('fastviewStatSummPeakCompiledPages', None)
        self.fastviewStatSummTotCompiledPages = kwargs.get('fastviewStatSummTotCompiledPages', None)
        self.cachStatSummTotObj = kwargs.get('cachStatSummTotObj', None)
        self.cachStatSummHitPerc = kwargs.get('cachStatSummHitPerc', None)
        self.cachStatSummServRate = kwargs.get('cachStatSummServRate', None)
        self.cachStatSummNewCachedObj = kwargs.get('cachStatSummNewCachedObj', None)
        self.cachStatPeakNewCachedObj = kwargs.get('cachStatPeakNewCachedObj', None)
        self.cachStatSummRateNewCachedObj = kwargs.get('cachStatSummRateNewCachedObj', None)
        self.cachStatSummNewCachedBytes = kwargs.get('cachStatSummNewCachedBytes', None)
        self.cachStatSummRateNewCachedBytes = kwargs.get('cachStatSummRateNewCachedBytes', None)
        self.cachStatSummObjSmaller10K = kwargs.get('cachStatSummObjSmaller10K', None)
        self.cachStatSummObj11KTO50K = kwargs.get('cachStatSummObj11KTO50K', None)
        self.cachStatSummObj51KTO100K = kwargs.get('cachStatSummObj51KTO100K', None)
        self.cachStatSummObj101KTO1M = kwargs.get('cachStatSummObj101KTO1M', None)
        self.cachStatSummObjLarger1M = kwargs.get('cachStatSummObjLarger1M', None)
        self.compUnCompressedThrputKB = kwargs.get('compUnCompressedThrputKB', None)
        self.compAvgSizeBefCompKB = kwargs.get('compAvgSizeBefCompKB', None)
        self.compCompressedThrputKB = kwargs.get('compCompressedThrputKB', None)
        self.compAvgSizeAftCompKB = kwargs.get('compAvgSizeAftCompKB', None)
        self.compAvgCompRatio = kwargs.get('compAvgCompRatio', None)
        self.compThrputCompRatio = kwargs.get('compThrputCompRatio', None)
        self.compBytesSaved = kwargs.get('compBytesSaved', None)
        self.compBytesSavedPeak = kwargs.get('compBytesSavedPeak', None)
        self.compBytesSavedTot = kwargs.get('compBytesSavedTot', None)
        self.sslOffNewHandShake = kwargs.get('sslOffNewHandShake', None)
        self.sslOffReusedHandShake = kwargs.get('sslOffReusedHandShake', None)
        self.sslOffPerReusedHandShake = kwargs.get('sslOffPerReusedHandShake', None)
        self.sslOffPercSessUsingSSLv2 = kwargs.get('sslOffPercSessUsingSSLv2', None)
        self.sslOffPercSessUsingSSLv3 = kwargs.get('sslOffPercSessUsingSSLv3', None)
        self.sslOffPercSessUsingTLS = kwargs.get('sslOffPercSessUsingTLS', None)
        self.sslOffPercSessUsingTLS11 = kwargs.get('sslOffPercSessUsingTLS11', None)
        self.sslOffPercSessUsingTLS12 = kwargs.get('sslOffPercSessUsingTLS12', None)
        self.sslOffPerRejectedHandShake = kwargs.get('sslOffPerRejectedHandShake', None)
        self.sslOffByCipherHandShake = kwargs.get('sslOffByCipherHandShake', None)
        self.sslOffPerRejectedCertificates = kwargs.get('sslOffPerRejectedCertificates', None)
        self.sslOffPerIgnoredCertificates = kwargs.get('sslOffPerIgnoredCertificates', None)
        self.sslOffPerExpiredCertificates = kwargs.get('sslOffPerExpiredCertificates', None)
        self.sslOffPerUntrustedCertificates = kwargs.get('sslOffPerUntrustedCertificates', None)
        self.sslOffPerCertificateHostnameMismatches = kwargs.get('sslOffPerCertificateHostnameMismatches', None)
        self.sslOffBeNewHandShake = kwargs.get('sslOffBeNewHandShake', None)
        self.sslOffBeReusedHandShake = kwargs.get('sslOffBeReusedHandShake', None)
        self.sslOffBePerReusedHandShake = kwargs.get('sslOffBePerReusedHandShake', None)
        self.sslOffBePerRejectedHandShake = kwargs.get('sslOffBePerRejectedHandShake', None)
        self.sslOffBePercSessUsingSSLv3 = kwargs.get('sslOffBePercSessUsingSSLv3', None)
        self.sslOffBePercSessUsingTLS = kwargs.get('sslOffBePercSessUsingTLS', None)
        self.sslOffBePercSessUsingTLS11 = kwargs.get('sslOffBePercSessUsingTLS11', None)
        self.sslOffBePercSessUsingTLS12 = kwargs.get('sslOffBePercSessUsingTLS12', None)
        self.sslOffNewHandShakeTotal = kwargs.get('sslOffNewHandShakeTotal', None)
        self.sslOffBeNewHandShakeTotal = kwargs.get('sslOffBeNewHandShakeTotal', None)
        self.sslOffReusedHandShakeTotal = kwargs.get('sslOffReusedHandShakeTotal', None)
        self.sslOffBeReusedHandShakeTotal = kwargs.get('sslOffBeReusedHandShakeTotal', None)
        self.sslOffPerReusedHandShakeTotal = kwargs.get('sslOffPerReusedHandShakeTotal', None)
        self.sslOffBePerReusedHandShakeTotal = kwargs.get('sslOffBePerReusedHandShakeTotal', None)
        self.sslOffPerRejectedHandShakeTotal = kwargs.get('sslOffPerRejectedHandShakeTotal', None)
        self.sslOffBePerRejectedHandShakeTotal = kwargs.get('sslOffBePerRejectedHandShakeTotal', None)
        self.sslOffPercSessUsingSSLv3Total = kwargs.get('sslOffPercSessUsingSSLv3Total', None)
        self.sslOffBePercSessUsingSSLv3Total = kwargs.get('sslOffBePercSessUsingSSLv3Total', None)
        self.sslOffPercSessUsingTLSTotal = kwargs.get('sslOffPercSessUsingTLSTotal', None)
        self.sslOffBePercSessUsingTLSTotal = kwargs.get('sslOffBePercSessUsingTLSTotal', None)
        self.sslOffPercSessUsingTLS11Total = kwargs.get('sslOffPercSessUsingTLS11Total', None)
        self.sslOffBePercSessUsingTLS11Total = kwargs.get('sslOffBePercSessUsingTLS11Total', None)
        self.sslOffPercSessUsingTLS12Total = kwargs.get('sslOffPercSessUsingTLS12Total', None)
        self.sslOffBePercSessUsingTLS12Total = kwargs.get('sslOffBePercSessUsingTLS12Total', None)
        self.httpStatSummCliusingKeepAliv = kwargs.get('httpStatSummCliusingKeepAliv', None)
        self.httpStatSummHTTP10Per = kwargs.get('httpStatSummHTTP10Per', None)
        self.httpStatSummHTTP11Per = kwargs.get('httpStatSummHTTP11Per', None)
        self.httpStatSummHttpToHttpsRedir = kwargs.get('httpStatSummHttpToHttpsRedir', None)
        self.httpStatSummAvgNumReqPerConn = kwargs.get('httpStatSummAvgNumReqPerConn', None)
        self.httpStatSummResSmall1Kb = kwargs.get('httpStatSummResSmall1Kb', None)
        self.httpStatSummRes1KbTo10Kb = kwargs.get('httpStatSummRes1KbTo10Kb', None)
        self.httpStatSummRes11KbTo50Kb = kwargs.get('httpStatSummRes11KbTo50Kb', None)
        self.httpStatSummRes51KbTo100Kb = kwargs.get('httpStatSummRes51KbTo100Kb', None)
        self.httpStatSummResLarger100Kb = kwargs.get('httpStatSummResLarger100Kb', None)
        self.httpTransSummReqCliToAas = kwargs.get('httpTransSummReqCliToAas', None)
        self.httpTransSummReqAasToSer = kwargs.get('httpTransSummReqAasToSer', None)
        self.httpTransSummResSerToAas = kwargs.get('httpTransSummResSerToAas', None)
        self.httpTransSummResAasToCli = kwargs.get('httpTransSummResAasToCli', None)
        self.httpTransSummTransRate = kwargs.get('httpTransSummTransRate', None)
        self.httpStatSummHTTP20ConnectionCount = kwargs.get('httpStatSummHTTP20ConnectionCount', None)
        self.httpStatSummHTTP11ConnectionCount = kwargs.get('httpStatSummHTTP11ConnectionCount', None)
        self.httpStatSummHTTP10ConnectionCount = kwargs.get('httpStatSummHTTP10ConnectionCount', None)
        self.httpStatSummHTTP20ConnectionPeak = kwargs.get('httpStatSummHTTP20ConnectionPeak', None)
        self.httpStatSummHTTP11ConnectionPeak = kwargs.get('httpStatSummHTTP11ConnectionPeak', None)
        self.httpStatSummHTTP10ConnectionPeak = kwargs.get('httpStatSummHTTP10ConnectionPeak', None)
        self.httpStatSummHTTP20RequestCount = kwargs.get('httpStatSummHTTP20RequestCount', None)
        self.httpStatSummHTTP11RequestCount = kwargs.get('httpStatSummHTTP11RequestCount', None)
        self.httpStatSummHTTP10RequestCount = kwargs.get('httpStatSummHTTP10RequestCount', None)
        self.connmngStatSummServConn = kwargs.get('connmngStatSummServConn', None)
        self.connmngStatSummCliReq = kwargs.get('connmngStatSummCliReq', None)
        self.connmngStatSummMulRatio = kwargs.get('connmngStatSummMulRatio', None)
        self.tcpConnmngStatSummServConn = kwargs.get('tcpConnmngStatSummServConn', None)
        self.tcpConnmngStatSummServConnReuse = kwargs.get('tcpConnmngStatSummServConnReuse', None)
        self.tcpConnmngStatSummCliTrans = kwargs.get('tcpConnmngStatSummCliTrans', None)
        self.tcpConnmngStatSummMulRatio = kwargs.get('tcpConnmngStatSummMulRatio', None)
        self.tcpConnmngStatSummTotalServConn = kwargs.get('tcpConnmngStatSummTotalServConn', None)
        self.tcpConnmngStatSummTotalServConnReuse = kwargs.get('tcpConnmngStatSummTotalServConnReuse', None)
        self.tcpConnmngStatSummTotalCliTrans = kwargs.get('tcpConnmngStatSummTotalCliTrans', None)
        self.tcpConnmngStatSummTotalMulRatio = kwargs.get('tcpConnmngStatSummTotalMulRatio', None)
        self.slbSapAslrTableMaxSize = kwargs.get('slbSapAslrTableMaxSize', None)
        self.slbNewAppwallGenCfgWaf = EnumSlbNewAppwallGenCfgWaf.enum(kwargs.get('slbNewAppwallGenCfgWaf', None))
        self.slbNewAppwallGenCfgAuthSso = EnumSlbNewAppwallGenCfgAuthSso.enum(kwargs.get('slbNewAppwallGenCfgAuthSso', None))
        self.slbNewAppwallReporterIpAddress = kwargs.get('slbNewAppwallReporterIpAddress', None)
        self.slbNewAppwallReporterPort = kwargs.get('slbNewAppwallReporterPort', None)
        self.slbNewAppwallReporterPciRep = EnumSlbNewAppwallReporterPciRep.enum(kwargs.get('slbNewAppwallReporterPciRep', None))
        self.slbNewAppwallReporterSecLog = EnumSlbNewAppwallReporterSecLog.enum(kwargs.get('slbNewAppwallReporterSecLog', None))
        self.slbNewAppwallReporterAudit = EnumSlbNewAppwallReporterAudit.enum(kwargs.get('slbNewAppwallReporterAudit', None))
        self.slbNewAppwallReporterOthLog = EnumSlbNewAppwallReporterOthLog.enum(kwargs.get('slbNewAppwallReporterOthLog', None))
        self.slbNewAppwallReporterTenant = EnumSlbNewAppwallReporterTenant.enum(kwargs.get('slbNewAppwallReporterTenant', None))
        self.slbNewAppwallReporterTenantHdrName = kwargs.get('slbNewAppwallReporterTenantHdrName', None)
        self.slbNewAppwallReporterTenantHdrNameId = kwargs.get('slbNewAppwallReporterTenantHdrNameId', None)
        self.slbNewAppwallReporterOnOff = EnumSlbNewAppwallReporterOnOff.enum(kwargs.get('slbNewAppwallReporterOnOff', None))
        self.slbNewAppwallReporterHighPrio = EnumSlbNewAppwallReporterHighPrio.enum(kwargs.get('slbNewAppwallReporterHighPrio', None))
        self.slbNewLpOn = EnumSlbNewLpOn.enum(kwargs.get('slbNewLpOn', None))
        self.slbNewCfgSmartNatState = EnumSlbNewCfgSmartNatState.enum(kwargs.get('slbNewCfgSmartNatState', None))
        self.slbGslbProximityClear = EnumSlbGslbProximityClear.enum(kwargs.get('slbGslbProximityClear', None))
        self.slbNewCfgUrlRedirNonGetOrigSrv = EnumSlbNewCfgUrlRedirNonGetOrigSrv.enum(kwargs.get('slbNewCfgUrlRedirNonGetOrigSrv', None))
        self.slbNewCfgUrlRedirCookieOrigSrv = EnumSlbNewCfgUrlRedirCookieOrigSrv.enum(kwargs.get('slbNewCfgUrlRedirCookieOrigSrv', None))
        self.slbNewCfgUrlRedirNoCacheOrigSrv = EnumSlbNewCfgUrlRedirNoCacheOrigSrv.enum(kwargs.get('slbNewCfgUrlRedirNoCacheOrigSrv', None))
        self.slbNewCfgUrlRedirUriHashLength = kwargs.get('slbNewCfgUrlRedirUriHashLength', None)
        self.slbNewCfgUrlRedirHeader = EnumSlbNewCfgUrlRedirHeader.enum(kwargs.get('slbNewCfgUrlRedirHeader', None))
        self.slbNewCfgUrlRedirHeaderName = kwargs.get('slbNewCfgUrlRedirHeaderName', None)
        self.slbNewCfgUrlHashing = EnumSlbNewCfgUrlHashing.enum(kwargs.get('slbNewCfgUrlHashing', None))
        self.slbNewCfgUrlRedirHeaderNameType = EnumSlbNewCfgUrlRedirHeaderNameType.enum(kwargs.get('slbNewCfgUrlRedirHeaderNameType', None))
        self.slbOperSslInspectionCachePurge = kwargs.get('slbOperSslInspectionCachePurge', None)
        self.slbOperUrlfCachePurge = kwargs.get('slbOperUrlfCachePurge', None)
        self.slbUrlLbPathTableMaxSize = kwargs.get('slbUrlLbPathTableMaxSize', None)
        self.slbNewCfgUrlLbErrorMsg = kwargs.get('slbNewCfgUrlLbErrorMsg', None)
        self.slbNewCfgUrlLbCaseSensitiveStrMatch = EnumSlbNewCfgUrlLbCaseSensitiveStrMatch.enum(kwargs.get('slbNewCfgUrlLbCaseSensitiveStrMatch', None))
        self.slbUrlHttpMethodsTableMaxSize = kwargs.get('slbUrlHttpMethodsTableMaxSize', None)
        self.layer7NewCfgDbindTimeout = kwargs.get('layer7NewCfgDbindTimeout', None)
        self.layer7NewCfgURLFilteringEna = kwargs.get('layer7NewCfgURLFilteringEna', None)
        self.layer7NewCfgURLFilteringCacheSize = kwargs.get('layer7NewCfgURLFilteringCacheSize', None)
        self.slbSdpTableMaxSize = kwargs.get('slbSdpTableMaxSize', None)
        self.urlStatRedRedirs = kwargs.get('urlStatRedRedirs', None)
        self.urlStatRedOrigSrvs = kwargs.get('urlStatRedOrigSrvs', None)
        self.urlStatRedNonGets = kwargs.get('urlStatRedNonGets', None)
        self.urlStatRedCookie = kwargs.get('urlStatRedCookie', None)
        self.urlStatRedNoCache = kwargs.get('urlStatRedNoCache', None)
        self.urlStatRedStraightOrigSrvs = kwargs.get('urlStatRedStraightOrigSrvs', None)
        self.urlStatRedRtspCacheSrvs = kwargs.get('urlStatRedRtspCacheSrvs', None)
        self.urlStatRedRtspOrigSrvs = kwargs.get('urlStatRedRtspOrigSrvs', None)
        self.urlMaintStatClientReset = kwargs.get('urlMaintStatClientReset', None)
        self.urlMaintStatServerReset = kwargs.get('urlMaintStatServerReset', None)
        self.urlMaintStatConnSplicing = kwargs.get('urlMaintStatConnSplicing', None)
        self.urlMaintStatHalfOpens = kwargs.get('urlMaintStatHalfOpens', None)
        self.urlMaintStatSwitchRetries = kwargs.get('urlMaintStatSwitchRetries', None)
        self.urlMaintStatRandomEarlyDrops = kwargs.get('urlMaintStatRandomEarlyDrops', None)
        self.urlMaintStatReqTooLong = kwargs.get('urlMaintStatReqTooLong', None)
        self.urlMaintStatInvalidHandshakes = kwargs.get('urlMaintStatInvalidHandshakes', None)
        self.urlMaintStatCurSPMemUnits = kwargs.get('urlMaintStatCurSPMemUnits', None)
        self.urlMaintStatCurSEQBufEntries = kwargs.get('urlMaintStatCurSEQBufEntries', None)
        self.urlMaintStatHighestSEQBufEntries = kwargs.get('urlMaintStatHighestSEQBufEntries', None)
        self.urlMaintStatCurDataBufUse = kwargs.get('urlMaintStatCurDataBufUse', None)
        self.urlMaintStatHighestDataBufUse = kwargs.get('urlMaintStatHighestDataBufUse', None)
        self.urlMaintStatCurSPBufEntries = kwargs.get('urlMaintStatCurSPBufEntries', None)
        self.urlMaintStatHighestSPBufEntries = kwargs.get('urlMaintStatHighestSPBufEntries', None)
        self.urlMaintStatTotalNonZeroSEQAlloc = kwargs.get('urlMaintStatTotalNonZeroSEQAlloc', None)
        self.urlMaintStatTotalSEQBufAllocs = kwargs.get('urlMaintStatTotalSEQBufAllocs', None)
        self.urlMaintStatTotalSEQBufFrees = kwargs.get('urlMaintStatTotalSEQBufFrees', None)
        self.urlMaintStatTotalDataBufAllocs = kwargs.get('urlMaintStatTotalDataBufAllocs', None)
        self.urlMaintStatTotalDataBufFrees = kwargs.get('urlMaintStatTotalDataBufFrees', None)
        self.urlMaintStatSeqBufAllocFails = kwargs.get('urlMaintStatSeqBufAllocFails', None)
        self.urlMaintStatUBufAllocFails = kwargs.get('urlMaintStatUBufAllocFails', None)
        self.urlMaintStatMaxSessPerBucket = kwargs.get('urlMaintStatMaxSessPerBucket', None)
        self.urlMaintStatMaxFramesPerSess = kwargs.get('urlMaintStatMaxFramesPerSess', None)
        self.urlMaintStatMaxBytesBuffered = kwargs.get('urlMaintStatMaxBytesBuffered', None)
        self.urlMaintStatInvalidMethods = kwargs.get('urlMaintStatInvalidMethods', None)
        self.urlMaintStatAgedSessions = kwargs.get('urlMaintStatAgedSessions', None)
        self.urlMaintStatLowestSPMemUnits = kwargs.get('urlMaintStatLowestSPMemUnits', None)
        self.currOpenedServerConns = kwargs.get('currOpenedServerConns', None)
        self.activeServerConns = kwargs.get('activeServerConns', None)
        self.availServerConns = kwargs.get('availServerConns', None)
        self.agedOutClientConns = kwargs.get('agedOutClientConns', None)
        self.agedOutServerConns = kwargs.get('agedOutServerConns', None)
        self.slbParsingString = kwargs.get('slbParsingString', None)
        self.slbParsingVip = kwargs.get('slbParsingVip', None)
        self.slbParsingRip = kwargs.get('slbParsingRip', None)
        self.slbParsingRport = kwargs.get('slbParsingRport', None)
        self.slbParsingCip = kwargs.get('slbParsingCip', None)
        self.ipInterfaceTableMax = kwargs.get('ipInterfaceTableMax', None)
        self.ipNewLanIfId = kwargs.get('ipNewLanIfId', None)
        self.ipNewCfgGwMetric = EnumIpNewCfgGwMetric.enum(kwargs.get('ipNewCfgGwMetric', None))
        self.ipGatewayTableMax = kwargs.get('ipGatewayTableMax', None)
        self.ipStaticRouteTableMaxSize = kwargs.get('ipStaticRouteTableMaxSize', None)
        self.rip2NewCfgState = EnumRip2NewCfgState.enum(kwargs.get('rip2NewCfgState', None))
        self.rip2NewCfgUpdatePeriod = kwargs.get('rip2NewCfgUpdatePeriod', None)
        self.rip2NewCfgVip = EnumRip2NewCfgVip.enum(kwargs.get('rip2NewCfgVip', None))
        self.rip2NewCfgStaticSupply = EnumRip2NewCfgStaticSupply.enum(kwargs.get('rip2NewCfgStaticSupply', None))
        self.ipFwdNewCfgState = EnumIpFwdNewCfgState.enum(kwargs.get('ipFwdNewCfgState', None))
        self.ipFwdNewCfgDirectedBcast = EnumIpFwdNewCfgDirectedBcast.enum(kwargs.get('ipFwdNewCfgDirectedBcast', None))
        self.ipFwdNewCfgNoICMPRedirect = EnumIpFwdNewCfgNoICMPRedirect.enum(kwargs.get('ipFwdNewCfgNoICMPRedirect', None))
        self.ipFwdNewCfgRtCache = EnumIpFwdNewCfgRtCache.enum(kwargs.get('ipFwdNewCfgRtCache', None))
        self.ipFwdPortTableMaxSize = kwargs.get('ipFwdPortTableMaxSize', None)
        self.ipFwdLocalTableMaxSize = kwargs.get('ipFwdLocalTableMaxSize', None)
        self.arpNewCfgReARPPeriod = kwargs.get('arpNewCfgReARPPeriod', None)
        self.ipNewCfgBootpAddr = kwargs.get('ipNewCfgBootpAddr', None)
        self.ipNewCfgBootpAddr2 = kwargs.get('ipNewCfgBootpAddr2', None)
        self.ipNewCfgBootpState = EnumIpNewCfgBootpState.enum(kwargs.get('ipNewCfgBootpState', None))
        self.ipNewCfgBootpPrsvPort = EnumIpNewCfgBootpPrsvPort.enum(kwargs.get('ipNewCfgBootpPrsvPort', None))
        self.vrrpNewCfgGenState = EnumVrrpNewCfgGenState.enum(kwargs.get('vrrpNewCfgGenState', None))
        self.vrrpNewCfgGenTckVirtRtrInc = kwargs.get('vrrpNewCfgGenTckVirtRtrInc', None)
        self.vrrpNewCfgGenTckIpIntfInc = kwargs.get('vrrpNewCfgGenTckIpIntfInc', None)
        self.vrrpNewCfgGenTckVlanPortInc = kwargs.get('vrrpNewCfgGenTckVlanPortInc', None)
        self.vrrpNewCfgGenTckL4PortInc = kwargs.get('vrrpNewCfgGenTckL4PortInc', None)
        self.vrrpNewCfgGenTckRServerInc = kwargs.get('vrrpNewCfgGenTckRServerInc', None)
        self.vrrpNewCfgGenTckHsrpInc = kwargs.get('vrrpNewCfgGenTckHsrpInc', None)
        self.vrrpNewCfgGenHotstandby = EnumVrrpNewCfgGenHotstandby.enum(kwargs.get('vrrpNewCfgGenHotstandby', None))
        self.vrrpNewCfgGenTckHsrvInc = kwargs.get('vrrpNewCfgGenTckHsrvInc', None)
        self.vrrpNewCfgGenHoldoff = kwargs.get('vrrpNewCfgGenHoldoff', None)
        self.vrrpNewCfgGenOspfCost = kwargs.get('vrrpNewCfgGenOspfCost', None)
        self.vrrpNewCfgGenTckSwExtInc = kwargs.get('vrrpNewCfgGenTckSwExtInc', None)
        self.vrrpNewCfgGenUnicast = EnumVrrpNewCfgGenUnicast.enum(kwargs.get('vrrpNewCfgGenUnicast', None))
        self.vrrpNewCfgGenFovdelay = EnumVrrpNewCfgGenFovdelay.enum(kwargs.get('vrrpNewCfgGenFovdelay', None))
        self.vrrpVirtRtrTableMaxSize = kwargs.get('vrrpVirtRtrTableMaxSize', None)
        self.vrrpIfTableMaxSize = kwargs.get('vrrpIfTableMaxSize', None)
        self.vrrpVirtRtrGrpTableMaxSize = kwargs.get('vrrpVirtRtrGrpTableMaxSize', None)
        self.vrrpVirtRtrVrGrpTableMaxSize = kwargs.get('vrrpVirtRtrVrGrpTableMaxSize', None)
        self.dnsNewCfgPrimaryIpAddr = kwargs.get('dnsNewCfgPrimaryIpAddr', None)
        self.dnsNewCfgSecondaryIpAddr = kwargs.get('dnsNewCfgSecondaryIpAddr', None)
        self.dnsNewCfgDomainName = kwargs.get('dnsNewCfgDomainName', None)
        self.dnsNewCfgPrimaryIpv6Addr = kwargs.get('dnsNewCfgPrimaryIpv6Addr', None)
        self.dnsNewCfgSecondaryIpv6Addr = kwargs.get('dnsNewCfgSecondaryIpv6Addr', None)
        self.ipNwfTableMax = kwargs.get('ipNwfTableMax', None)
        self.ipRmapTableMax = kwargs.get('ipRmapTableMax', None)
        self.ipAlistTableMax = kwargs.get('ipAlistTableMax', None)
        self.ipAspathTableMax = kwargs.get('ipAspathTableMax', None)
        self.bgpNewCfgState = EnumBgpNewCfgState.enum(kwargs.get('bgpNewCfgState', None))
        self.bgpNewCfgLocalPref = kwargs.get('bgpNewCfgLocalPref', None)
        self.bgpNewCfgMaxASPath = kwargs.get('bgpNewCfgMaxASPath', None)
        self.bgpNewCfgASNumber = kwargs.get('bgpNewCfgASNumber', None)
        self.bgpNewCfgStopVipAdv = EnumBgpNewCfgStopVipAdv.enum(kwargs.get('bgpNewCfgStopVipAdv', None))
        self.bgpNewCfgAdvFip = EnumBgpNewCfgAdvFip.enum(kwargs.get('bgpNewCfgAdvFip', None))
        self.bgpNewCfgMode = EnumBgpNewCfgMode.enum(kwargs.get('bgpNewCfgMode', None))
        self.bgpNewCfgEcmp = EnumBgpNewCfgEcmp.enum(kwargs.get('bgpNewCfgEcmp', None))
        self.bgpPeerTableMax = kwargs.get('bgpPeerTableMax', None)
        self.bgpAggrTableMax = kwargs.get('bgpAggrTableMax', None)
        self.ospfNewCfgDefaultRouteMetric = kwargs.get('ospfNewCfgDefaultRouteMetric', None)
        self.ospfNewCfgDefaultRouteMetricType = EnumOspfNewCfgDefaultRouteMetricType.enum(kwargs.get('ospfNewCfgDefaultRouteMetricType', None))
        self.ospfIntfTableMaxSize = kwargs.get('ospfIntfTableMaxSize', None)
        self.ospfAreaTableMaxSize = kwargs.get('ospfAreaTableMaxSize', None)
        self.ospfRangeTableMaxSize = kwargs.get('ospfRangeTableMaxSize', None)
        self.ospfVirtIntfTableMaxSize = kwargs.get('ospfVirtIntfTableMaxSize', None)
        self.ospfHostTableMaxSize = kwargs.get('ospfHostTableMaxSize', None)
        self.ospfNewCfgState = EnumOspfNewCfgState.enum(kwargs.get('ospfNewCfgState', None))
        self.ospfNewCfgLsdb = kwargs.get('ospfNewCfgLsdb', None)
        self.ospfMdkeyTableMaxSize = kwargs.get('ospfMdkeyTableMaxSize', None)
        self.ospfNewCfgStaticMetric = kwargs.get('ospfNewCfgStaticMetric', None)
        self.ospfNewCfgStaticMetricType = EnumOspfNewCfgStaticMetricType.enum(kwargs.get('ospfNewCfgStaticMetricType', None))
        self.ospfNewCfgStaticOutRmapList = kwargs.get('ospfNewCfgStaticOutRmapList', None)
        self.ospfNewCfgStaticAddOutRmap = kwargs.get('ospfNewCfgStaticAddOutRmap', None)
        self.ospfNewCfgStaticRemoveOutRmap = kwargs.get('ospfNewCfgStaticRemoveOutRmap', None)
        self.ospfNewCfgEbgpMetric = kwargs.get('ospfNewCfgEbgpMetric', None)
        self.ospfNewCfgEbgpMetricType = EnumOspfNewCfgEbgpMetricType.enum(kwargs.get('ospfNewCfgEbgpMetricType', None))
        self.ospfNewCfgEbgpOutRmapList = kwargs.get('ospfNewCfgEbgpOutRmapList', None)
        self.ospfNewCfgEbgpAddOutRmap = kwargs.get('ospfNewCfgEbgpAddOutRmap', None)
        self.ospfNewCfgEbgpRemoveOutRmap = kwargs.get('ospfNewCfgEbgpRemoveOutRmap', None)
        self.ospfNewCfgIbgpMetric = kwargs.get('ospfNewCfgIbgpMetric', None)
        self.ospfNewCfgIbgpMetricType = EnumOspfNewCfgIbgpMetricType.enum(kwargs.get('ospfNewCfgIbgpMetricType', None))
        self.ospfNewCfgIbgpOutRmapList = kwargs.get('ospfNewCfgIbgpOutRmapList', None)
        self.ospfNewCfgIbgpAddOutRmap = kwargs.get('ospfNewCfgIbgpAddOutRmap', None)
        self.ospfNewCfgIbgpRemoveOutRmap = kwargs.get('ospfNewCfgIbgpRemoveOutRmap', None)
        self.ospfNewCfgFixedMetric = kwargs.get('ospfNewCfgFixedMetric', None)
        self.ospfNewCfgFixedMetricType = EnumOspfNewCfgFixedMetricType.enum(kwargs.get('ospfNewCfgFixedMetricType', None))
        self.ospfNewCfgFixedOutRmapList = kwargs.get('ospfNewCfgFixedOutRmapList', None)
        self.ospfNewCfgFixedAddOutRmap = kwargs.get('ospfNewCfgFixedAddOutRmap', None)
        self.ospfNewCfgFixedRemoveOutRmap = kwargs.get('ospfNewCfgFixedRemoveOutRmap', None)
        self.ospfNewCfgRipMetric = kwargs.get('ospfNewCfgRipMetric', None)
        self.ospfNewCfgRipMetricType = EnumOspfNewCfgRipMetricType.enum(kwargs.get('ospfNewCfgRipMetricType', None))
        self.ospfNewCfgRipOutRmapList = kwargs.get('ospfNewCfgRipOutRmapList', None)
        self.ospfNewCfgRipAddOutRmap = kwargs.get('ospfNewCfgRipAddOutRmap', None)
        self.ospfNewCfgRipRemoveOutRmap = kwargs.get('ospfNewCfgRipRemoveOutRmap', None)
        self.ospfv3NewCfgDefaultRouteMetric = kwargs.get('ospfv3NewCfgDefaultRouteMetric', None)
        self.ospfv3NewCfgDefaultRouteMetricType = EnumOspfv3NewCfgDefaultRouteMetricType.enum(kwargs.get('ospfv3NewCfgDefaultRouteMetricType', None))
        self.ospfv3IntfTableMaxSize = kwargs.get('ospfv3IntfTableMaxSize', None)
        self.ospfv3AreaTableMaxSize = kwargs.get('ospfv3AreaTableMaxSize', None)
        self.ospfv3RangeTableMaxSize = kwargs.get('ospfv3RangeTableMaxSize', None)
        self.ospfv3VirtIntfTableMaxSize = kwargs.get('ospfv3VirtIntfTableMaxSize', None)
        self.ospfv3HostTableMaxSize = kwargs.get('ospfv3HostTableMaxSize', None)
        self.ospfv3NewCfgState = EnumOspfv3NewCfgState.enum(kwargs.get('ospfv3NewCfgState', None))
        self.ospfv3NewCfgLsdb = kwargs.get('ospfv3NewCfgLsdb', None)
        self.ospfv3NewCfgStaticMetric = kwargs.get('ospfv3NewCfgStaticMetric', None)
        self.ospfv3NewCfgStaticMetricType = EnumOspfv3NewCfgStaticMetricType.enum(kwargs.get('ospfv3NewCfgStaticMetricType', None))
        self.ospfv3NewCfgStaticOutRmapList = kwargs.get('ospfv3NewCfgStaticOutRmapList', None)
        self.ospfv3NewCfgStaticAddOutRmap = kwargs.get('ospfv3NewCfgStaticAddOutRmap', None)
        self.ospfv3NewCfgStaticRemoveOutRmap = kwargs.get('ospfv3NewCfgStaticRemoveOutRmap', None)
        self.ospfv3NewCfgEbgpMetric = kwargs.get('ospfv3NewCfgEbgpMetric', None)
        self.ospfv3NewCfgEbgpMetricType = EnumOspfv3NewCfgEbgpMetricType.enum(kwargs.get('ospfv3NewCfgEbgpMetricType', None))
        self.ospfv3NewCfgEbgpOutRmapList = kwargs.get('ospfv3NewCfgEbgpOutRmapList', None)
        self.ospfv3NewCfgEbgpAddOutRmap = kwargs.get('ospfv3NewCfgEbgpAddOutRmap', None)
        self.ospfv3NewCfgEbgpRemoveOutRmap = kwargs.get('ospfv3NewCfgEbgpRemoveOutRmap', None)
        self.ospfv3NewCfgIbgpMetric = kwargs.get('ospfv3NewCfgIbgpMetric', None)
        self.ospfv3NewCfgIbgpMetricType = EnumOspfv3NewCfgIbgpMetricType.enum(kwargs.get('ospfv3NewCfgIbgpMetricType', None))
        self.ospfv3NewCfgIbgpOutRmapList = kwargs.get('ospfv3NewCfgIbgpOutRmapList', None)
        self.ospfv3NewCfgIbgpAddOutRmap = kwargs.get('ospfv3NewCfgIbgpAddOutRmap', None)
        self.ospfv3NewCfgIbgpRemoveOutRmap = kwargs.get('ospfv3NewCfgIbgpRemoveOutRmap', None)
        self.ospfv3NewCfgFixedMetric = kwargs.get('ospfv3NewCfgFixedMetric', None)
        self.ospfv3NewCfgFixedMetricType = EnumOspfv3NewCfgFixedMetricType.enum(kwargs.get('ospfv3NewCfgFixedMetricType', None))
        self.ospfv3NewCfgFixedOutRmapList = kwargs.get('ospfv3NewCfgFixedOutRmapList', None)
        self.ospfv3NewCfgFixedAddOutRmap = kwargs.get('ospfv3NewCfgFixedAddOutRmap', None)
        self.ospfv3NewCfgFixedRemoveOutRmap = kwargs.get('ospfv3NewCfgFixedRemoveOutRmap', None)
        self.ospfv3NewCfgRipMetric = kwargs.get('ospfv3NewCfgRipMetric', None)
        self.ospfv3NewCfgRipMetricType = EnumOspfv3NewCfgRipMetricType.enum(kwargs.get('ospfv3NewCfgRipMetricType', None))
        self.ospfv3NewCfgRipOutRmapList = kwargs.get('ospfv3NewCfgRipOutRmapList', None)
        self.ospfv3NewCfgRipAddOutRmap = kwargs.get('ospfv3NewCfgRipAddOutRmap', None)
        self.ospfv3NewCfgRipRemoveOutRmap = kwargs.get('ospfv3NewCfgRipRemoveOutRmap', None)
        self.ipNewCfgRouterID = kwargs.get('ipNewCfgRouterID', None)
        self.ipNewCfgASNumber = kwargs.get('ipNewCfgASNumber', None)
        self.ipNewCfgFragTblSize = kwargs.get('ipNewCfgFragTblSize', None)
        self.ipStaticArpTableMaxSize = kwargs.get('ipStaticArpTableMaxSize', None)
        self.ipStaticArpTableNextAvailableIndex = kwargs.get('ipStaticArpTableNextAvailableIndex', None)
        self.ipv6StaticNbrTableMaxSize = kwargs.get('ipv6StaticNbrTableMaxSize', None)
        self.ipv6StaticNbrTableNextAvailableIndex = kwargs.get('ipv6StaticNbrTableNextAvailableIndex', None)
        self.ripStatInPackets = kwargs.get('ripStatInPackets', None)
        self.ripStatOutPackets = kwargs.get('ripStatOutPackets', None)
        self.ripStatInRequestPkts = kwargs.get('ripStatInRequestPkts', None)
        self.ripStatInResponsePkts = kwargs.get('ripStatInResponsePkts', None)
        self.ripStatOutRequestPkts = kwargs.get('ripStatOutRequestPkts', None)
        self.ripStatOutResponsePkts = kwargs.get('ripStatOutResponsePkts', None)
        self.ripStatRouteTimeout = kwargs.get('ripStatRouteTimeout', None)
        self.ripStatInBadSizePkts = kwargs.get('ripStatInBadSizePkts', None)
        self.ripStatInBadVersion = kwargs.get('ripStatInBadVersion', None)
        self.ripStatInBadZeros = kwargs.get('ripStatInBadZeros', None)
        self.ripStatInBadSourcePort = kwargs.get('ripStatInBadSourcePort', None)
        self.ripStatInBadSourceIP = kwargs.get('ripStatInBadSourceIP', None)
        self.ripStatInSelfRcvPkts = kwargs.get('ripStatInSelfRcvPkts', None)
        self.tcpStatCurConn = kwargs.get('tcpStatCurConn', None)
        self.tcpStatCurInConn = kwargs.get('tcpStatCurInConn', None)
        self.tcpStatCurOutConn = kwargs.get('tcpStatCurOutConn', None)
        self.arpStatEntries = kwargs.get('arpStatEntries', None)
        self.arpStatHighWater = kwargs.get('arpStatHighWater', None)
        self.arpStatMaxEntries = kwargs.get('arpStatMaxEntries', None)
        self.routeStatEntries = kwargs.get('routeStatEntries', None)
        self.routeStatHighWater = kwargs.get('routeStatHighWater', None)
        self.routeStatMaxEntries = kwargs.get('routeStatMaxEntries', None)
        self.dnsStatInGoodDnsRequests = kwargs.get('dnsStatInGoodDnsRequests', None)
        self.dnsStatInBadDnsRequests = kwargs.get('dnsStatInBadDnsRequests', None)
        self.dnsStatOutDnsRequests = kwargs.get('dnsStatOutDnsRequests', None)
        self.vrrpStatInAdvers = kwargs.get('vrrpStatInAdvers', None)
        self.vrrpStatOutAdvers = kwargs.get('vrrpStatOutAdvers', None)
        self.vrrpStatOutBadAdvers = kwargs.get('vrrpStatOutBadAdvers', None)
        self.vrrpStatBadPassword = kwargs.get('vrrpStatBadPassword', None)
        self.vrrpStatBadVersion = kwargs.get('vrrpStatBadVersion', None)
        self.vrrpStatBadVrid = kwargs.get('vrrpStatBadVrid', None)
        self.vrrpStatBadAddress = kwargs.get('vrrpStatBadAddress', None)
        self.vrrpStatBadData = kwargs.get('vrrpStatBadData', None)
        self.vrrpStatBadInterval = kwargs.get('vrrpStatBadInterval', None)
        self.vrrpStatBadHaid = kwargs.get('vrrpStatBadHaid', None)
        self.ipClearStats = EnumIpClearStats.enum(kwargs.get('ipClearStats', None))
        self.urlfClearStats = EnumUrlfClearStats.enum(kwargs.get('urlfClearStats', None))
        self.ospfCumRxPkts = kwargs.get('ospfCumRxPkts', None)
        self.ospfCumTxPkts = kwargs.get('ospfCumTxPkts', None)
        self.ospfCumRxHello = kwargs.get('ospfCumRxHello', None)
        self.ospfCumTxHello = kwargs.get('ospfCumTxHello', None)
        self.ospfCumRxDatabase = kwargs.get('ospfCumRxDatabase', None)
        self.ospfCumTxDatabase = kwargs.get('ospfCumTxDatabase', None)
        self.ospfCumRxlsReqs = kwargs.get('ospfCumRxlsReqs', None)
        self.ospfCumTxlsReqs = kwargs.get('ospfCumTxlsReqs', None)
        self.ospfCumRxlsAcks = kwargs.get('ospfCumRxlsAcks', None)
        self.ospfCumTxlsAcks = kwargs.get('ospfCumTxlsAcks', None)
        self.ospfCumRxlsUpdates = kwargs.get('ospfCumRxlsUpdates', None)
        self.ospfCumTxlsUpdates = kwargs.get('ospfCumTxlsUpdates', None)
        self.ospfCumNbrhello = kwargs.get('ospfCumNbrhello', None)
        self.ospfCumNbrStart = kwargs.get('ospfCumNbrStart', None)
        self.ospfCumNbrAdjointOk = kwargs.get('ospfCumNbrAdjointOk', None)
        self.ospfCumNbrNegotiationDone = kwargs.get('ospfCumNbrNegotiationDone', None)
        self.ospfCumNbrExchangeDone = kwargs.get('ospfCumNbrExchangeDone', None)
        self.ospfCumNbrBadRequests = kwargs.get('ospfCumNbrBadRequests', None)
        self.ospfCumNbrBadSequence = kwargs.get('ospfCumNbrBadSequence', None)
        self.ospfCumNbrLoadingDone = kwargs.get('ospfCumNbrLoadingDone', None)
        self.ospfCumNbrN1way = kwargs.get('ospfCumNbrN1way', None)
        self.ospfCumNbrRstAd = kwargs.get('ospfCumNbrRstAd', None)
        self.ospfCumNbrDown = kwargs.get('ospfCumNbrDown', None)
        self.ospfCumNbrN2way = kwargs.get('ospfCumNbrN2way', None)
        self.ospfCumIntfHello = kwargs.get('ospfCumIntfHello', None)
        self.ospfCumIntfDown = kwargs.get('ospfCumIntfDown', None)
        self.ospfCumIntfLoop = kwargs.get('ospfCumIntfLoop', None)
        self.ospfCumIntfUnloop = kwargs.get('ospfCumIntfUnloop', None)
        self.ospfCumIntfWaitTimer = kwargs.get('ospfCumIntfWaitTimer', None)
        self.ospfCumIntfBackup = kwargs.get('ospfCumIntfBackup', None)
        self.ospfCumIntfNbrChange = kwargs.get('ospfCumIntfNbrChange', None)
        self.ospfTmrsKckOffHello = kwargs.get('ospfTmrsKckOffHello', None)
        self.ospfTmrsKckOffRetransmit = kwargs.get('ospfTmrsKckOffRetransmit', None)
        self.ospfTmrsKckOffLsaLock = kwargs.get('ospfTmrsKckOffLsaLock', None)
        self.ospfTmrsKckOffLsaAck = kwargs.get('ospfTmrsKckOffLsaAck', None)
        self.ospfTmrsKckOffDbage = kwargs.get('ospfTmrsKckOffDbage', None)
        self.ospfTmrsKckOffSummary = kwargs.get('ospfTmrsKckOffSummary', None)
        self.ospfTmrsKckOffAseExport = kwargs.get('ospfTmrsKckOffAseExport', None)
        self.ospfv3StatsPackSent = kwargs.get('ospfv3StatsPackSent', None)
        self.ospfv3PacketRx = kwargs.get('ospfv3PacketRx', None)
        self.ospfv3RxPacketDrop = kwargs.get('ospfv3RxPacketDrop', None)
        self.ospfv3TxPacketDrop = kwargs.get('ospfv3TxPacketDrop', None)
        self.ospfv3RxBadPacket = kwargs.get('ospfv3RxBadPacket', None)
        self.ospfv3SpfRunCount = kwargs.get('ospfv3SpfRunCount', None)
        self.ospfv3LastSpfRun = kwargs.get('ospfv3LastSpfRun', None)
        self.ospfv3LSDBtableSize = kwargs.get('ospfv3LSDBtableSize', None)
        self.ospfv3BadLSReqCnt = kwargs.get('ospfv3BadLSReqCnt', None)
        self.ospfv3SeqMismatchCnt = kwargs.get('ospfv3SeqMismatchCnt', None)
        self.vrrp6StatInAdvers = kwargs.get('vrrp6StatInAdvers', None)
        self.vrrp6StatOutAdvers = kwargs.get('vrrp6StatOutAdvers', None)
        self.vrrp6StatOutBadAdvers = kwargs.get('vrrp6StatOutBadAdvers', None)
        self.vrrp6StatBadVersion = kwargs.get('vrrp6StatBadVersion', None)
        self.vrrp6StatBadVrid = kwargs.get('vrrp6StatBadVrid', None)
        self.vrrp6StatBadAddress = kwargs.get('vrrp6StatBadAddress', None)
        self.vrrp6StatBadData = kwargs.get('vrrp6StatBadData', None)
        self.vrrp6StatBadInterval = kwargs.get('vrrp6StatBadInterval', None)
        self.vrrp6StatBadHaid = kwargs.get('vrrp6StatBadHaid', None)
        self.ip6InReceives = kwargs.get('ip6InReceives', None)
        self.ip6ForwDatagrams = kwargs.get('ip6ForwDatagrams', None)
        self.ip6InDelivers = kwargs.get('ip6InDelivers', None)
        self.ip6InDiscards = kwargs.get('ip6InDiscards', None)
        self.ip6InUnknownProtos = kwargs.get('ip6InUnknownProtos', None)
        self.ip6InAddrErrors = kwargs.get('ip6InAddrErrors', None)
        self.ip6OutRequests = kwargs.get('ip6OutRequests', None)
        self.ip6OutNoRoutes = kwargs.get('ip6OutNoRoutes', None)
        self.ip6ReasmOKs = kwargs.get('ip6ReasmOKs', None)
        self.ip6ReasmFails = kwargs.get('ip6ReasmFails', None)
        self.ip6icmpInMsgs = kwargs.get('ip6icmpInMsgs', None)
        self.ip6icmpOutMsgs = kwargs.get('ip6icmpOutMsgs', None)
        self.ip6icmpInErrors = kwargs.get('ip6icmpInErrors', None)
        self.ip6icmpOutErrors = kwargs.get('ip6icmpOutErrors', None)
        self.routeTableClear = EnumRouteTableClear.enum(kwargs.get('routeTableClear', None))
        self.arpCacheClear = EnumArpCacheClear.enum(kwargs.get('arpCacheClear', None))
        self.vrrpInfoHAState = kwargs.get('vrrpInfoHAState', None)
        self.ospfStartTime = kwargs.get('ospfStartTime', None)
        self.ospfProcessUptime = kwargs.get('ospfProcessUptime', None)
        self.ospfLsTypesSupported = kwargs.get('ospfLsTypesSupported', None)
        self.ospfIntfCountForRouter = kwargs.get('ospfIntfCountForRouter', None)
        self.ospfVlinkCountForRouter = kwargs.get('ospfVlinkCountForRouter', None)
        self.ospfTotalNeighbours = kwargs.get('ospfTotalNeighbours', None)
        self.ospfNbrInInitState = kwargs.get('ospfNbrInInitState', None)
        self.ospfNbrInExchState = kwargs.get('ospfNbrInExchState', None)
        self.ospfNbrInFullState = kwargs.get('ospfNbrInFullState', None)
        self.ospfTotalAreas = kwargs.get('ospfTotalAreas', None)
        self.ospfTotalTransitAreas = kwargs.get('ospfTotalTransitAreas', None)
        self.ospfTotalNssaAreas = kwargs.get('ospfTotalNssaAreas', None)
        self.nbrcacheClear = EnumNbrcacheClear.enum(kwargs.get('nbrcacheClear', None))
        self.nbrcacheInfoTotDynamicEntries = kwargs.get('nbrcacheInfoTotDynamicEntries', None)
        self.nbrcacheInfoTotLocalEntries = kwargs.get('nbrcacheInfoTotLocalEntries', None)
        self.nbrcacheInfoTotOtherEntries = kwargs.get('nbrcacheInfoTotOtherEntries', None)
        self.nbrcacheInfoTotStaticEntries = kwargs.get('nbrcacheInfoTotStaticEntries', None)
        self.ripInfoState = EnumRipInfoState.enum(kwargs.get('ripInfoState', None))
        self.ripInfoUpdatePeriod = kwargs.get('ripInfoUpdatePeriod', None)
        self.ripInfoVip = EnumRipInfoVip.enum(kwargs.get('ripInfoVip', None))
        self.ripInfoStaticSupply = EnumRipInfoStaticSupply.enum(kwargs.get('ripInfoStaticSupply', None))
        self.ospfv3RouterID = kwargs.get('ospfv3RouterID', None)
        self.ospfv3AdminState = EnumOspfv3AdminState.enum(kwargs.get('ospfv3AdminState', None))
        self.ospfv3ASBRstatus = EnumOspfv3ASBRstatus.enum(kwargs.get('ospfv3ASBRstatus', None))
        self.ospfv3ABRStatus = EnumOspfv3ABRStatus.enum(kwargs.get('ospfv3ABRStatus', None))
        self.ospfv3ASscopeLSAcnt = kwargs.get('ospfv3ASscopeLSAcnt', None)
        self.ospfv3RcvLSAcnt = kwargs.get('ospfv3RcvLSAcnt', None)
        self.ospfv3NewLSAcnt = kwargs.get('ospfv3NewLSAcnt', None)
        self.ospfv3MulticstExt = kwargs.get('ospfv3MulticstExt', None)
        self.haSwitchInfoState = kwargs.get('haSwitchInfoState', None)
        self.haNewCfgMode = EnumHaNewCfgMode.enum(kwargs.get('haNewCfgMode', None))
        self.haNewCfgHoldoffTime = kwargs.get('haNewCfgHoldoffTime', None)
        self.haSwitchNewCfgPref = EnumHaSwitchNewCfgPref.enum(kwargs.get('haSwitchNewCfgPref', None))
        self.haSwitchNewCfgFailBackMode = EnumHaSwitchNewCfgFailBackMode.enum(kwargs.get('haSwitchNewCfgFailBackMode', None))
        self.haSwitchNewCfgAdvIfsMapList = kwargs.get('haSwitchNewCfgAdvIfsMapList', None)
        self.haSwitchNewCfgAddIf = kwargs.get('haSwitchNewCfgAddIf', None)
        self.haSwitchNewCfgRemIf = kwargs.get('haSwitchNewCfgRemIf', None)
        self.haSwitchNewCfgAdver = kwargs.get('haSwitchNewCfgAdver', None)
        self.haSwitchNewCfgOrder = kwargs.get('haSwitchNewCfgOrder', None)
        self.haSwitchNewCfgTriggerl4Reals = EnumHaSwitchNewCfgTriggerl4Reals.enum(kwargs.get('haSwitchNewCfgTriggerl4Reals', None))
        self.haSwitchNewCfgTrigIfTrackAdd = kwargs.get('haSwitchNewCfgTrigIfTrackAdd', None)
        self.haSwitchNewCfgTrigIfTrackExclude = kwargs.get('haSwitchNewCfgTrigIfTrackExclude', None)
        self.haSwitchNewCfgTrackIfsMapList = kwargs.get('haSwitchNewCfgTrackIfsMapList', None)
        self.haSwitchNewCfgTrigGwTrackState = EnumHaSwitchNewCfgTrigGwTrackState.enum(kwargs.get('haSwitchNewCfgTrigGwTrackState', None))
        self.haSwitchNewCfgTrigGwTrackAdd = kwargs.get('haSwitchNewCfgTrigGwTrackAdd', None)
        self.haSwitchNewCfgTrigGwTrackExclude = kwargs.get('haSwitchNewCfgTrigGwTrackExclude', None)
        self.haSwitchNewCfgTrackGwsMapList = kwargs.get('haSwitchNewCfgTrackGwsMapList', None)
        self.haSwitchNewCfgTriggerNewl4Reals = EnumHaSwitchNewCfgTriggerNewl4Reals.enum(kwargs.get('haSwitchNewCfgTriggerNewl4Reals', None))
        self.haSwitchNewCfgTriggerAllReml4Reals = EnumHaSwitchNewCfgTriggerAllReml4Reals.enum(kwargs.get('haSwitchNewCfgTriggerAllReml4Reals', None))
        self.haSwitchNewCfgTriggerListl4Reals = kwargs.get('haSwitchNewCfgTriggerListl4Reals', None)
        self.haSwitchNewCfgTriggerAddl4Reals = kwargs.get('haSwitchNewCfgTriggerAddl4Reals', None)
        self.haSwitchNewCfgTriggerRemovel4Reals = kwargs.get('haSwitchNewCfgTriggerRemovel4Reals', None)
        self.haTrunkTableMaxSize = kwargs.get('haTrunkTableMaxSize', None)
        self.haLacpTableMaxSize = kwargs.get('haLacpTableMaxSize', None)
        self.haLacpMaxAdminKey = kwargs.get('haLacpMaxAdminKey', None)
        self.haNewLPWizardCfgMode = EnumHaNewLPWizardCfgMode.enum(kwargs.get('haNewLPWizardCfgMode', None))
        self.haNewCfgHAID = kwargs.get('haNewCfgHAID', None)
        self.haNewCfgBkpVipRt = EnumHaNewCfgBkpVipRt.enum(kwargs.get('haNewCfgBkpVipRt', None))
        self.haNewCfgNwClGarp = EnumHaNewCfgNwClGarp.enum(kwargs.get('haNewCfgNwClGarp', None))
        self.bfdNewCfgState = EnumBfdNewCfgState.enum(kwargs.get('bfdNewCfgState', None))
        self.bfdNewCfgRxInterval = kwargs.get('bfdNewCfgRxInterval', None)
        self.bfdNewCfgMultiplier = kwargs.get('bfdNewCfgMultiplier', None)
        self.bfdNewCfgIfBmap = kwargs.get('bfdNewCfgIfBmap', None)
        self.bfdNewCfgAddIf = kwargs.get('bfdNewCfgAddIf', None)
        self.bfdNewCfgRemIf = kwargs.get('bfdNewCfgRemIf', None)
        self.vrrpOperVirtRtrGroupBackup = EnumVrrpOperVirtRtrGroupBackup.enum(kwargs.get('vrrpOperVirtRtrGroupBackup', None))
        self.bgpOperStartPeerNum = kwargs.get('bgpOperStartPeerNum', None)
        self.bgpOperStartSess = EnumBgpOperStartSess.enum(kwargs.get('bgpOperStartSess', None))
        self.bgpOperStopPeerNum = kwargs.get('bgpOperStopPeerNum', None)
        self.bgpOperStopSess = EnumBgpOperStopSess.enum(kwargs.get('bgpOperStopSess', None))
        self.garpOperIpAddr = kwargs.get('garpOperIpAddr', None)
        self.garpOperVlanNumber = kwargs.get('garpOperVlanNumber', None)
        self.garpOperSend = EnumGarpOperSend.enum(kwargs.get('garpOperSend', None))
        self.haOperSwitchBackup = EnumHaOperSwitchBackup.enum(kwargs.get('haOperSwitchBackup', None))
        self.hwTemperatureStatus = EnumHwTemperatureStatus.enum(kwargs.get('hwTemperatureStatus', None))
        self.hwFanStatus = EnumHwFanStatus.enum(kwargs.get('hwFanStatus', None))
        self.switchCapFDBMaxEnt = kwargs.get('switchCapFDBMaxEnt', None)
        self.switchCapFDBCurrEnt = kwargs.get('switchCapFDBCurrEnt', None)
        self.switchCapFDBPerSPMaxEnt = kwargs.get('switchCapFDBPerSPMaxEnt', None)
        self.switchCapVlanMaxEnt = kwargs.get('switchCapVlanMaxEnt', None)
        self.switchCapVlanCurrEnt = kwargs.get('switchCapVlanCurrEnt', None)
        self.switchCapStaticTrunkGrpsMaxEnt = kwargs.get('switchCapStaticTrunkGrpsMaxEnt', None)
        self.switchCapStaticTrunkGrpsCurrEnt = kwargs.get('switchCapStaticTrunkGrpsCurrEnt', None)
        self.switchCapLACPTrunkGRs = kwargs.get('switchCapLACPTrunkGRs', None)
        self.switchCapTrunksperTrunkGR = kwargs.get('switchCapTrunksperTrunkGR', None)
        self.switchCapSTGsMaxEnt = kwargs.get('switchCapSTGsMaxEnt', None)
        self.switchCapSTGsCurrEnt = kwargs.get('switchCapSTGsCurrEnt', None)
        self.switchCapPortTeamsMaxEnt = kwargs.get('switchCapPortTeamsMaxEnt', None)
        self.switchCapPortTeamsCurrEnt = kwargs.get('switchCapPortTeamsCurrEnt', None)
        self.switchCapMonitorPorts = kwargs.get('switchCapMonitorPorts', None)
        self.switchCapIpIntfMaxEnt = kwargs.get('switchCapIpIntfMaxEnt', None)
        self.switchCapIpIntfCurrEnt = kwargs.get('switchCapIpIntfCurrEnt', None)
        self.switchCapIpGWMaxEnt = kwargs.get('switchCapIpGWMaxEnt', None)
        self.switchCapIpGWCurrEnt = kwargs.get('switchCapIpGWCurrEnt', None)
        self.switchCapIpRoutesMaxEnt = kwargs.get('switchCapIpRoutesMaxEnt', None)
        self.switchCapIpRoutesCurrEnt = kwargs.get('switchCapIpRoutesCurrEnt', None)
        self.switchCapIpStaticRoutesMaxEnt = kwargs.get('switchCapIpStaticRoutesMaxEnt', None)
        self.switchCapIpStaticRoutesCurrEnt = kwargs.get('switchCapIpStaticRoutesCurrEnt', None)
        self.switchCapIpARPMaxEnt = kwargs.get('switchCapIpARPMaxEnt', None)
        self.switchCapIpARPCurrEnt = kwargs.get('switchCapIpARPCurrEnt', None)
        self.switchCapIpStaticARPMaxEnt = kwargs.get('switchCapIpStaticARPMaxEnt', None)
        self.switchCapIpStaticARPCurrEnt = kwargs.get('switchCapIpStaticARPCurrEnt', None)
        self.switchCapLocNetsMaxEnt = kwargs.get('switchCapLocNetsMaxEnt', None)
        self.switchCapLocNetsCurrEnt = kwargs.get('switchCapLocNetsCurrEnt', None)
        self.switchCapDNSSerMaxEnt = kwargs.get('switchCapDNSSerMaxEnt', None)
        self.switchCapDNSSerCurrEnt = kwargs.get('switchCapDNSSerCurrEnt', None)
        self.switchCapBootpSerMaxEnt = kwargs.get('switchCapBootpSerMaxEnt', None)
        self.switchCapBootpSerCurrEnt = kwargs.get('switchCapBootpSerCurrEnt', None)
        self.switchCapRIPIntfMaxEnt = kwargs.get('switchCapRIPIntfMaxEnt', None)
        self.switchCapRIPIntfCurrEnt = kwargs.get('switchCapRIPIntfCurrEnt', None)
        self.switchCapOSPFIntfMaxEnt = kwargs.get('switchCapOSPFIntfMaxEnt', None)
        self.switchCapOSPFIntfCurrEnt = kwargs.get('switchCapOSPFIntfCurrEnt', None)
        self.switchCapOSPFAreasMaxEnt = kwargs.get('switchCapOSPFAreasMaxEnt', None)
        self.switchCapOSPFAreasCurrEnt = kwargs.get('switchCapOSPFAreasCurrEnt', None)
        self.switchCapOSPFSummaryRangesMaxEnt = kwargs.get('switchCapOSPFSummaryRangesMaxEnt', None)
        self.switchCapOSPFSummaryRangesCurrEnt = kwargs.get('switchCapOSPFSummaryRangesCurrEnt', None)
        self.switchCapOSPFVirtLinksMaxEnt = kwargs.get('switchCapOSPFVirtLinksMaxEnt', None)
        self.switchCapOSPFVirtLinksCurrEnt = kwargs.get('switchCapOSPFVirtLinksCurrEnt', None)
        self.switchCapOSPFHostsMaxEnt = kwargs.get('switchCapOSPFHostsMaxEnt', None)
        self.switchCapOSPFHostsCurrEnt = kwargs.get('switchCapOSPFHostsCurrEnt', None)
        self.switchCapLSDBLimit = kwargs.get('switchCapLSDBLimit', None)
        self.switchCapBGPPeersMaxEnt = kwargs.get('switchCapBGPPeersMaxEnt', None)
        self.switchCapBGPPeersCurrEnt = kwargs.get('switchCapBGPPeersCurrEnt', None)
        self.switchCapBGPRouteAggrsMaxEnt = kwargs.get('switchCapBGPRouteAggrsMaxEnt', None)
        self.switchCapBGPRouteAggrsCurrEnt = kwargs.get('switchCapBGPRouteAggrsCurrEnt', None)
        self.switchCapRouteMapsMaxEnt = kwargs.get('switchCapRouteMapsMaxEnt', None)
        self.switchCapRouteMapsCurrEnt = kwargs.get('switchCapRouteMapsCurrEnt', None)
        self.switchCapNwkFltsMaxEnt = kwargs.get('switchCapNwkFltsMaxEnt', None)
        self.switchCapNwkFltsCurrEnt = kwargs.get('switchCapNwkFltsCurrEnt', None)
        self.switchCapASFlts = kwargs.get('switchCapASFlts', None)
        self.switchCapVRRPRtrsMaxEnt = kwargs.get('switchCapVRRPRtrsMaxEnt', None)
        self.switchCapVRRPRtrsCurrEnt = kwargs.get('switchCapVRRPRtrsCurrEnt', None)
        self.switchCapVRRPRtrGRsMaxEnt = kwargs.get('switchCapVRRPRtrGRsMaxEnt', None)
        self.switchCapVRRPRtrGRsCurrEnt = kwargs.get('switchCapVRRPRtrGRsCurrEnt', None)
        self.switchCapVRRPIntfsMaxEnt = kwargs.get('switchCapVRRPIntfsMaxEnt', None)
        self.switchCapVRRPIntfsCurrEnt = kwargs.get('switchCapVRRPIntfsCurrEnt', None)
        self.switchCapOSPFv3IntfMaxEnt = kwargs.get('switchCapOSPFv3IntfMaxEnt', None)
        self.switchCapOSPFv3IntfCurrEnt = kwargs.get('switchCapOSPFv3IntfCurrEnt', None)
        self.switchCapOSPFv3AreasMaxEnt = kwargs.get('switchCapOSPFv3AreasMaxEnt', None)
        self.switchCapOSPFv3AreasCurrEnt = kwargs.get('switchCapOSPFv3AreasCurrEnt', None)
        self.switchCapOSPFv3SummaryRangesMaxEnt = kwargs.get('switchCapOSPFv3SummaryRangesMaxEnt', None)
        self.switchCapOSPFv3SummaryRangesCurrEnt = kwargs.get('switchCapOSPFv3SummaryRangesCurrEnt', None)
        self.switchCapOSPFv3VirtLinksMaxEnt = kwargs.get('switchCapOSPFv3VirtLinksMaxEnt', None)
        self.switchCapOSPFv3VirtLinksCurrEnt = kwargs.get('switchCapOSPFv3VirtLinksCurrEnt', None)
        self.switchCapOSPFv3HostsMaxEnt = kwargs.get('switchCapOSPFv3HostsMaxEnt', None)
        self.switchCapOSPFv3HostsCurrEnt = kwargs.get('switchCapOSPFv3HostsCurrEnt', None)
        self.switchCapASFltsCurr = kwargs.get('switchCapASFltsCurr', None)
        self.switchCapRealSersMaxEnt = kwargs.get('switchCapRealSersMaxEnt', None)
        self.switchCapRealSersCurrEnt = kwargs.get('switchCapRealSersCurrEnt', None)
        self.switchCapSerGRsMaxEnt = kwargs.get('switchCapSerGRsMaxEnt', None)
        self.switchCapSerGRsCurrEnt = kwargs.get('switchCapSerGRsCurrEnt', None)
        self.switchCapVirtSersMaxEnt = kwargs.get('switchCapVirtSersMaxEnt', None)
        self.switchCapVirtSersCurrEnt = kwargs.get('switchCapVirtSersCurrEnt', None)
        self.switchCapVirtServicesEnt = kwargs.get('switchCapVirtServicesEnt', None)
        self.switchCapRealServicesEnt = kwargs.get('switchCapRealServicesEnt', None)
        self.switchCapRealIDSSer = kwargs.get('switchCapRealIDSSer', None)
        self.switchCapIDSSerGRs = kwargs.get('switchCapIDSSerGRs', None)
        self.switchCapGSLBDomainsMaxEnt = kwargs.get('switchCapGSLBDomainsMaxEnt', None)
        self.switchCapGSLBDomainsCurrEnt = kwargs.get('switchCapGSLBDomainsCurrEnt', None)
        self.switchCapGSLBServicesMaxEnt = kwargs.get('switchCapGSLBServicesMaxEnt', None)
        self.switchCapGSLBServicesCurrEnt = kwargs.get('switchCapGSLBServicesCurrEnt', None)
        self.switchCapGSLBLocSersMaxEnt = kwargs.get('switchCapGSLBLocSersMaxEnt', None)
        self.switchCapGSLBLocSersCurrEnt = kwargs.get('switchCapGSLBLocSersCurrEnt', None)
        self.switchCapGSLBRemSersMaxEnt = kwargs.get('switchCapGSLBRemSersMaxEnt', None)
        self.switchCapGSLBRemSersCurrEnt = kwargs.get('switchCapGSLBRemSersCurrEnt', None)
        self.switchCapGSLBRemSitesMaxEnt = kwargs.get('switchCapGSLBRemSitesMaxEnt', None)
        self.switchCapGSLBRemSitesCurrEnt = kwargs.get('switchCapGSLBRemSitesCurrEnt', None)
        self.switchCapGSLBFailoversPerRemSiteMaxEnt = kwargs.get('switchCapGSLBFailoversPerRemSiteMaxEnt', None)
        self.switchCapGSLBFailoversPerRemSiteCurrEnt = kwargs.get('switchCapGSLBFailoversPerRemSiteCurrEnt', None)
        self.switchCapGSLBNetworksMaxEnt = kwargs.get('switchCapGSLBNetworksMaxEnt', None)
        self.switchCapGSLBNetworksCurrEnt = kwargs.get('switchCapGSLBNetworksCurrEnt', None)
        self.switchCapGSLBGeographicalRegionsMaxEnt = kwargs.get('switchCapGSLBGeographicalRegionsMaxEnt', None)
        self.switchCapGSLBGeographicalRegionsCurrEnt = kwargs.get('switchCapGSLBGeographicalRegionsCurrEnt', None)
        self.switchCapGSLBRulesMaxEnt = kwargs.get('switchCapGSLBRulesMaxEnt', None)
        self.switchCapGSLBRulesCurrEnt = kwargs.get('switchCapGSLBRulesCurrEnt', None)
        self.switchCapGSLBMetricsPerRuleMaxEnt = kwargs.get('switchCapGSLBMetricsPerRuleMaxEnt', None)
        self.switchCapGSLBMetricPerRuleCurrEnt = kwargs.get('switchCapGSLBMetricPerRuleCurrEnt', None)
        self.switchCapGSLBDNSPersCacheMaxEnt = kwargs.get('switchCapGSLBDNSPersCacheMaxEnt', None)
        self.switchCapGSLBDNSPersCacheCurrEnt = kwargs.get('switchCapGSLBDNSPersCacheCurrEnt', None)
        self.switchCapFltsMaxEnt = kwargs.get('switchCapFltsMaxEnt', None)
        self.switchCapFltsCurrEnt = kwargs.get('switchCapFltsCurrEnt', None)
        self.switchCapPIPsMaxEnt = kwargs.get('switchCapPIPsMaxEnt', None)
        self.switchCapPIPsCurrEnt = kwargs.get('switchCapPIPsCurrEnt', None)
        self.switchCapScriptHealthChecksMaxEnt = kwargs.get('switchCapScriptHealthChecksMaxEnt', None)
        self.switchCapScriptHealthChecksCurrEnt = kwargs.get('switchCapScriptHealthChecksCurrEnt', None)
        self.switchCapSNMPHealthChecksMaxEnt = kwargs.get('switchCapSNMPHealthChecksMaxEnt', None)
        self.switchCapSNMPHealthChecksCurrEnt = kwargs.get('switchCapSNMPHealthChecksCurrEnt', None)
        self.switchCapRulesforURLParsingMaxEnt = kwargs.get('switchCapRulesforURLParsingMaxEnt', None)
        self.switchCapRulesforURLParsingCurrEnt = kwargs.get('switchCapRulesforURLParsingCurrEnt', None)
        self.switchCapSLBSessionsMaxEnt = kwargs.get('switchCapSLBSessionsMaxEnt', None)
        self.switchCapSLBSessionsCurrEnt = kwargs.get('switchCapSLBSessionsCurrEnt', None)
        self.switchCapNumofRportstoVport = kwargs.get('switchCapNumofRportstoVport', None)
        self.switchCapDomianRecordsMaxEnt = kwargs.get('switchCapDomianRecordsMaxEnt', None)
        self.switchCapDomainRecordsCurrEnt = kwargs.get('switchCapDomainRecordsCurrEnt', None)
        self.switchCapMappingPerDomainrecord = kwargs.get('switchCapMappingPerDomainrecord', None)
        self.switchCapNetworkClassesMaxEnt = kwargs.get('switchCapNetworkClassesMaxEnt', None)
        self.switchCapNetworkClassesCurrEnt = kwargs.get('switchCapNetworkClassesCurrEnt', None)
        self.switchCapNetworkElementsMaxEnt = kwargs.get('switchCapNetworkElementsMaxEnt', None)
        self.switchCapNetworkElementsCurrEnt = kwargs.get('switchCapNetworkElementsCurrEnt', None)
        self.switchCapAppShapeMaxEnt = kwargs.get('switchCapAppShapeMaxEnt', None)
        self.switchCapAppShapeCurrEnt = kwargs.get('switchCapAppShapeCurrEnt', None)
        self.switchCapDataClassClassesMaxEnt = kwargs.get('switchCapDataClassClassesMaxEnt', None)
        self.switchCapDataClassClassesCurEnt = kwargs.get('switchCapDataClassClassesCurEnt', None)
        self.switchCapDataClassManualEntriesPerClassMaxEnt = kwargs.get('switchCapDataClassManualEntriesPerClassMaxEnt', None)
        self.switchCapDataClassManualEntriesMaxEnt = kwargs.get('switchCapDataClassManualEntriesMaxEnt', None)
        self.switchCapDataClassManualEntriesCurEnt = kwargs.get('switchCapDataClassManualEntriesCurEnt', None)
        self.switchCapDataClassMemMaxSize = kwargs.get('switchCapDataClassMemMaxSize', None)
        self.switchCapDataClassMemCurSize = kwargs.get('switchCapDataClassMemCurSize', None)
        self.switchCapDynamicDataStoreMaxSize = kwargs.get('switchCapDynamicDataStoreMaxSize', None)
        self.switchCapDynamicDataStoreCurSize = kwargs.get('switchCapDynamicDataStoreCurSize', None)
        self.switchCapCachePolMaxEnt = kwargs.get('switchCapCachePolMaxEnt', None)
        self.switchCapCachePolCurrEnt = kwargs.get('switchCapCachePolCurrEnt', None)
        self.switchCapCacheRuleMaxEnt = kwargs.get('switchCapCacheRuleMaxEnt', None)
        self.switchCapCacheRuleCurrEnt = kwargs.get('switchCapCacheRuleCurrEnt', None)
        self.switchCapCacheRuleListMaxEnt = kwargs.get('switchCapCacheRuleListMaxEnt', None)
        self.switchCapCacheRuleListCurrEnt = kwargs.get('switchCapCacheRuleListCurrEnt', None)
        self.switchCapKeysMaxEnt = kwargs.get('switchCapKeysMaxEnt', None)
        self.switchCapKeysCurrEnt = kwargs.get('switchCapKeysCurrEnt', None)
        self.switchCapCertSignReqMaxEnt = kwargs.get('switchCapCertSignReqMaxEnt', None)
        self.switchCapCertSignReqCurrEnt = kwargs.get('switchCapCertSignReqCurrEnt', None)
        self.switchCapServerCertMaxEnt = kwargs.get('switchCapServerCertMaxEnt', None)
        self.switchCapServerCertCurrEnt = kwargs.get('switchCapServerCertCurrEnt', None)
        self.switchCapTrusCACertMaxEnt = kwargs.get('switchCapTrusCACertMaxEnt', None)
        self.switchCapTrusCACertCurrEnt = kwargs.get('switchCapTrusCACertCurrEnt', None)
        self.switchCapInterCACertMaxEnt = kwargs.get('switchCapInterCACertMaxEnt', None)
        self.switchCapInterCACertCurrEnt = kwargs.get('switchCapInterCACertCurrEnt', None)
        self.switchCapCertGroupMaxEnt = kwargs.get('switchCapCertGroupMaxEnt', None)
        self.switchCapCertGroupCurrEnt = kwargs.get('switchCapCertGroupCurrEnt', None)
        self.switchCapSecurityPolicyMaxEnt = kwargs.get('switchCapSecurityPolicyMaxEnt', None)
        self.switchCapSecurityPolicyCurrEnt = kwargs.get('switchCapSecurityPolicyCurrEnt', None)
        self.switchCapSmartNatMaxEnt = kwargs.get('switchCapSmartNatMaxEnt', None)
        self.switchCapSmartNatCurrEnt = kwargs.get('switchCapSmartNatCurrEnt', None)
        self.bwmPoliciesMaxEnt = kwargs.get('bwmPoliciesMaxEnt', None)
        self.bwmPoliciesCurrEnt = kwargs.get('bwmPoliciesCurrEnt', None)
        self.bwmContsMaxEnt = kwargs.get('bwmContsMaxEnt', None)
        self.bwmContsCurrEnt = kwargs.get('bwmContsCurrEnt', None)
        self.bwmGRsMaxEnt = kwargs.get('bwmGRsMaxEnt', None)
        self.bwmGRsCurrEnt = kwargs.get('bwmGRsCurrEnt', None)
        self.bwmContsPerGRs = kwargs.get('bwmContsPerGRs', None)
        self.bwmTimePoliciesPerCont = kwargs.get('bwmTimePoliciesPerCont', None)
        self.configSrcIPACLsMaxEnt = kwargs.get('configSrcIPACLsMaxEnt', None)
        self.configSrcIPACLsCurrEnt = kwargs.get('configSrcIPACLsCurrEnt', None)
        self.bogonSrcIPACLsMaxEnt = kwargs.get('bogonSrcIPACLsMaxEnt', None)
        self.bogonSrcIPACLsCurrEnt = kwargs.get('bogonSrcIPACLsCurrEnt', None)
        self.operSrcIPACLsMaxEnt = kwargs.get('operSrcIPACLsMaxEnt', None)
        self.operSrcIPACLsCurrEnt = kwargs.get('operSrcIPACLsCurrEnt', None)
        self.totalSrcIPACLsMaxEnt = kwargs.get('totalSrcIPACLsMaxEnt', None)
        self.totalSrcIPACLsCurrEnt = kwargs.get('totalSrcIPACLsCurrEnt', None)
        self.configDstIPACLsMaxEnt = kwargs.get('configDstIPACLsMaxEnt', None)
        self.configDstIPACLsCurrEnt = kwargs.get('configDstIPACLsCurrEnt', None)
        self.operDstIPACLsMaxEnt = kwargs.get('operDstIPACLsMaxEnt', None)
        self.operDstIPACLsCurrEnt = kwargs.get('operDstIPACLsCurrEnt', None)
        self.totalDstIPACLsMaxEnt = kwargs.get('totalDstIPACLsMaxEnt', None)
        self.totalDstIPACLsCurrEnt = kwargs.get('totalDstIPACLsCurrEnt', None)
        self.ipDosAtkPrevention = kwargs.get('ipDosAtkPrevention', None)
        self.tcpDosAtkPrevention = kwargs.get('tcpDosAtkPrevention', None)
        self.udpDosAtkPrevention = kwargs.get('udpDosAtkPrevention', None)
        self.icmpDosAtkPrevention = kwargs.get('icmpDosAtkPrevention', None)
        self.igmpDosAtkPrevention = kwargs.get('igmpDosAtkPrevention', None)
        self.arpDosAtkPrevention = kwargs.get('arpDosAtkPrevention', None)
        self.ipv6DosAtkPrevention = kwargs.get('ipv6DosAtkPrevention', None)
        self.totalDosAtkPrevention = kwargs.get('totalDosAtkPrevention', None)
        self.udpBlastProtection = kwargs.get('udpBlastProtection', None)
        self.syslogHostMaxEnt = kwargs.get('syslogHostMaxEnt', None)
        self.syslogHostCurrEnt = kwargs.get('syslogHostCurrEnt', None)
        self.radiusSerMaxEnt = kwargs.get('radiusSerMaxEnt', None)
        self.radiusSerCurrEnt = kwargs.get('radiusSerCurrEnt', None)
        self.tacacsSerMaxEnt = kwargs.get('tacacsSerMaxEnt', None)
        self.tacacsSerCurrEnt = kwargs.get('tacacsSerCurrEnt', None)
        self.ntpSerMaxEnt = kwargs.get('ntpSerMaxEnt', None)
        self.ntpSerCurrEnt = kwargs.get('ntpSerCurrEnt', None)
        self.smtpHostsMaxEnt = kwargs.get('smtpHostsMaxEnt', None)
        self.smtpHostsCurrEnt = kwargs.get('smtpHostsCurrEnt', None)
        self.mgmtNetworksMaxEnt = kwargs.get('mgmtNetworksMaxEnt', None)
        self.mgmtNetworksCurrEnt = kwargs.get('mgmtNetworksCurrEnt', None)
        self.endUsers = kwargs.get('endUsers', None)
        self.panicDumps = kwargs.get('panicDumps', None)
        self.snmpv3UsersMaxEnt = kwargs.get('snmpv3UsersMaxEnt', None)
        self.snmpv3UsersCurrEnt = kwargs.get('snmpv3UsersCurrEnt', None)
        self.snmpv3ViewsMaxEnt = kwargs.get('snmpv3ViewsMaxEnt', None)
        self.snmpv3ViewsCurrEnt = kwargs.get('snmpv3ViewsCurrEnt', None)
        self.snmpv3AccessGRsMaxEnt = kwargs.get('snmpv3AccessGRsMaxEnt', None)
        self.snmpv3AccessGRsCurrEnt = kwargs.get('snmpv3AccessGRsCurrEnt', None)
        self.snmpv3TargetAddrMaxEnt = kwargs.get('snmpv3TargetAddrMaxEnt', None)
        self.snmpv3TargetAddrCurrEnt = kwargs.get('snmpv3TargetAddrCurrEnt', None)
        self.snmpv3TargetParamsMaxEnt = kwargs.get('snmpv3TargetParamsMaxEnt', None)
        self.snmpv3TargetParamsCurrEnt = kwargs.get('snmpv3TargetParamsCurrEnt', None)
        self.ramSize = kwargs.get('ramSize', None)
        self.hardDiskMax = kwargs.get('hardDiskMax', None)
        self.hardDiskCur = kwargs.get('hardDiskCur', None)
        self.cacheUsageMaxEnt = kwargs.get('cacheUsageMaxEnt', None)
        self.cacheUsageCurrEnt = kwargs.get('cacheUsageCurrEnt', None)
        self.ramSizeCurr = kwargs.get('ramSizeCurr', None)
        self.capacityUnitsMax = kwargs.get('capacityUnitsMax', None)
        self.capacityUnitsCurr = kwargs.get('capacityUnitsCurr', None)
        self.vAdcMax = kwargs.get('vAdcMax', None)
        self.vAdcCurr = kwargs.get('vAdcCurr', None)
        self.agLicenseInfoConvStatus = EnumAgLicenseInfoConvStatus.enum(kwargs.get('agLicenseInfoConvStatus', None))
        self.licenseKey = kwargs.get('licenseKey', None)
        self.licenseDelete = EnumLicenseDelete.enum(kwargs.get('licenseDelete', None))
        self.automaticConvType = EnumAutomaticConvType.enum(kwargs.get('automaticConvType', None))
        self.automaticConvStatus = kwargs.get('automaticConvStatus', None)
        self.throPutLicenseKey = kwargs.get('throPutLicenseKey', None)
        self.sslLicenseKey = kwargs.get('sslLicenseKey', None)
        self.compressionLicenseKey = kwargs.get('compressionLicenseKey', None)
        self.vADCLicenseKey = kwargs.get('vADCLicenseKey', None)
        self.fastviewLicenseKey = kwargs.get('fastviewLicenseKey', None)
        self.apmLicenseKey = kwargs.get('apmLicenseKey', None)              #obsolete
        self.wafLicenseKey = kwargs.get('wafLicenseKey', None)
        self.authLicenseKey = kwargs.get('authLicenseKey', None)
        self.fastviewLicenseKeyNext = kwargs.get('fastviewLicenseKeyNext', None)
        self.apmLicenseKeyNext = kwargs.get('apmLicenseKeyNext', None)      #obsolete
        self.wafLicenseKeyNext = kwargs.get('wafLicenseKeyNext', None)
        self.additionalLicenseKey = kwargs.get('additionalLicenseKey', None)
        self.iprepLicenseKey = kwargs.get('iprepLicenseKey', None)
        self.iprepLicenseKeyNext = kwargs.get('iprepLicenseKeyNext', None)
        self.urlfilterLicenseKey = kwargs.get('urlfilterLicenseKey', None)
        self.urlfilterLicenseKeyNext = kwargs.get('urlfilterLicenseKeyNext', None)
        self.agUserNewPasswdOper = kwargs.get('agUserNewPasswdOper', None)
        self.agSecIpAclOperRemAll = EnumAgSecIpAclOperRemAll.enum(kwargs.get('agSecIpAclOperRemAll', None))
        self.agSecIpAclOperDestRemAll = EnumAgSecIpAclOperDestRemAll.enum(kwargs.get('agSecIpAclOperDestRemAll', None))
        self.agSecIpAclOperAddSrcIp = kwargs.get('agSecIpAclOperAddSrcIp', None)
        self.agSecIpAclOperAddMask = kwargs.get('agSecIpAclOperAddMask', None)
        self.agSecIpAclOperAddTimeOut = kwargs.get('agSecIpAclOperAddTimeOut', None)
        self.agSecIpAclOperAddIp = EnumAgSecIpAclOperAddIp.enum(kwargs.get('agSecIpAclOperAddIp', None))
        self.agSecIpAclOperRemIp = kwargs.get('agSecIpAclOperRemIp', None)
        self.agSecIpAclOperRemMask = kwargs.get('agSecIpAclOperRemMask', None)
        self.agSecIpAclOperRemove = EnumAgSecIpAclOperRemove.enum(kwargs.get('agSecIpAclOperRemove', None))
        self.agSecIpAclOperDestAddIpAddr = kwargs.get('agSecIpAclOperDestAddIpAddr', None)
        self.agSecIpAclOperDestAddMask = kwargs.get('agSecIpAclOperDestAddMask', None)
        self.agSecIpAclOperDestAddTimeOut = kwargs.get('agSecIpAclOperDestAddTimeOut', None)
        self.agSecIpAclOperDestAddIp = EnumAgSecIpAclOperDestAddIp.enum(kwargs.get('agSecIpAclOperDestAddIp', None))
        self.agSecIpAclOperDestRemIp = kwargs.get('agSecIpAclOperDestRemIp', None)
        self.agSecIpAclOperDestRemMask = kwargs.get('agSecIpAclOperDestRemMask', None)
        self.agSecIpAclOperDestRemove = EnumAgSecIpAclOperDestRemove.enum(kwargs.get('agSecIpAclOperDestRemove', None))
        self.agSecIpAclOperListSummCfgSrc = kwargs.get('agSecIpAclOperListSummCfgSrc', None)
        self.agSecIpAclOperListSummCfgDst = kwargs.get('agSecIpAclOperListSummCfgDst', None)
        self.agSecIpAclOperListSummOperSrc = kwargs.get('agSecIpAclOperListSummOperSrc', None)
        self.agSecIpAclOperListSummOperDst = kwargs.get('agSecIpAclOperListSummOperDst', None)
        self.agSecIpAclOperListSummBogonSrc = kwargs.get('agSecIpAclOperListSummBogonSrc', None)
        self.agSecIpAclOperListSummTotSrc = kwargs.get('agSecIpAclOperListSummTotSrc', None)
        self.agSecIpAclOperListSummTotDst = kwargs.get('agSecIpAclOperListSummTotDst', None)
        self.agSyslogOperDispLog = EnumAgSyslogOperDispLog.enum(kwargs.get('agSyslogOperDispLog', None))
        self.agClearAppLog = EnumAgClearAppLog.enum(kwargs.get('agClearAppLog', None))
        self.ntpOperSendReq = EnumNtpOperSendReq.enum(kwargs.get('ntpOperSendReq', None))
        self.agPeerSyncConfigOper = EnumAgPeerSyncConfigOper.enum(kwargs.get('agPeerSyncConfigOper', None))
        self.agAppLogAppShape = EnumAgAppLogAppShape.enum(kwargs.get('agAppLogAppShape', None))
        self.agAppLogCaching = EnumAgAppLogCaching.enum(kwargs.get('agAppLogCaching', None))
        self.agAppLogCompression = EnumAgAppLogCompression.enum(kwargs.get('agAppLogCompression', None))
        self.agAppLogContentClass = EnumAgAppLogContentClass.enum(kwargs.get('agAppLogContentClass', None))
        self.agAppLogHTTP = EnumAgAppLogHTTP.enum(kwargs.get('agAppLogHTTP', None))
        self.agAppLogHTTPModification = EnumAgAppLogHTTPModification.enum(kwargs.get('agAppLogHTTPModification', None))
        self.agAppLogSSL = EnumAgAppLogSSL.enum(kwargs.get('agAppLogSSL', None))
        self.agAppLogTCP = EnumAgAppLogTCP.enum(kwargs.get('agAppLogTCP', None))
        self.agAppLogDataTable = EnumAgAppLogDataTable.enum(kwargs.get('agAppLogDataTable', None))
        self.agAppLogMemory = EnumAgAppLogMemory.enum(kwargs.get('agAppLogMemory', None))
        self.agAppLogFastview = EnumAgAppLogFastview.enum(kwargs.get('agAppLogFastview', None))
        self.agAppLogFastviewSmf = EnumAgAppLogFastviewSmf.enum(kwargs.get('agAppLogFastviewSmf', None))
        self.agAppLogExternalFetcher = EnumAgAppLogExternalFetcher.enum(kwargs.get('agAppLogExternalFetcher', None))
        self.agAppLogConfigFlushFreq = kwargs.get('agAppLogConfigFlushFreq', None)
        self.agAppLogConfigMaxFiles = kwargs.get('agAppLogConfigMaxFiles', None)
        self.agAppLogConfigMaxSize = kwargs.get('agAppLogConfigMaxSize', None)
        self.agEnabledSwFeatures = kwargs.get('agEnabledSwFeatures', None)
        self.agEnabledGslbKey = EnumAgEnabledGslbKey.enum(kwargs.get('agEnabledGslbKey', None))
        self.agEnabledBwmKey = EnumAgEnabledBwmKey.enum(kwargs.get('agEnabledBwmKey', None))
        self.agEnabledSecurityKey = EnumAgEnabledSecurityKey.enum(kwargs.get('agEnabledSecurityKey', None))
        self.agEnabledLinklbKey = EnumAgEnabledLinklbKey.enum(kwargs.get('agEnabledLinklbKey', None))
        self.agEnabledOtbKey = EnumAgEnabledOtbKey.enum(kwargs.get('agEnabledOtbKey', None))
        self.agEnabledGeoKey = EnumAgEnabledGeoKey.enum(kwargs.get('agEnabledGeoKey', None))
        self.agApplyConfiguration = EnumAgApplyConfiguration.enum(kwargs.get('agApplyConfiguration', None))
        self.agSavePending = EnumAgSavePending.enum(kwargs.get('agSavePending', None))
        self.agSaveConfiguration = EnumAgSaveConfiguration.enum(kwargs.get('agSaveConfiguration', None))
        self.agRevert = EnumAgRevert.enum(kwargs.get('agRevert', None))
        self.agRevertApply = EnumAgRevertApply.enum(kwargs.get('agRevertApply', None))
        self.agReset = EnumAgReset.enum(kwargs.get('agReset', None))
        self.agConfigForNxtReset = EnumAgConfigForNxtReset.enum(kwargs.get('agConfigForNxtReset', None))
        self.agImageForNxtReset = kwargs.get('agImageForNxtReset', None)
        self.agSoftwareVersion = kwargs.get('agSoftwareVersion', None)
        self.agBootVer = kwargs.get('agBootVer', None)
        self.agImage1Ver = kwargs.get('agImage1Ver', None)
        self.agImage2Ver = kwargs.get('agImage2Ver', None)
        self.agRtcDate = kwargs.get('agRtcDate', None)
        self.agRtcTime = kwargs.get('agRtcTime', None)
        self.agLastSetErrorReason = kwargs.get('agLastSetErrorReason', None)
        self.agNewCfgHttpServerPort = kwargs.get('agNewCfgHttpServerPort', None)
        self.agNewCfgLoginBanner = kwargs.get('agNewCfgLoginBanner', None)
        self.agNewCfgSmtpHost = kwargs.get('agNewCfgSmtpHost', None)
        self.agNewCfgConsole = EnumAgNewCfgConsole.enum(kwargs.get('agNewCfgConsole', None))
        self.agNewCfgBootp = EnumAgNewCfgBootp.enum(kwargs.get('agNewCfgBootp', None))
        self.agNewCfgSnmpTimeout = kwargs.get('agNewCfgSnmpTimeout', None)
        self.agNewCfgTelnetServerPort = kwargs.get('agNewCfgTelnetServerPort', None)
        self.agClearFlashDump = EnumAgClearFlashDump.enum(kwargs.get('agClearFlashDump', None))
        self.agNewCfgTrapSrcIf = kwargs.get('agNewCfgTrapSrcIf', None)
        self.agNewCfgARPMaxRate = kwargs.get('agNewCfgARPMaxRate', None)
        self.agNewCfgICMPMaxRate = kwargs.get('agNewCfgICMPMaxRate', None)
        self.agNewCfgTCPMaxRate = kwargs.get('agNewCfgTCPMaxRate', None)
        self.agNewCfgUDPMaxRate = kwargs.get('agNewCfgUDPMaxRate', None)
        self.agNewCfgHttpsServerPort = kwargs.get('agNewCfgHttpsServerPort', None)
        self.agNewDaylightSavings = EnumAgNewDaylightSavings.enum(kwargs.get('agNewDaylightSavings', None))
        self.agNewCfgIdleCLITimeout = kwargs.get('agNewCfgIdleCLITimeout', None)
        self.agNewCfgXMLCfgServerPort = kwargs.get('agNewCfgXMLCfgServerPort', None)
        self.agNewCfgLoginNotice = kwargs.get('agNewCfgLoginNotice', None)
        self.agPlatformIdentifier = kwargs.get('agPlatformIdentifier', None)
        self.agFormFactor = kwargs.get('agFormFactor', None)
        self.agNewCfgTputInterval = kwargs.get('agNewCfgTputInterval', None)
        self.agNewCfgTputThreshold = kwargs.get('agNewCfgTputThreshold', None)
        self.agMgmtGlobalState = EnumAgMgmtGlobalState.enum(kwargs.get('agMgmtGlobalState', None))
        self.agCurCfgBootVAID = kwargs.get('agCurCfgBootVAID', None)
        self.agNewCfgCfgBootVAID = kwargs.get('agNewCfgCfgBootVAID', None)
        self.agNewCfgPrompt = EnumAgNewCfgPrompt.enum(kwargs.get('agNewCfgPrompt', None))
        self.agVisionDriverActiveName = kwargs.get('agVisionDriverActiveName', None)
        self.agVisionDriverRestoreFromBackup = EnumAgVisionDriverRestoreFromBackup.enum(kwargs.get('agVisionDriverRestoreFromBackup', None))
        self.agNewCfgHCTCPServState = EnumAgNewCfgHCTCPServState.enum(kwargs.get('agNewCfgHCTCPServState', None))
        self.agCfgHcTcpPortNxtIdx = kwargs.get('agCfgHcTcpPortNxtIdx', None)
        self.agImageTrasform = EnumAgImageTrasform.enum(kwargs.get('agImageTrasform', None))
        self.agImageTransformBootOption = EnumAgImageTransformBootOption.enum(kwargs.get('agImageTransformBootOption', None))
        self.agImageTransformID = kwargs.get('agImageTransformID', None)
        self.agNewCfgIdleCUAlloc = EnumAgNewCfgIdleCUAlloc.enum(kwargs.get('agNewCfgIdleCUAlloc', None))
        self.agActiveConfigBlk = kwargs.get('agActiveConfigBlk', None)
        self.agDefaultImageID = kwargs.get('agDefaultImageID', None)
        self.agDefaultImageVer = kwargs.get('agDefaultImageVer', None)
        self.agMgmtConfigForNxtReset = EnumAgMgmtConfigForNxtReset.enum(kwargs.get('agMgmtConfigForNxtReset', None))
        self.agActiveImageName = kwargs.get('agActiveImageName', None)
        self.agNewCfgSmtpHostIPVersion = EnumAgNewCfgSmtpHostIPVersion.enum(kwargs.get('agNewCfgSmtpHostIPVersion', None))
        self.agNewCfgVassign = EnumAgNewCfgVassign.enum(kwargs.get('agNewCfgVassign', None))
        self.agMgmtCurGlobalState = EnumAgMgmtCurGlobalState.enum(kwargs.get('agMgmtCurGlobalState', None))
        self.agSshKeysForNxtReset = EnumAgSshKeysForNxtReset.enum(kwargs.get('agSshKeysForNxtReset', None))
        self.agNewStatReportConnPort = kwargs.get('agNewStatReportConnPort', None)
        self.agNewStatReportStatus = EnumAgNewStatReportStatus.enum(kwargs.get('agNewStatReportStatus', None))
        self.agStatReportProtocolVer = kwargs.get('agStatReportProtocolVer', None)
        self.agStatReportRstCounters = EnumAgStatReportRstCounters.enum(kwargs.get('agStatReportRstCounters', None))
        self.agStatReportError = kwargs.get('agStatReportError', None)
        self.agStatReportNaming = EnumAgStatReportNaming.enum(kwargs.get('agStatReportNaming', None))
        self.agStatReportInterval = kwargs.get('agStatReportInterval', None)
        self.agStatReportClientIPv4Addr = kwargs.get('agStatReportClientIPv4Addr', None)
        self.agShutdown = EnumAgShutdown.enum(kwargs.get('agShutdown', None))
        self.agNewCfgLimitCUAlloc = EnumAgNewCfgLimitCUAlloc.enum(kwargs.get('agNewCfgLimitCUAlloc', None))
        self.agNewIdByNum = EnumAgNewIdByNum.enum(kwargs.get('agNewIdByNum', None))
        self.agSysIdByNum = EnumAgSysIdByNum.enum(kwargs.get('agSysIdByNum', None))
        self.agLastSyncErrorReason = kwargs.get('agLastSyncErrorReason', None)
        self.agSyncStatus = EnumAgSyncStatus.enum(kwargs.get('agSyncStatus', None))
        self.connmngStatsFIPSCard = EnumConnmngStatsFIPSCard.enum(kwargs.get('connmngStatsFIPSCard', None))
        self.agNewCfgBPDUMaxRate = kwargs.get('agNewCfgBPDUMaxRate', None)
        self.agNewCfgZeroTtlMaxRate = kwargs.get('agNewCfgZeroTtlMaxRate', None)
        self.agImageUploadStatus = EnumAgImageUploadStatus.enum(kwargs.get('agImageUploadStatus', None))
        self.agSyncNeeded = EnumAgSyncNeeded.enum(kwargs.get('agSyncNeeded', None))
        self.agMaxRules = kwargs.get('agMaxRules', None)
        self.agMaxNetworks = kwargs.get('agMaxNetworks', None)
        self.agNewCfgGlobalLanguage = EnumAgNewCfgGlobalLanguage.enum(kwargs.get('agNewCfgGlobalLanguage', None))
        self.agLpMode = EnumAgLpMode.enum(kwargs.get('agLpMode', None))
        self.agNewCfgApmSamp = kwargs.get('agNewCfgApmSamp', None)      #obsolete
        self.agNewPerformanceMonitorInterval = kwargs.get('agNewPerformanceMonitorInterval', None)
        self.agNewPerformanceMonitorMaxEntries = kwargs.get('agNewPerformanceMonitorMaxEntries', None)
        self.agNewPerformanceMonitorState = kwargs.get('agNewPerformanceMonitorState', None)
        self.agNewCfgSmtpHost2IPVersion = EnumAgNewCfgSmtpHost2IPVersion.enum(kwargs.get('agNewCfgSmtpHost2IPVersion', None))
        self.agNewCfgSmtpHost2 = kwargs.get('agNewCfgSmtpHost2', None)
        self.agFipsSecurityLevel = EnumAgFipsSecurityLevel.enum(kwargs.get('agFipsSecurityLevel', None))
        self.agFipsNonApprovedMode = kwargs.get('agFipsNonApprovedMode', None)
        self.agNewSecurityReportingServer = EnumAgNewSecurityReportingServer.enum(kwargs.get('agNewSecurityReportingServer', None))
        self.agNewSecurityReportingServerAddr = kwargs.get('agNewSecurityReportingServerAddr', None)
        self.agCurCfgSingleip = EnumAgCurCfgSingleip.enum(kwargs.get('agCurCfgSingleip', None))
        self.agCurSingleIPonSingleNIC = EnumAgCurSingleIPonSingleNIC.enum(kwargs.get('agCurSingleIPonSingleNIC', None))
        self.agAppwallVersion = kwargs.get('agAppwallVersion', None)
        self.agAccCardSupport = EnumAgAccCardSupport.enum(kwargs.get('agAccCardSupport', None))
        self.agDeviceLicMode = EnumAgDeviceLicMode.enum(kwargs.get('agDeviceLicMode', None))
        self.agUpgradeJarVersion = kwargs.get('agUpgradeJarVersion', None)
        self.agUpgradeRuleVersion = kwargs.get('agUpgradeRuleVersion', None)
        self.agUpgradeLog4Version = kwargs.get('agUpgradeLog4Version', None)
        self.agImageForNxtResetNew = kwargs.get('agImageForNxtResetNew', None)
        self.agMgmtNewCfgIpv6Addr = kwargs.get('agMgmtNewCfgIpv6Addr', None)
        self.agMgmtNewCfgIpv6PrefixLen = kwargs.get('agMgmtNewCfgIpv6PrefixLen', None)
        self.agMgmtNewCfgIpv6Gateway = kwargs.get('agMgmtNewCfgIpv6Gateway', None)
        self.agMgmtNewCfgIpv6Addr2 = kwargs.get('agMgmtNewCfgIpv6Addr2', None)
        self.agMgmtNewCfgIpv6PrefixLen2 = kwargs.get('agMgmtNewCfgIpv6PrefixLen2', None)
        self.agMgmtNewCfgIpv6Gateway2 = kwargs.get('agMgmtNewCfgIpv6Gateway2', None)
        self.agMgmtNewCfgArpState = EnumAgMgmtNewCfgArpState.enum(kwargs.get('agMgmtNewCfgArpState', None))
        self.agMgmtNewCfgWsRadius = EnumAgMgmtNewCfgWsRadius.enum(kwargs.get('agMgmtNewCfgWsRadius', None))
        self.agMgmtNewCfgWsLdap = EnumAgMgmtNewCfgWsLdap.enum(kwargs.get('agMgmtNewCfgWsLdap', None))
        self.agMgmtNewCfgDefensePro = EnumAgMgmtNewCfgDefensePro.enum(kwargs.get('agMgmtNewCfgDefensePro', None))
        self.agMgmtNewCfgLinkBonding = EnumAgMgmtNewCfgLinkBonding.enum(kwargs.get('agMgmtNewCfgLinkBonding', None))
        self.agSysNewSyncPasswordMode = EnumAgSysNewSyncPasswordMode.enum(kwargs.get('agSysNewSyncPasswordMode', None))
        self.agSysSyncPassphrase = kwargs.get('agSysSyncPassphrase', None)
        self.agSysNewSyncAutosync = EnumAgSysNewSyncAutosync.enum(kwargs.get('agSysNewSyncAutosync', None))
        self.agNewCfgAPMServerId = kwargs.get('agNewCfgAPMServerId', None)                  #obsolete
        self.agNewCfgAPMServerDataIpAddr = kwargs.get('agNewCfgAPMServerDataIpAddr', None)  #obsolete
        self.agNewCfgAPMServerDataPort = kwargs.get('agNewCfgAPMServerDataPort', None)      #obsolete
        self.agNewCfgAPMServerMgmtIpAddr = kwargs.get('agNewCfgAPMServerMgmtIpAddr', None)  #obsolete
        self.agNewCfgAPMServerDelete = EnumAgNewCfgAPMServerDelete.enum(kwargs.get('agNewCfgAPMServerDelete', None))                                #obsolete
        self.agCurCfgAPMSharepathConfigStatus = EnumAgCurCfgAPMSharepathConfigStatus.enum(kwargs.get('agCurCfgAPMSharepathConfigStatus', None))     #obsolete
        self.agNewCfgSyslogHost = kwargs.get('agNewCfgSyslogHost', None)
        self.agNewCfgSyslog2Host = kwargs.get('agNewCfgSyslog2Host', None)
        self.agNewCfgSyslogFac = EnumAgNewCfgSyslogFac.enum(kwargs.get('agNewCfgSyslogFac', None))
        self.agNewCfgSyslog2Fac = EnumAgNewCfgSyslog2Fac.enum(kwargs.get('agNewCfgSyslog2Fac', None))
        self.agNewCfgSyslogSev = EnumAgNewCfgSyslogSev.enum(kwargs.get('agNewCfgSyslogSev', None))
        self.agNewCfgSyslog2Sev = EnumAgNewCfgSyslog2Sev.enum(kwargs.get('agNewCfgSyslog2Sev', None))
        self.agClrSyslogMsgs = EnumAgClrSyslogMsgs.enum(kwargs.get('agClrSyslogMsgs', None))
        self.agSyslogMsgTableMaxSize = kwargs.get('agSyslogMsgTableMaxSize', None)
        self.agNewCfgSyslog3Host = kwargs.get('agNewCfgSyslog3Host', None)
        self.agNewCfgSyslog4Host = kwargs.get('agNewCfgSyslog4Host', None)
        self.agNewCfgSyslog5Host = kwargs.get('agNewCfgSyslog5Host', None)
        self.agNewCfgSyslog3Fac = EnumAgNewCfgSyslog3Fac.enum(kwargs.get('agNewCfgSyslog3Fac', None))
        self.agNewCfgSyslog4Fac = EnumAgNewCfgSyslog4Fac.enum(kwargs.get('agNewCfgSyslog4Fac', None))
        self.agNewCfgSyslog5Fac = EnumAgNewCfgSyslog5Fac.enum(kwargs.get('agNewCfgSyslog5Fac', None))
        self.agNewCfgSyslog3Sev = EnumAgNewCfgSyslog3Sev.enum(kwargs.get('agNewCfgSyslog3Sev', None))
        self.agNewCfgSyslog4Sev = EnumAgNewCfgSyslog4Sev.enum(kwargs.get('agNewCfgSyslog4Sev', None))
        self.agNewCfgSyslog5Sev = EnumAgNewCfgSyslog5Sev.enum(kwargs.get('agNewCfgSyslog5Sev', None))
        self.agNewCfgAuditTrail = EnumAgNewCfgAuditTrail.enum(kwargs.get('agNewCfgAuditTrail', None))
        self.agNewCfgSyslogHostv6 = kwargs.get('agNewCfgSyslogHostv6', None)
        self.agNewCfgSyslog2Hostv6 = kwargs.get('agNewCfgSyslog2Hostv6', None)
        self.agNewCfgSyslog3Hostv6 = kwargs.get('agNewCfgSyslog3Hostv6', None)
        self.agNewCfgSyslog4Hostv6 = kwargs.get('agNewCfgSyslog4Hostv6', None)
        self.agNewCfgSyslog5Hostv6 = kwargs.get('agNewCfgSyslog5Hostv6', None)
        self.agNewCfgSyslogSessLog = EnumAgNewCfgSyslogSessLog.enum(kwargs.get('agNewCfgSyslogSessLog', None))
        self.agNewCfgSyslogSessLogFieldReal = EnumAgNewCfgSyslogSessLogFieldReal.enum(kwargs.get('agNewCfgSyslogSessLogFieldReal', None))
        self.agNewCfgSyslogSessLogFieldNat = EnumAgNewCfgSyslogSessLogFieldNat.enum(kwargs.get('agNewCfgSyslogSessLogFieldNat', None))
        self.agNewCfgSyslogEmail = EnumAgNewCfgSyslogEmail.enum(kwargs.get('agNewCfgSyslogEmail', None))
        self.agNewCfgSyslogEmailSev = EnumAgNewCfgSyslogEmailSev.enum(kwargs.get('agNewCfgSyslogEmailSev', None))
        self.agNewCfgSyslogEmailToAddress = kwargs.get('agNewCfgSyslogEmailToAddress', None)
        self.agNewCfgSyslogEmailFromAddress = kwargs.get('agNewCfgSyslogEmailFromAddress', None)
        self.agNewCfgSecSyslogHost = kwargs.get('agNewCfgSecSyslogHost', None)
        self.agNewCfgSecSyslogHostv6 = kwargs.get('agNewCfgSecSyslogHostv6', None)
        self.agNewCfgSecSyslogFac = EnumAgNewCfgSecSyslogFac.enum(kwargs.get('agNewCfgSecSyslogFac', None))
        self.agNewCfgSecSyslogSev = EnumAgNewCfgSecSyslogSev.enum(kwargs.get('agNewCfgSecSyslogSev', None))
        self.agNewCfgSyslogFeature = EnumAgNewCfgSyslogFeature.enum(kwargs.get('agNewCfgSyslogFeature', None))
        self.agNewCfgSyslog2Feature = EnumAgNewCfgSyslog2Feature.enum(kwargs.get('agNewCfgSyslog2Feature', None))
        self.agNewCfgSyslog3Feature = EnumAgNewCfgSyslog3Feature.enum(kwargs.get('agNewCfgSyslog3Feature', None))
        self.agNewCfgSyslog4Feature = EnumAgNewCfgSyslog4Feature.enum(kwargs.get('agNewCfgSyslog4Feature', None))
        self.agNewCfgSyslog5Feature = EnumAgNewCfgSyslog5Feature.enum(kwargs.get('agNewCfgSyslog5Feature', None))
        self.agNewCfgSyslogPort = kwargs.get('agNewCfgSyslogPort', None)
        self.agNewCfgSyslog2Port = kwargs.get('agNewCfgSyslog2Port', None)
        self.agNewCfgSyslog3Port = kwargs.get('agNewCfgSyslog3Port', None)
        self.agNewCfgSyslog4Port = kwargs.get('agNewCfgSyslog4Port', None)
        self.agNewCfgSyslog5Port = kwargs.get('agNewCfgSyslog5Port', None)
        self.agNewCfgSyslogExtdlog = EnumAgNewCfgSyslogExtdlog.enum(kwargs.get('agNewCfgSyslogExtdlog', None))
        self.agNewCfgSyslogSessLogMode = EnumAgNewCfgSyslogSessLogMode.enum(kwargs.get('agNewCfgSyslogSessLogMode', None))
        self.agNewCfgSyslogTrapConsole = EnumAgNewCfgSyslogTrapConsole.enum(kwargs.get('agNewCfgSyslogTrapConsole', None))
        self.agNewCfgSyslogTrapSystem = EnumAgNewCfgSyslogTrapSystem.enum(kwargs.get('agNewCfgSyslogTrapSystem', None))
        self.agNewCfgSyslogTrapMgmt = EnumAgNewCfgSyslogTrapMgmt.enum(kwargs.get('agNewCfgSyslogTrapMgmt', None))
        self.agNewCfgSyslogTrapCli = EnumAgNewCfgSyslogTrapCli.enum(kwargs.get('agNewCfgSyslogTrapCli', None))
        self.agNewCfgSyslogTrapStp = EnumAgNewCfgSyslogTrapStp.enum(kwargs.get('agNewCfgSyslogTrapStp', None))
        self.agNewCfgSyslogTrapVlan = EnumAgNewCfgSyslogTrapVlan.enum(kwargs.get('agNewCfgSyslogTrapVlan', None))
        self.agNewCfgSyslogTrapSlb = EnumAgNewCfgSyslogTrapSlb.enum(kwargs.get('agNewCfgSyslogTrapSlb', None))
        self.agNewCfgSyslogTrapGslb = EnumAgNewCfgSyslogTrapGslb.enum(kwargs.get('agNewCfgSyslogTrapGslb', None))
        self.agNewCfgSyslogTrapFilter = EnumAgNewCfgSyslogTrapFilter.enum(kwargs.get('agNewCfgSyslogTrapFilter', None))
        self.agNewCfgSyslogTrapSsh = EnumAgNewCfgSyslogTrapSsh.enum(kwargs.get('agNewCfgSyslogTrapSsh', None))
        self.agNewCfgSyslogTrapVrrp = EnumAgNewCfgSyslogTrapVrrp.enum(kwargs.get('agNewCfgSyslogTrapVrrp', None))
        self.agNewCfgSyslogTrapBgp = EnumAgNewCfgSyslogTrapBgp.enum(kwargs.get('agNewCfgSyslogTrapBgp', None))
        self.agNewCfgSyslogTrapNtp = EnumAgNewCfgSyslogTrapNtp.enum(kwargs.get('agNewCfgSyslogTrapNtp', None))
        self.agNewCfgSyslogTrapIp = EnumAgNewCfgSyslogTrapIp.enum(kwargs.get('agNewCfgSyslogTrapIp', None))
        self.agNewCfgSyslogTrapWeb = EnumAgNewCfgSyslogTrapWeb.enum(kwargs.get('agNewCfgSyslogTrapWeb', None))
        self.agNewCfgSyslogTrapSynAtk = EnumAgNewCfgSyslogTrapSynAtk.enum(kwargs.get('agNewCfgSyslogTrapSynAtk', None))
        self.agNewCfgSyslogTrapTcpLim = EnumAgNewCfgSyslogTrapTcpLim.enum(kwargs.get('agNewCfgSyslogTrapTcpLim', None))
        self.agNewCfgSyslogTrapOspf = EnumAgNewCfgSyslogTrapOspf.enum(kwargs.get('agNewCfgSyslogTrapOspf', None))
        self.agNewCfgSyslogTrapSecurity = EnumAgNewCfgSyslogTrapSecurity.enum(kwargs.get('agNewCfgSyslogTrapSecurity', None))
        self.agNewCfgSyslogTrapRmon = EnumAgNewCfgSyslogTrapRmon.enum(kwargs.get('agNewCfgSyslogTrapRmon', None))
        self.agNewCfgSyslogTrapSlbAtk = EnumAgNewCfgSyslogTrapSlbAtk.enum(kwargs.get('agNewCfgSyslogTrapSlbAtk', None))
        self.agNewCfgSyslogTrapIpv6 = EnumAgNewCfgSyslogTrapIpv6.enum(kwargs.get('agNewCfgSyslogTrapIpv6', None))
        self.agNewCfgSyslogTrapAppSvc = EnumAgNewCfgSyslogTrapAppSvc.enum(kwargs.get('agNewCfgSyslogTrapAppSvc', None))
        self.agNewCfgSyslogTrapFastView = EnumAgNewCfgSyslogTrapFastView.enum(kwargs.get('agNewCfgSyslogTrapFastView', None))
        self.agNewCfgSyslogTrapHA = EnumAgNewCfgSyslogTrapHA.enum(kwargs.get('agNewCfgSyslogTrapHA', None))
        self.agNewCfgSyslogTrapOspfv3 = EnumAgNewCfgSyslogTrapOspfv3.enum(kwargs.get('agNewCfgSyslogTrapOspfv3', None))
        self.agNewCfgSyslogTrapAudit = EnumAgNewCfgSyslogTrapAudit.enum(kwargs.get('agNewCfgSyslogTrapAudit', None))
        self.agNewCfgSyslogUrlf = EnumAgNewCfgSyslogUrlf.enum(kwargs.get('agNewCfgSyslogUrlf', None))
        self.agNewCfgSyslogTrapIprep = EnumAgNewCfgSyslogTrapIprep.enum(kwargs.get('agNewCfgSyslogTrapIprep', None))
        self.agTrapHostTableMaxEnt = kwargs.get('agTrapHostTableMaxEnt', None)
        self.agTftpServer = kwargs.get('agTftpServer', None)
        self.agTftpImage = EnumAgTftpImage.enum(kwargs.get('agTftpImage', None))
        self.agTftpImageFileName = kwargs.get('agTftpImageFileName', None)
        self.agTftpCfgFileName = kwargs.get('agTftpCfgFileName', None)
        self.agTftpDumpFileName = kwargs.get('agTftpDumpFileName', None)
        self.agTftpAction = EnumAgTftpAction.enum(kwargs.get('agTftpAction', None))
        self.agTftpLastActionStatus = kwargs.get('agTftpLastActionStatus', None)
        self.agTftpPort = EnumAgTftpPort.enum(kwargs.get('agTftpPort', None))
        self.agTftpUserName = kwargs.get('agTftpUserName', None)
        self.agTftpPassword = kwargs.get('agTftpPassword', None)
        self.agTftpTSDumpFileName = kwargs.get('agTftpTSDumpFileName', None)
        self.agTftpTechDataFileName = kwargs.get('agTftpTechDataFileName', None)
        self.agTftpVersionPass = kwargs.get('agTftpVersionPass', None)
        self.agTftpMode = EnumAgTftpMode.enum(kwargs.get('agTftpMode', None))
        self.agTftpConfigOption = EnumAgTftpConfigOption.enum(kwargs.get('agTftpConfigOption', None))
        self.agTftpConfigOptionvADC = kwargs.get('agTftpConfigOptionvADC', None)
        self.agTftpConfigTypevADC = EnumAgTftpConfigTypevADC.enum(kwargs.get('agTftpConfigTypevADC', None))
        self.agTftpImageAdc = kwargs.get('agTftpImageAdc', None)
        self.agTftpImageVx = kwargs.get('agTftpImageVx', None)
        self.agTftpSSLCertType = EnumAgTftpSSLCertType.enum(kwargs.get('agTftpSSLCertType', None))
        self.agTftpSSLCertId = kwargs.get('agTftpSSLCertId', None)
        self.agTftpSSLCertKeyPassphrase = kwargs.get('agTftpSSLCertKeyPassphrase', None)
        self.agTftpSSLCertFileName = kwargs.get('agTftpSSLCertFileName', None)
        self.agTftpPrivateKeys = EnumAgTftpPrivateKeys.enum(kwargs.get('agTftpPrivateKeys', None))
        self.agTftpPrivateKeyPassPhrase = kwargs.get('agTftpPrivateKeyPassPhrase', None)
        self.agTftpPrivateKeyConfPassPhrase = kwargs.get('agTftpPrivateKeyConfPassPhrase', None)
        self.agTftpAllowedNetworks = EnumAgTftpAllowedNetworks.enum(kwargs.get('agTftpAllowedNetworks', None))
        self.agCfgTftpHostIPVersion = EnumAgCfgTftpHostIPVersion.enum(kwargs.get('agCfgTftpHostIPVersion', None))
        self.agTftpImageType = EnumAgTftpImageType.enum(kwargs.get('agTftpImageType', None))
        self.agTftpImageDownloadStatus = EnumAgTftpImageDownloadStatus.enum(kwargs.get('agTftpImageDownloadStatus', None))
        self.agTftpManSync = EnumAgTftpManSync.enum(kwargs.get('agTftpManSync', None))
        self.agTftpPrevArchSessLogFile = EnumAgTftpPrevArchSessLogFile.enum(kwargs.get('agTftpPrevArchSessLogFile', None))
        self.agTftpSessLogFileName = kwargs.get('agTftpSessLogFileName', None)
        self.agTftpSshKeyFileName = kwargs.get('agTftpSshKeyFileName', None)
        self.agPortTableMaxEnt = kwargs.get('agPortTableMaxEnt', None)
        self.radNewCfgPrimaryIpAddr = kwargs.get('radNewCfgPrimaryIpAddr', None)
        self.radNewCfgSecondaryIpAddr = kwargs.get('radNewCfgSecondaryIpAddr', None)
        self.radNewCfgPort = kwargs.get('radNewCfgPort', None)
        self.radNewCfgTimeout = kwargs.get('radNewCfgTimeout', None)
        self.radNewCfgRetries = kwargs.get('radNewCfgRetries', None)
        self.radNewCfgState = EnumRadNewCfgState.enum(kwargs.get('radNewCfgState', None))
        self.radNewCfgAuthenString = kwargs.get('radNewCfgAuthenString', None)
        self.radNewCfgTelnet = EnumRadNewCfgTelnet.enum(kwargs.get('radNewCfgTelnet', None))
        self.radNewCfgAuthenSecondString = kwargs.get('radNewCfgAuthenSecondString', None)
        self.radNewCfgSecBd = EnumRadNewCfgSecBd.enum(kwargs.get('radNewCfgSecBd', None))
        self.radNewCfgPrimaryIpv6Addr = kwargs.get('radNewCfgPrimaryIpv6Addr', None)
        self.radNewCfgSecondaryIpv6Addr = kwargs.get('radNewCfgSecondaryIpv6Addr', None)
        self.radNewCfgOtp = EnumRadNewCfgOtp.enum(kwargs.get('radNewCfgOtp', None))
        self.radNewCfgLocalAuth = EnumRadNewCfgLocalAuth.enum(kwargs.get('radNewCfgLocalAuth', None))
        self.agNewCfgNTPServer = kwargs.get('agNewCfgNTPServer', None)
        self.agNewCfgNTPResyncInterval = kwargs.get('agNewCfgNTPResyncInterval', None)
        self.agNewCfgNTPTzoneHHMM = kwargs.get('agNewCfgNTPTzoneHHMM', None)
        self.agNewCfgNTPDlight = EnumAgNewCfgNTPDlight.enum(kwargs.get('agNewCfgNTPDlight', None))
        self.agNewCfgNTPService = EnumAgNewCfgNTPService.enum(kwargs.get('agNewCfgNTPService', None))
        self.agNewCfgNTPSecServer = kwargs.get('agNewCfgNTPSecServer', None)
        self.agNewCfgNTPServerIpv6Addr = kwargs.get('agNewCfgNTPServerIpv6Addr', None)
        self.agNewCfgNTPSecServerIpv6Addr = kwargs.get('agNewCfgNTPSecServerIpv6Addr', None)
        self.agApplyPending = EnumAgApplyPending.enum(kwargs.get('agApplyPending', None))
        self.agApplyConfig = EnumAgApplyConfig.enum(kwargs.get('agApplyConfig', None))
        self.agApplyTableSize = kwargs.get('agApplyTableSize', None)
        self.agMgmtNewCfgIpAddr = kwargs.get('agMgmtNewCfgIpAddr', None)
        self.agMgmtNewCfgMask = kwargs.get('agMgmtNewCfgMask', None)
        self.agMgmtNewCfgGateway = kwargs.get('agMgmtNewCfgGateway', None)
        self.agMgmtNewCfgState = EnumAgMgmtNewCfgState.enum(kwargs.get('agMgmtNewCfgState', None))
        self.agMgmtNewCfgNtp = EnumAgMgmtNewCfgNtp.enum(kwargs.get('agMgmtNewCfgNtp', None))
        self.agMgmtNewCfgRadius = EnumAgMgmtNewCfgRadius.enum(kwargs.get('agMgmtNewCfgRadius', None))
        self.agMgmtNewCfgSmtp = EnumAgMgmtNewCfgSmtp.enum(kwargs.get('agMgmtNewCfgSmtp', None))
        self.agMgmtNewCfgSnmp = EnumAgMgmtNewCfgSnmp.enum(kwargs.get('agMgmtNewCfgSnmp', None))
        self.agMgmtNewCfgSyslog = EnumAgMgmtNewCfgSyslog.enum(kwargs.get('agMgmtNewCfgSyslog', None))
        self.agMgmtNewCfgTftp = EnumAgMgmtNewCfgTftp.enum(kwargs.get('agMgmtNewCfgTftp', None))
        self.agMgmtNewCfgDns = EnumAgMgmtNewCfgDns.enum(kwargs.get('agMgmtNewCfgDns', None))
        self.agMgmtNewCfgTacacs = EnumAgMgmtNewCfgTacacs.enum(kwargs.get('agMgmtNewCfgTacacs', None))
        self.agMgmtNewCfgIntr = kwargs.get('agMgmtNewCfgIntr', None)
        self.agMgmtNewCfgRetry = kwargs.get('agMgmtNewCfgRetry', None)
        self.agMgmtNewCfgWlm = EnumAgMgmtNewCfgWlm.enum(kwargs.get('agMgmtNewCfgWlm', None))
        self.agMgmtNewCfgReport = EnumAgMgmtNewCfgReport.enum(kwargs.get('agMgmtNewCfgReport', None))
        self.agMgmtNewCfgIpAddr2 = kwargs.get('agMgmtNewCfgIpAddr2', None)
        self.agMgmtNewCfgMask2 = kwargs.get('agMgmtNewCfgMask2', None)
        self.agMgmtNewCfgGateway2 = kwargs.get('agMgmtNewCfgGateway2', None)
        self.agMgmtNewCfgState2 = EnumAgMgmtNewCfgState2.enum(kwargs.get('agMgmtNewCfgState2', None))
        self.agMgmtNewCfgCdp = EnumAgMgmtNewCfgCdp.enum(kwargs.get('agMgmtNewCfgCdp', None))
        self.agMgmtNewCfgOcsp = EnumAgMgmtNewCfgOcsp.enum(kwargs.get('agMgmtNewCfgOcsp', None))
        self.agMgmtPortNewCfgSpeed = EnumAgMgmtPortNewCfgSpeed.enum(kwargs.get('agMgmtPortNewCfgSpeed', None))
        self.agMgmtPortNewCfgMode = EnumAgMgmtPortNewCfgMode.enum(kwargs.get('agMgmtPortNewCfgMode', None))
        self.agMgmtPortNewCfgAuto = EnumAgMgmtPortNewCfgAuto.enum(kwargs.get('agMgmtPortNewCfgAuto', None))
        self.agMgmtPortNewCfgSpeed2 = EnumAgMgmtPortNewCfgSpeed2.enum(kwargs.get('agMgmtPortNewCfgSpeed2', None))
        self.agMgmtPortNewCfgMode2 = EnumAgMgmtPortNewCfgMode2.enum(kwargs.get('agMgmtPortNewCfgMode2', None))
        self.agMgmtPortNewCfgAuto2 = EnumAgMgmtPortNewCfgAuto2.enum(kwargs.get('agMgmtPortNewCfgAuto2', None))
        self.agSslprocNewCfgIpAddr = kwargs.get('agSslprocNewCfgIpAddr', None)
        self.agSslprocNewCfgPort = kwargs.get('agSslprocNewCfgPort', None)
        self.agSslprocNewCfgRts = EnumAgSslprocNewCfgRts.enum(kwargs.get('agSslprocNewCfgRts', None))
        self.agSslprocNewCfgFilt = EnumAgSslprocNewCfgFilt.enum(kwargs.get('agSslprocNewCfgFilt', None))
        self.tacNewCfgPrimaryIpAddr = kwargs.get('tacNewCfgPrimaryIpAddr', None)
        self.tacNewCfgSecondaryIpAddr = kwargs.get('tacNewCfgSecondaryIpAddr', None)
        self.tacNewCfgPort = kwargs.get('tacNewCfgPort', None)
        self.tacNewCfgTimeout = kwargs.get('tacNewCfgTimeout', None)
        self.tacNewCfgRetries = kwargs.get('tacNewCfgRetries', None)
        self.tacNewCfgState = EnumTacNewCfgState.enum(kwargs.get('tacNewCfgState', None))
        self.tacNewCfgAuthenString = kwargs.get('tacNewCfgAuthenString', None)
        self.tacNewCfgTelnet = EnumTacNewCfgTelnet.enum(kwargs.get('tacNewCfgTelnet', None))
        self.tacNewCfgAuthenSecondString = kwargs.get('tacNewCfgAuthenSecondString', None)
        self.tacNewCfgCmdAuthor = EnumTacNewCfgCmdAuthor.enum(kwargs.get('tacNewCfgCmdAuthor', None))
        self.tacNewCfgCmdLogging = EnumTacNewCfgCmdLogging.enum(kwargs.get('tacNewCfgCmdLogging', None))
        self.tacNewCfgClogname = EnumTacNewCfgClogname.enum(kwargs.get('tacNewCfgClogname', None))
        self.tacNewCfgSecBd = EnumTacNewCfgSecBd.enum(kwargs.get('tacNewCfgSecBd', None))
        self.tacNewCfgCmap = EnumTacNewCfgCmap.enum(kwargs.get('tacNewCfgCmap', None))
        self.tacNewCfgPrimaryIpv6Addr = kwargs.get('tacNewCfgPrimaryIpv6Addr', None)
        self.tacNewCfgSecondaryIpv6Addr = kwargs.get('tacNewCfgSecondaryIpv6Addr', None)
        self.tacNewCfgOtp = EnumTacNewCfgOtp.enum(kwargs.get('tacNewCfgOtp', None))
        self.tacNewCfgLocalAuth = EnumTacNewCfgLocalAuth.enum(kwargs.get('tacNewCfgLocalAuth', None))
        self.agMgmtNetTableMaxSize = kwargs.get('agMgmtNetTableMaxSize', None)
        self.agPgrpMatchTableMaxSize = kwargs.get('agPgrpMatchTableMaxSize', None)
        self.ipRepEnableNewCfg = EnumIpRepEnableNewCfg.enum(kwargs.get('ipRepEnableNewCfg', None))
        self.ipRepWhiteListTableMaxSize = kwargs.get('ipRepWhiteListTableMaxSize', None)
        self.ipRepCountriesTableMaxSize = kwargs.get('ipRepCountriesTableMaxSize', None)
        self.ipRepNewCfgActionsErtTorLow = EnumIpRepNewCfgActionsErtTorLow.enum(kwargs.get('ipRepNewCfgActionsErtTorLow', None))
        self.ipRepNewCfgActionsErtTorMedium = EnumIpRepNewCfgActionsErtTorMedium.enum(kwargs.get('ipRepNewCfgActionsErtTorMedium', None))
        self.ipRepNewCfgActionsErtTorHigh = EnumIpRepNewCfgActionsErtTorHigh.enum(kwargs.get('ipRepNewCfgActionsErtTorHigh', None))
        self.ipRepNewCfgActionsErtMaliciousLow = EnumIpRepNewCfgActionsErtMaliciousLow.enum(kwargs.get('ipRepNewCfgActionsErtMaliciousLow', None))
        self.ipRepNewCfgActionsErtMaliciousMedium = EnumIpRepNewCfgActionsErtMaliciousMedium.enum(kwargs.get('ipRepNewCfgActionsErtMaliciousMedium', None))
        self.ipRepNewCfgActionsErtMaliciousHigh = EnumIpRepNewCfgActionsErtMaliciousHigh.enum(kwargs.get('ipRepNewCfgActionsErtMaliciousHigh', None))
        self.ipRepNewCfgCountriesMap = kwargs.get('ipRepNewCfgCountriesMap', None)
        self.ipRepNewCfgCountriesMapAddCountry = kwargs.get('ipRepNewCfgCountriesMapAddCountry', None)
        self.ipRepNewCfgCountriesMapRemCountry = kwargs.get('ipRepNewCfgCountriesMapRemCountry', None)
        self.ipRepBaselineLastUpdate = kwargs.get('ipRepBaselineLastUpdate', None)
        self.ipRepBaselineLastUpdateStatus = kwargs.get('ipRepBaselineLastUpdateStatus', None)
        self.ipRepDeltaLastUpdate = kwargs.get('ipRepDeltaLastUpdate', None)
        self.ipRepDeltaLastUpdateStatus = kwargs.get('ipRepDeltaLastUpdateStatus', None)
        self.ipRepVisionUrlNewCfg = kwargs.get('ipRepVisionUrlNewCfg', None)
        self.ipRepIndirectNewCfg = EnumIpRepIndirectNewCfg.enum(kwargs.get('ipRepIndirectNewCfg', None))
        self.ipAclTableMaxSize = kwargs.get('ipAclTableMaxSize', None)
        self.udpBlastudpPortTableMaxSize = kwargs.get('udpBlastudpPortTableMaxSize', None)
        self.udpBlastNewCfgudpPortPacketLimit = kwargs.get('udpBlastNewCfgudpPortPacketLimit', None)
        self.secNewCfgSecurityLogThreshold = kwargs.get('secNewCfgSecurityLogThreshold', None)
        self.secNewCfgPacketDepth = kwargs.get('secNewCfgPacketDepth', None)
        self.secNewCfgIpAclSyslogThreshold = kwargs.get('secNewCfgIpAclSyslogThreshold', None)
        self.secNewCfgIpAclSyslogTime = kwargs.get('secNewCfgIpAclSyslogTime', None)
        self.secNewCfgIpAclSyslogSendMode = EnumSecNewCfgIpAclSyslogSendMode.enum(kwargs.get('secNewCfgIpAclSyslogSendMode', None))
        self.dosNewCfgIPTTL = kwargs.get('dosNewCfgIPTTL', None)
        self.dosNewCfgIPProt = kwargs.get('dosNewCfgIPProt', None)
        self.dosNewCfgFragdata = kwargs.get('dosNewCfgFragdata', None)
        self.dosNewCfgFragoff = kwargs.get('dosNewCfgFragoff', None)
        self.dosNewCfgSYNdata = kwargs.get('dosNewCfgSYNdata', None)
        self.dosNewCfgICMPdata = kwargs.get('dosNewCfgICMPdata', None)
        self.dosNewCfgICMPoff = kwargs.get('dosNewCfgICMPoff', None)
        self.ipDstAclTableMaxSize = kwargs.get('ipDstAclTableMaxSize', None)
        self.agBogonFileSeqNumber = kwargs.get('agBogonFileSeqNumber', None)
        self.secSignalingEnableNewCfg = EnumSecSignalingEnableNewCfg.enum(kwargs.get('secSignalingEnableNewCfg', None))
        self.secSignalingPeriodNewCfg = kwargs.get('secSignalingPeriodNewCfg', None)
        self.secSignalingNewSyslogHostCfg = kwargs.get('secSignalingNewSyslogHostCfg', None)
        self.secSignalingNewSyslogHostCfgv6 = kwargs.get('secSignalingNewSyslogHostCfgv6', None)
        self.secSignalingNewTrapHostCfg = kwargs.get('secSignalingNewTrapHostCfg', None)
        self.secSignalingNewTrapHostCfgv6 = kwargs.get('secSignalingNewTrapHostCfgv6', None)
        self.secSignalingNewSyslogHostSev = EnumSecSignalingNewSyslogHostSev.enum(kwargs.get('secSignalingNewSyslogHostSev', None))
        self.secSignalingNewSyslogHostFac = EnumSecSignalingNewSyslogHostFac.enum(kwargs.get('secSignalingNewSyslogHostFac', None))
        self.agPortAccessTableMaxSize = kwargs.get('agPortAccessTableMaxSize', None)
        self.agVLANAccessTableMaxSize = kwargs.get('agVLANAccessTableMaxSize', None)
        self.agSaveConfig = EnumAgSaveConfig.enum(kwargs.get('agSaveConfig', None))
        self.agSaveTableSize = kwargs.get('agSaveTableSize', None)
        self.agFileSize = kwargs.get('agFileSize', None)
        self.agFileTransferState = EnumAgFileTransferState.enum(kwargs.get('agFileTransferState', None))
        self.agFileTableMissingRows = kwargs.get('agFileTableMissingRows', None)
        self.agFileType = EnumAgFileType.enum(kwargs.get('agFileType', None))
        self.agFileTableSize = kwargs.get('agFileTableSize', None)
        self.agFileErrorTableSize = kwargs.get('agFileErrorTableSize', None)
        self.agAccessUsrPasswd = kwargs.get('agAccessUsrPasswd', None)
        self.agAccessSlbOperPasswd = kwargs.get('agAccessSlbOperPasswd', None)
        self.agAccessL4OperPasswd = kwargs.get('agAccessL4OperPasswd', None)
        self.agAccessOperPasswd = kwargs.get('agAccessOperPasswd', None)
        self.agAccessSlbAdminPasswd = kwargs.get('agAccessSlbAdminPasswd', None)
        self.agAccessL4AdminPasswd = kwargs.get('agAccessL4AdminPasswd', None)
        self.agAccessAdminPasswd = kwargs.get('agAccessAdminPasswd', None)
        self.agAccessAdminNewPasswd = kwargs.get('agAccessAdminNewPasswd', None)
        self.agAccessAdminConfNewPasswd = kwargs.get('agAccessAdminConfNewPasswd', None)
        self.agAccessSlbViewerPasswd = kwargs.get('agAccessSlbViewerPasswd', None)
        self.agAccessWsAdminPasswd = kwargs.get('agAccessWsAdminPasswd', None)
        self.agAccessTelnet = EnumAgAccessTelnet.enum(kwargs.get('agAccessTelnet', None))
        self.agAccessHttp = EnumAgAccessHttp.enum(kwargs.get('agAccessHttp', None))
        self.agAccessNewCfgHttpsState = EnumAgAccessNewCfgHttpsState.enum(kwargs.get('agAccessNewCfgHttpsState', None))
        self.agAccessNewCfgHttpsPort = kwargs.get('agAccessNewCfgHttpsPort', None)
        self.agAccessNewCfgHttpsCert = kwargs.get('agAccessNewCfgHttpsCert', None)
        self.agAccessNewCfgHttpsIntermcaChainName = kwargs.get('agAccessNewCfgHttpsIntermcaChainName', None)
        self.agAccessNewCfgHttpsIntermcaChainType = kwargs.get('agAccessNewCfgHttpsIntermcaChainType', None)
        self.agAccessNewTls10State = EnumAgAccessNewTls10State.enum(kwargs.get('agAccessNewTls10State', None))
        self.agAccessNewTls11State = EnumAgAccessNewTls11State.enum(kwargs.get('agAccessNewTls11State', None))
        self.agAccessNewTls12State = EnumAgAccessNewTls12State.enum(kwargs.get('agAccessNewTls12State', None))
        self.agAccessNewTls13State = EnumAgAccessNewTls13State.enum(kwargs.get('agAccessNewTls13State', None))
        self.agAccessNewCfgSnmpAccess = EnumAgAccessNewCfgSnmpAccess.enum(kwargs.get('agAccessNewCfgSnmpAccess', None))
        self.agAccessNewCfgSnmpReadComm = kwargs.get('agAccessNewCfgSnmpReadComm', None)
        self.agAccessNewCfgSnmpWriteComm = kwargs.get('agAccessNewCfgSnmpWriteComm', None)
        self.agAccessNewCfgSnmpTrap1 = kwargs.get('agAccessNewCfgSnmpTrap1', None)
        self.agAccessNewCfgSnmpTrap2 = kwargs.get('agAccessNewCfgSnmpTrap2', None)
        self.agAccessNewCfgSnmpTrap1Ipv6Addr = kwargs.get('agAccessNewCfgSnmpTrap1Ipv6Addr', None)
        self.agAccessNewCfgSnmpTrap2Ipv6Addr = kwargs.get('agAccessNewCfgSnmpTrap2Ipv6Addr', None)
        self.agAccessNewCfgSshPort = kwargs.get('agAccessNewCfgSshPort', None)
        self.agAccessNewCfgSshV1 = EnumAgAccessNewCfgSshV1.enum(kwargs.get('agAccessNewCfgSshV1', None))
        self.agAccessNewCfgSshScp = EnumAgAccessNewCfgSshScp.enum(kwargs.get('agAccessNewCfgSshScp', None))
        self.agAccessNewCfgSshState = EnumAgAccessNewCfgSshState.enum(kwargs.get('agAccessNewCfgSshState', None))
        self.agNewCfgXMLCfgState = EnumAgNewCfgXMLCfgState.enum(kwargs.get('agNewCfgXMLCfgState', None))
        self.agCfgXMLCertExpire = kwargs.get('agCfgXMLCertExpire', None)
        self.agCfgXMLCertSubjectCountry = kwargs.get('agCfgXMLCertSubjectCountry', None)
        self.agCfgXMLCertSubjectState = kwargs.get('agCfgXMLCertSubjectState', None)
        self.agCfgXMLCertSubjectLocality = kwargs.get('agCfgXMLCertSubjectLocality', None)
        self.agCfgXMLCertSubjectOrg = kwargs.get('agCfgXMLCertSubjectOrg', None)
        self.agCfgXMLCertSubjectOrgUnit = kwargs.get('agCfgXMLCertSubjectOrgUnit', None)
        self.agCfgXMLCertSubjectCommonName = kwargs.get('agCfgXMLCertSubjectCommonName', None)
        self.agCfgXMLCertSubjectEmail = kwargs.get('agCfgXMLCertSubjectEmail', None)
        self.agCfgXMLCertSignatureAlg = kwargs.get('agCfgXMLCertSignatureAlg', None)
        self.agCfgXMLClientCertName = kwargs.get('agCfgXMLClientCertName', None)
        self.agCfgXMLClientCertDelete = EnumAgCfgXMLClientCertDelete.enum(kwargs.get('agCfgXMLClientCertDelete', None))
        self.agAccessNewCfgUserAutolock = EnumAgAccessNewCfgUserAutolock.enum(kwargs.get('agAccessNewCfgUserAutolock', None))
        self.agAccessNewCfgUserLockTreshld = kwargs.get('agAccessNewCfgUserLockTreshld', None)
        self.agAccessNewCfgUserLockDuration = kwargs.get('agAccessNewCfgUserLockDuration', None)
        self.agAccessNewCfgUserLockResetTime = kwargs.get('agAccessNewCfgUserLockResetTime', None)
        self.agAccessNewCfgSnmpV1V2Access = EnumAgAccessNewCfgSnmpV1V2Access.enum(kwargs.get('agAccessNewCfgSnmpV1V2Access', None))
        self.agNewCfgThresholdInterval = kwargs.get('agNewCfgThresholdInterval', None)
        self.agNewCfgThresholdThrput = kwargs.get('agNewCfgThresholdThrput', None)
        self.agNewCfgThresholdSSLCps = kwargs.get('agNewCfgThresholdSSLCps', None)
        self.agNewCfgThresholdCompress = kwargs.get('agNewCfgThresholdCompress', None)
        self.agNewCfgThresholdApm = kwargs.get('agNewCfgThresholdApm', None) #obsolete
        self.agNewCfgThresholdSPCpu = kwargs.get('agNewCfgThresholdSPCpu', None)
        self.agNewCfgThresholdMPCpu = kwargs.get('agNewCfgThresholdMPCpu', None)
        self.agCurCfgThresholdSPClrCpu = kwargs.get('agCurCfgThresholdSPClrCpu', None)
        self.agCurCfgThresholdMPClrCpu = kwargs.get('agCurCfgThresholdMPClrCpu', None)
        self.agNewCfgThresholdSessTblCritical = kwargs.get('agNewCfgThresholdSessTblCritical', None)
        self.agNewCfgThresholdSessTblHigh = kwargs.get('agNewCfgThresholdSessTblHigh', None)
        self.agNewCfgThresholdPrximityTblHigh = kwargs.get('agNewCfgThresholdPrximityTblHigh', None)
        self.licCompanyName = kwargs.get('licCompanyName', None)
        self.licSwitchLocation = kwargs.get('licSwitchLocation', None)
        self.licContact = kwargs.get('licContact', None)
        self.licCookie = EnumLicCookie.enum(kwargs.get('licCookie', None))
        self.agSnmpErrorRequestId = kwargs.get('agSnmpErrorRequestId', None)
        self.pktStatsAllocs = kwargs.get('pktStatsAllocs', None)
        self.pktStatsFrees = kwargs.get('pktStatsFrees', None)
        self.pktStatsAllocFails = kwargs.get('pktStatsAllocFails', None)
        self.pktStatsMediums = kwargs.get('pktStatsMediums', None)
        self.pktStatsJumbos = kwargs.get('pktStatsJumbos', None)
        self.pktStatsSmalls = kwargs.get('pktStatsSmalls', None)
        self.pktStatsMediumsHiWatermark = kwargs.get('pktStatsMediumsHiWatermark', None)
        self.pktStatsJumbosHiWatermark = kwargs.get('pktStatsJumbosHiWatermark', None)
        self.pktStatsSmallsHiWatermark = kwargs.get('pktStatsSmallsHiWatermark', None)
        self.pktStatsDiscards = kwargs.get('pktStatsDiscards', None)
        self.pktStatsDynAllocated = kwargs.get('pktStatsDynAllocated', None)
        self.pktStatsDynFreed = kwargs.get('pktStatsDynFreed', None)
        self.pktStatsDynInUse = kwargs.get('pktStatsDynInUse', None)
        self.pktStatsDynAllocFails = kwargs.get('pktStatsDynAllocFails', None)
        self.mpCpuStatsUtil1Second = kwargs.get('mpCpuStatsUtil1Second', None)
        self.mpCpuStatsUtil4Seconds = kwargs.get('mpCpuStatsUtil4Seconds', None)
        self.mpCpuStatsUtil64Seconds = kwargs.get('mpCpuStatsUtil64Seconds', None)
        self.portMirrorStatsClear = EnumPortMirrorStatsClear.enum(kwargs.get('portMirrorStatsClear', None))
        self.peakThroughputUsage = kwargs.get('peakThroughputUsage', None)
        self.curThroughputUsage = kwargs.get('curThroughputUsage', None)
        self.peakSslCapUsage = kwargs.get('peakSslCapUsage', None)
        self.curSslCapUsage = kwargs.get('curSslCapUsage', None)
        self.peakComprsnCapUsage = kwargs.get('peakComprsnCapUsage', None)
        self.curComprsnCapUsage = kwargs.get('curComprsnCapUsage', None)
        self.clearCapacityUsageStats = EnumClearCapacityUsageStats.enum(kwargs.get('clearCapacityUsageStats', None))
        self.peakApmCapUsage = kwargs.get('peakApmCapUsage', None)      #obsolete
        self.curApmCapUsage = kwargs.get('curApmCapUsage', None)        #obsolete
        self.mpMemStatsTotal = kwargs.get('mpMemStatsTotal', None)
        self.mpMemStatsFree = kwargs.get('mpMemStatsFree', None)
        self.mpMemStatsVirtual = kwargs.get('mpMemStatsVirtual', None)
        self.mpMemStatsRss = kwargs.get('mpMemStatsRss', None)
        self.ntpPrimaryServerReqSent = kwargs.get('ntpPrimaryServerReqSent', None)
        self.ntpPrimaryServerRespRcvd = kwargs.get('ntpPrimaryServerRespRcvd', None)
        self.ntpPrimaryServerUpdates = kwargs.get('ntpPrimaryServerUpdates', None)
        self.ntpSecondaryServerReqSent = kwargs.get('ntpSecondaryServerReqSent', None)
        self.ntpSecondaryServerRespRcvd = kwargs.get('ntpSecondaryServerRespRcvd', None)
        self.ntpSecondaryServerUpdates = kwargs.get('ntpSecondaryServerUpdates', None)
        self.ntpLastUpdateServer = EnumNtpLastUpdateServer.enum(kwargs.get('ntpLastUpdateServer', None))
        self.ntpLastUpdateTime = kwargs.get('ntpLastUpdateTime', None)
        self.ntpClearStats = EnumNtpClearStats.enum(kwargs.get('ntpClearStats', None))
        self.ntpSystemCurrentTime = kwargs.get('ntpSystemCurrentTime', None)
        self.snmpClearStats = EnumSnmpClearStats.enum(kwargs.get('snmpClearStats', None))
        self.agDiffState = EnumAgDiffState.enum(kwargs.get('agDiffState', None))
        self.agDiffTableSize = kwargs.get('agDiffTableSize', None)
        self.agCfgDumpState = EnumAgCfgDumpState.enum(kwargs.get('agCfgDumpState', None))
        self.agCfgDumpTableSize = kwargs.get('agCfgDumpTableSize', None)
        self.systemMemStatsTotalMemory = kwargs.get('systemMemStatsTotalMemory', None)
        self.systemMemStatsInitConfigMemory = kwargs.get('systemMemStatsInitConfigMemory', None)
        self.systemMemStatsNumOfSPs = kwargs.get('systemMemStatsNumOfSPs', None)
        self.systemMemStatsInitFreeRam = kwargs.get('systemMemStatsInitFreeRam', None)
        self.systemMemStatsInitCachedRam = kwargs.get('systemMemStatsInitCachedRam', None)
        self.systemMemStatsSafetyMargin1 = kwargs.get('systemMemStatsSafetyMargin1', None)
        self.systemMemStatsSafetyMargin2 = kwargs.get('systemMemStatsSafetyMargin2', None)
        self.systemMemStatsMemoryLimitEna = EnumSystemMemStatsMemoryLimitEna.enum(kwargs.get('systemMemStatsMemoryLimitEna', None))
        self.systemMemStatsMemoryTrapsEna = EnumSystemMemStatsMemoryTrapsEna.enum(kwargs.get('systemMemStatsMemoryTrapsEna', None))
        self.mgmtStatsRxpackets = kwargs.get('mgmtStatsRxpackets', None)
        self.mgmtStatsRxErrors = kwargs.get('mgmtStatsRxErrors', None)
        self.mgmtStatsRxDropped = kwargs.get('mgmtStatsRxDropped', None)
        self.mgmtStatsRxOverruns = kwargs.get('mgmtStatsRxOverruns', None)
        self.mgmtStatsRxFrame = kwargs.get('mgmtStatsRxFrame', None)
        self.mgmtStatsTxpackets = kwargs.get('mgmtStatsTxpackets', None)
        self.mgmtStatsTxErrors = kwargs.get('mgmtStatsTxErrors', None)
        self.mgmtStatsTxDropped = kwargs.get('mgmtStatsTxDropped', None)
        self.mgmtStatsTxOverruns = kwargs.get('mgmtStatsTxOverruns', None)
        self.mgmtStatsTxCarrier = kwargs.get('mgmtStatsTxCarrier', None)
        self.mgmtStatsTxCollisions = kwargs.get('mgmtStatsTxCollisions', None)
        self.mgmtStatsTxQueueLen = kwargs.get('mgmtStatsTxQueueLen', None)
        self.mgmtStatsRxBytes = kwargs.get('mgmtStatsRxBytes', None)
        self.mgmtStatsRxMulticast = kwargs.get('mgmtStatsRxMulticast', None)
        self.mgmtStatsTxBytes = kwargs.get('mgmtStatsTxBytes', None)
        self.ipAclBogonInfoTableMaxSize = kwargs.get('ipAclBogonInfoTableMaxSize', None)
        self.mgmtPortInfoSpeed = EnumMgmtPortInfoSpeed.enum(kwargs.get('mgmtPortInfoSpeed', None))
        self.mgmtPortInfoMode = EnumMgmtPortInfoMode.enum(kwargs.get('mgmtPortInfoMode', None))
        self.mgmtPortInfoLink = EnumMgmtPortInfoLink.enum(kwargs.get('mgmtPortInfoLink', None))
        self.hwMainBoardNumber = kwargs.get('hwMainBoardNumber', None)
        self.hwMainBoardRevision = kwargs.get('hwMainBoardRevision', None)
        self.hwEthernetBoardNumber = kwargs.get('hwEthernetBoardNumber', None)
        self.hwEthernetBoardRevision = kwargs.get('hwEthernetBoardRevision', None)
        self.hwMACAddress = kwargs.get('hwMACAddress', None)
        self.hwLicMACAddress = kwargs.get('hwLicMACAddress', None)
        self.hwFABNumber = kwargs.get('hwFABNumber', None)
        self.hwSerialNumber = kwargs.get('hwSerialNumber', None)
        self.hwManufacturingDate = kwargs.get('hwManufacturingDate', None)
        self.hwPLDFirmwareVersion = kwargs.get('hwPLDFirmwareVersion', None)
        self.hwTemperatureSensor1 = kwargs.get('hwTemperatureSensor1', None)
        self.hwTemperatureSensor2 = kwargs.get('hwTemperatureSensor2', None)
        self.hwDRAMSize = kwargs.get('hwDRAMSize', None)
        self.hwFlashSize = kwargs.get('hwFlashSize', None)
        self.hwNumberOfHD = kwargs.get('hwNumberOfHD', None)
        self.hwTemperatureWarningThresholdGet = kwargs.get('hwTemperatureWarningThresholdGet', None)
        self.hwTemperatureShutdownThresholdGet = kwargs.get('hwTemperatureShutdownThresholdGet', None)
        self.hwTemperatureThresholdStatusCPU1Get = EnumHwTemperatureThresholdStatusCPU1Get.enum(kwargs.get('hwTemperatureThresholdStatusCPU1Get', None))
        self.hwTemperatureThresholdStatusCPU2Get = EnumHwTemperatureThresholdStatusCPU2Get.enum(kwargs.get('hwTemperatureThresholdStatusCPU2Get', None))
        self.hwPowerSupplyTrapStatus = kwargs.get('hwPowerSupplyTrapStatus', None)
        self.hwPowerSupplyStatus = EnumHwPowerSupplyStatus.enum(kwargs.get('hwPowerSupplyStatus', None))
        self.hwVersion = kwargs.get('hwVersion', None)
        self.hwSslChipInfo = kwargs.get('hwSslChipInfo', None)
        self.hwApplicationSwitchNameInfo = kwargs.get('hwApplicationSwitchNameInfo', None)
        self.portStatsTotalInOctetsPerSec = kwargs.get('portStatsTotalInOctetsPerSec', None)
        self.portStatsTotalOutOctetsPerSec = kwargs.get('portStatsTotalOutOctetsPerSec', None)
        self.agSwitchUpTime = kwargs.get('agSwitchUpTime', None)
        self.agSwitchConfigChangeTime = kwargs.get('agSwitchConfigChangeTime', None)
        self.agSwitchConfigChangeTimeStr = kwargs.get('agSwitchConfigChangeTimeStr', None)
        self.agSwitchLastBootTime = kwargs.get('agSwitchLastBootTime', None)
        self.agSwitchLastApplyTime = kwargs.get('agSwitchLastApplyTime', None)
        self.agSwitchLastSaveTime = kwargs.get('agSwitchLastSaveTime', None)
        self.agSwitchTimeSinceLastSlbStatsClear = kwargs.get('agSwitchTimeSinceLastSlbStatsClear', None)
        self.agGeoDbAutoLastSuccUpdate = kwargs.get('agGeoDbAutoLastSuccUpdate', None)
        self.agGeoDbAutoLastFailedUpdate = kwargs.get('agGeoDbAutoLastFailedUpdate', None)
        self.agGeoDbIsLicValid = EnumAgGeoDbIsLicValid.enum(kwargs.get('agGeoDbIsLicValid', None))
        self.agentSwExtInfo = EnumAgentSwExtInfo.enum(kwargs.get('agentSwExtInfo', None))
        self.agAppwallWafStatus = EnumAgAppwallWafStatus.enum(kwargs.get('agAppwallWafStatus', None))
        self.agAppwallProcessId = kwargs.get('agAppwallProcessId', None)
        self.agAppwallProcessMemUsage = kwargs.get('agAppwallProcessMemUsage', None)
        self.agIpRepStatus = EnumAgIpRepStatus.enum(kwargs.get('agIpRepStatus', None))
        self.agIpRepStatusReason = kwargs.get('agIpRepStatusReason', None)
        self.agLastSyncInfoTableToString = kwargs.get('agLastSyncInfoTableToString', None)
        self.agNewCfgGeoDbAutoUpdate = EnumAgNewCfgGeoDbAutoUpdate.enum(kwargs.get('agNewCfgGeoDbAutoUpdate', None))
        self.agAppwallWebUIMode = EnumAgAppwallWebUIMode.enum(kwargs.get('agAppwallWebUIMode', None))
        self.ipRepCountStatsAllowErtTorLow = kwargs.get('ipRepCountStatsAllowErtTorLow', None)
        self.ipRepCountStatsAllowErtTorMedium = kwargs.get('ipRepCountStatsAllowErtTorMedium', None)
        self.ipRepCountStatsAllowErtTorHigh = kwargs.get('ipRepCountStatsAllowErtTorHigh', None)
        self.ipRepCountStatsAllowErtMaliciousLow = kwargs.get('ipRepCountStatsAllowErtMaliciousLow', None)
        self.ipRepCountStatsAllowErtMaliciousMedium = kwargs.get('ipRepCountStatsAllowErtMaliciousMedium', None)
        self.ipRepCountStatsAllowErtMaliciousHigh = kwargs.get('ipRepCountStatsAllowErtMaliciousHigh', None)
        self.ipRepCountStatsBlockErtTorLow = kwargs.get('ipRepCountStatsBlockErtTorLow', None)
        self.ipRepCountStatsBlockErtTorMedium = kwargs.get('ipRepCountStatsBlockErtTorMedium', None)
        self.ipRepCountStatsBlockErtTorHigh = kwargs.get('ipRepCountStatsBlockErtTorHigh', None)
        self.ipRepCountStatsBlockErtMaliciousLow = kwargs.get('ipRepCountStatsBlockErtMaliciousLow', None)
        self.ipRepCountStatsBlockErtMaliciousMedium = kwargs.get('ipRepCountStatsBlockErtMaliciousMedium', None)
        self.ipRepCountStatsBlockErtMaliciousHigh = kwargs.get('ipRepCountStatsBlockErtMaliciousHigh', None)
        self.ipRepCountStatsAlarmErtTorLow = kwargs.get('ipRepCountStatsAlarmErtTorLow', None)
        self.ipRepCountStatsAlarmErtTorMedium = kwargs.get('ipRepCountStatsAlarmErtTorMedium', None)
        self.ipRepCountStatsAlarmErtTorHigh = kwargs.get('ipRepCountStatsAlarmErtTorHigh', None)
        self.ipRepCountStatsAlarmErtMaliciousLow = kwargs.get('ipRepCountStatsAlarmErtMaliciousLow', None)
        self.ipRepCountStatsAlarmErtMaliciousMedium = kwargs.get('ipRepCountStatsAlarmErtMaliciousMedium', None)
        self.ipRepCountStatsAlarmErtMaliciousHigh = kwargs.get('ipRepCountStatsAlarmErtMaliciousHigh', None)
        self.ipRepCountStatsClear = EnumIpRepCountStatsClear.enum(kwargs.get('ipRepCountStatsClear', None))
        self.ipRepCountStatsWhiteListHits = kwargs.get('ipRepCountStatsWhiteListHits', None)
        self.agSysDiskNewCfgCriThreshold = kwargs.get('agSysDiskNewCfgCriThreshold', None)
        self.agSysDiskNewCfgCriInterval = kwargs.get('agSysDiskNewCfgCriInterval', None)
        self.agSysDiskNewCfgCriEnable = EnumAgSysDiskNewCfgCriEnable.enum(kwargs.get('agSysDiskNewCfgCriEnable', None))
        self.agSysDiskNewCfgExtThreshold = kwargs.get('agSysDiskNewCfgExtThreshold', None)
        self.agSysDiskNewCfgExtInterval = kwargs.get('agSysDiskNewCfgExtInterval', None)
        self.agSysDiskNewCfgExtEnable = EnumAgSysDiskNewCfgExtEnable.enum(kwargs.get('agSysDiskNewCfgExtEnable', None))
        self.agSysDiskNewCfgHighThreshold = kwargs.get('agSysDiskNewCfgHighThreshold', None)
        self.agSysDiskNewCfgHighInterval = kwargs.get('agSysDiskNewCfgHighInterval', None)
        self.agSysDiskNewCfgHighEnable = EnumAgSysDiskNewCfgHighEnable.enum(kwargs.get('agSysDiskNewCfgHighEnable', None))
        self.agSysCurUsedDiskspace = kwargs.get('agSysCurUsedDiskspace', None)
        self.agSysCurTotalDiskspace = kwargs.get('agSysCurTotalDiskspace', None)
        self.vlanMaxEnt = kwargs.get('vlanMaxEnt', None)
        self.vlanMaxVlanID = kwargs.get('vlanMaxVlanID', None)
        self.lacpNewSystemPriority = kwargs.get('lacpNewSystemPriority', None)
        self.lacpNewSystemTimeoutTime = EnumLacpNewSystemTimeoutTime.enum(kwargs.get('lacpNewSystemTimeoutTime', None))
        self.lacpNewSystemName = kwargs.get('lacpNewSystemName', None)
        self.lacpNewBlockPort = EnumLacpNewBlockPort.enum(kwargs.get('lacpNewBlockPort', None))
        self.trunkGroupTableMaxSize = kwargs.get('trunkGroupTableMaxSize', None)
        self.pmNewCfgPortMirrState = EnumPmNewCfgPortMirrState.enum(kwargs.get('pmNewCfgPortMirrState', None))
        self.mstNewCfgState = EnumMstNewCfgState.enum(kwargs.get('mstNewCfgState', None))
        self.mstNewCfgRegionName = kwargs.get('mstNewCfgRegionName', None)
        self.mstNewCfgRegionVersion = kwargs.get('mstNewCfgRegionVersion', None)
        self.mstNewCfgMaxHopCount = kwargs.get('mstNewCfgMaxHopCount', None)
        self.mstNewCfgStpMode = EnumMstNewCfgStpMode.enum(kwargs.get('mstNewCfgStpMode', None))
        self.mstCistDefaultCfg = EnumMstCistDefaultCfg.enum(kwargs.get('mstCistDefaultCfg', None))
        self.mstCistNewCfgBridgePriority = kwargs.get('mstCistNewCfgBridgePriority', None)
        self.mstCistNewCfgBridgeMaxAge = kwargs.get('mstCistNewCfgBridgeMaxAge', None)
        self.mstCistNewCfgBridgeForwardDelay = kwargs.get('mstCistNewCfgBridgeForwardDelay', None)
        self.portTeamTableMaxSize = kwargs.get('portTeamTableMaxSize', None)
        self.hwBypassNewState = EnumHwBypassNewState.enum(kwargs.get('hwBypassNewState', None))
        self.lldpNewTxState = EnumLldpNewTxState.enum(kwargs.get('lldpNewTxState', None))
        self.lldpNewTxInterval = kwargs.get('lldpNewTxInterval', None)
        self.lldpNewTxHold = kwargs.get('lldpNewTxHold', None)
        self.lldpNewVendtlv = EnumLldpNewVendtlv.enum(kwargs.get('lldpNewVendtlv', None))
        self.fdbStatsCreates = kwargs.get('fdbStatsCreates', None)
        self.fdbStatsDeletes = kwargs.get('fdbStatsDeletes', None)
        self.fdbStatsCurrent = kwargs.get('fdbStatsCurrent', None)
        self.fdbStatsHiwat = kwargs.get('fdbStatsHiwat', None)
        self.fdbStatsLookups = kwargs.get('fdbStatsLookups', None)
        self.fdbStatsLookupFails = kwargs.get('fdbStatsLookupFails', None)
        self.fdbStatsFinds = kwargs.get('fdbStatsFinds', None)
        self.fdbStatsFindFails = kwargs.get('fdbStatsFindFails', None)
        self.fdbStatsFindOrCreates = kwargs.get('fdbStatsFindOrCreates', None)
        self.fdbStatsOverflows = kwargs.get('fdbStatsOverflows', None)
        self.fdbClear = EnumFdbClear.enum(kwargs.get('fdbClear', None))
        self.cistRoot = kwargs.get('cistRoot', None)
        self.cistRootPathCost = kwargs.get('cistRootPathCost', None)
        self.cistRootPort = kwargs.get('cistRootPort', None)
        self.cistBridgeHelloTime = kwargs.get('cistBridgeHelloTime', None)
        self.cistBridgeMaxAge = kwargs.get('cistBridgeMaxAge', None)
        self.cistBridgeForwardDelay = kwargs.get('cistBridgeForwardDelay', None)
        self.cistRegionalRoot = kwargs.get('cistRegionalRoot', None)
        self.cistRegionalPathCost = kwargs.get('cistRegionalPathCost', None)
        self.dot1dBaseBridgeAddress = kwargs.get('dot1dBaseBridgeAddress', None)
        self.dot1dBaseNumPorts = kwargs.get('dot1dBaseNumPorts', None)
        self.dot1dBaseType = EnumDot1dBaseType.enum(kwargs.get('dot1dBaseType', None))
        self.dot1dStpProtocolSpecification = EnumDot1dStpProtocolSpecification.enum(kwargs.get('dot1dStpProtocolSpecification', None))
        self.dot1dStpPriority = kwargs.get('dot1dStpPriority', None)
        self.dot1dStpTimeSinceTopologyChange = kwargs.get('dot1dStpTimeSinceTopologyChange', None)
        self.dot1dStpTopChanges = kwargs.get('dot1dStpTopChanges', None)
        self.dot1dStpDesignatedRoot = kwargs.get('dot1dStpDesignatedRoot', None)
        self.dot1dStpRootCost = kwargs.get('dot1dStpRootCost', None)
        self.dot1dStpRootPort = kwargs.get('dot1dStpRootPort', None)
        self.dot1dStpMaxAge = kwargs.get('dot1dStpMaxAge', None)
        self.dot1dStpHelloTime = kwargs.get('dot1dStpHelloTime', None)
        self.dot1dStpHoldTime = kwargs.get('dot1dStpHoldTime', None)
        self.dot1dStpForwardDelay = kwargs.get('dot1dStpForwardDelay', None)
        self.dot1dStpBridgeMaxAge = kwargs.get('dot1dStpBridgeMaxAge', None)
        self.dot1dStpBridgeHelloTime = kwargs.get('dot1dStpBridgeHelloTime', None)
        self.dot1dStpBridgeForwardDelay = kwargs.get('dot1dStpBridgeForwardDelay', None)
        self.dot1dTpLearnedEntryDiscards = kwargs.get('dot1dTpLearnedEntryDiscards', None)
        self.dot1dTpAgingTime = kwargs.get('dot1dTpAgingTime', None)
        self.altSwTrapDisplayString = kwargs.get('altSwTrapDisplayString', None)
        self.altSwTrapRate = kwargs.get('altSwTrapRate', None)
        self.altSwTrapSeverity = kwargs.get('altSwTrapSeverity', None)
        self.sysDescr = kwargs.get('sysDescr', None)
        self.sysObjectID = kwargs.get('sysObjectID', None)
        self.sysUpTime = kwargs.get('sysUpTime', None)
        self.sysContact = kwargs.get('sysContact', None)
        self.sysName = kwargs.get('sysName', None)
        self.sysLocation = kwargs.get('sysLocation', None)
        self.sysServices = kwargs.get('sysServices', None)
        self.ifNumber = kwargs.get('ifNumber', None)
        self.snmpInPkts = kwargs.get('snmpInPkts', None)
        self.snmpInBadVersions = kwargs.get('snmpInBadVersions', None)
        self.snmpInBadCommunityNames = kwargs.get('snmpInBadCommunityNames', None)
        self.snmpInBadCommunityUses = kwargs.get('snmpInBadCommunityUses', None)
        self.snmpInASNParseErrs = kwargs.get('snmpInASNParseErrs', None)
        self.snmpEnableAuthenTraps = EnumSnmpEnableAuthenTraps.enum(kwargs.get('snmpEnableAuthenTraps', None))
        self.agAlteonCliCommand = kwargs.get('agAlteonCliCommand', None)        
        self.newCfgLmLicEnable = EnumGelState.enum(kwargs.get('newCfgLmLicEnable', None))
        self.newCfgLmLicPrimaryURL = kwargs.get('newCfgLmLicPrimaryURL', None)
        self.newCfgLmLicSecondaryURL = kwargs.get('newCfgLmLicSecondaryURL', None)
        self.newCfgLmLicPrimaryIpAddr = kwargs.get('newCfgLmLicPrimaryIpAddr', None)
        self.newCfgLmLicSecondaryIpAddr = kwargs.get('newCfgLmLicSecondaryIpAddr', None)
        self.newCfgLmLicPrimaryIpv6Addr = kwargs.get('newCfgLmLicPrimaryIpv6Addr', None)
        self.newCfgLmLicSecondaryIpv6Addr = kwargs.get('newCfgLmLicSecondaryIpv6Addr', None)
        self.newCfgLmLicInterval = kwargs.get('newCfgLmLicInterval', None)
        self.newCfgLmLicRetries = kwargs.get('newCfgLmLicRetries', None)
        self.newCfgLmLicRetryInterval = kwargs.get('newCfgLmLicRetryInterval', None)

