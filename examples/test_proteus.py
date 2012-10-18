#!/usr/bin/python


from proteus import ProteusClient

if __name__=='__main__':
    a.login()
    #b=a.get_txt_record('_kerberos.opsec-auth-test1.ops.expertcity.com',view_name='Internal')
    #b=a.get_hinfo_record('dc2-dc2db','ops.expertcity.com',view_name='Internal')
    #b=a.get_cname_record('booterlin1','ops.expertcity.com',view_name='Internal')
    #print b
    b=a.get_mx_record('dc2-dc2db','ops.expertcity.com',view_name='Internal')
    print b
    #print b.id
    #print b.name
    #print b.properties.absoluteName
    #print b.properties.addresses
    #print b.properties.reverseRecord
    #c=a.get_hinfo_record('_kerberos.opsec-auth-test1','ops.expertcity.com',view_name='Internal')
    #print c
    #d=a.get_zone_list('ops.expertcity.com',view_name='Internal')
    #for i in d:
    #    print '%s - %s' % (i.name,i.type)
    #a.logout()
