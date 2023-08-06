<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="1.0">
    <xsl:param name="file_name"/>
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>


    <!--
        ####################
        tei:header
        ####################
-->

    <xsl:template match="tei:listWit">
        <p/>
    </xsl:template>

    <!--
        ####################
        paragraphs
        ####################
-->

    <xsl:template match="tei:p[./tei:span[@class='pagenumber']]">
        <fw type="pageNum"><xsl:value-of select=".//text()"/></fw>
    </xsl:template>
    <xsl:template match="tei:p[@class='marginalie_place']">
        <p rendition="#marginalie_place"><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="tei:p[@class='footnote']">
        <note type="footnote"><xsl:apply-templates/></note>
    </xsl:template>
    <xsl:template match="tei:p[@class='footnote footnote-ff']">
        <note type="footnote" prev="true"><xsl:apply-templates/></note>
    </xsl:template>
    <xsl:template match="tei:p[@class='ff']">
        <p prev="true"><xsl:apply-templates/></p>
    </xsl:template>

    <!--
        ####################
        head / h1 h2 h3 4h
        ####################
-->

    <xsl:template match="tei:h2">
        <p rendition="#level_2"><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="tei:h1">
        <p rendition="#level_1"><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="tei:h3">
        <p rendition="#level_3"><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="tei:h4">
        <p rendition="#level_4"><xsl:apply-templates/></p>
    </xsl:template>


    <!--
        ####################
        renditions
        ####################
-->

    <!--no applied templates because inside tei:hi something like tei:sup must not occure-->
    <xsl:template match="tei:span[@class='smallcaps']">
        <hi><xsl:attribute name="rendition"><xsl:value-of select="concat('#', ./@class)"/></xsl:attribute><xsl:value-of select="."/></hi>
    </xsl:template>
    <xsl:template match="tei:span[@class='footnote-index']">
        <hi><xsl:attribute name="rendition"><xsl:value-of select="concat('#', ./@class)"/></xsl:attribute><xsl:value-of select="."/></hi>
    </xsl:template>
    <xsl:template match="tei:em">
        <hi><xsl:attribute name="rendition">#em</xsl:attribute><xsl:value-of select="."/></hi>
    </xsl:template>
    <xsl:template match="tei:sup">
        <xsl:value-of select="."/>
    </xsl:template>


    <!--
        ####################
        other things
        ####################
-->
    <xsl:template match="tei:blockquote">
        <q><xsl:apply-templates/></q>
    </xsl:template>

</xsl:stylesheet>
