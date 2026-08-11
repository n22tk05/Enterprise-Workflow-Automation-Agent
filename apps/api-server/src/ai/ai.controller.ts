import { Body, Controller, Get, Post } from "@nestjs/common";
import { AiService } from "./ai.service";

@Controller("ai")
export class AiController {
    constructor(private readonly aiService: AiService) {}

    @Get('connect')
    async connect() {
        return await this.aiService.connectAi()
    }

    @Post('chat')
    async chat(@Body() body: any) {
        return await this.aiService.askAi(body.message, body.thread_id)
    }
}
