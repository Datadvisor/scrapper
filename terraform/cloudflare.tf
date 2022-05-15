provider "cloudflare" {

}

resource "cloudflare_record" "www" {
	zone_id = "datadvisor.me"
	name    = "www"
	value   = "datadvisor.me"
	type		= "CNAME"
	proxied	= true
}
