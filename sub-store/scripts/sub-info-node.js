async function operator(proxies = [], targetPlatform, env) {
    const { parseFlowHeaders, getFlowHeaders, flowTransfer } = flowUtils
    const {
      expires,
      total,
      usage: { upload, download },
    } = parseFlowHeaders(await getFlowHeaders(env.source[proxies[0].subName].url))
    const date = expires ? new Date(expires * 1000).toISOString().split('T')[0] : '';
  
    const prefixName = env.source[proxies[0].subName].displayName || env.source[proxies[0].subName].name
    const current = upload + download
    const currT = flowTransfer(Math.abs(current))
    currT.value = current < 0 ? '-' + currT.value : currT.value
    const totalT = flowTransfer(total)
  
    proxies.unshift({
      type: 'ss',
      server: '127.0.0.1',
      port: 8080,
      cipher: 'aes-128-gcm',
      password: 'password',
      name: `ℹ️ ${prefixName}: ${currT.value} ${currT.unit} / ${totalT.value} ${totalT.unit} ${date}`,
    })
    return proxies
  }
  